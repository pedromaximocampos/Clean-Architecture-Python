from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple

from src.domain.ports.repositories.supplies_repository import ISuppliesRepository


from src.config.settings import CONST_ABASTECIMENTOS_COLLECTION
from src.domain.use_cases.models.principal_page import Venda
from src.infra.mongo.connection import MongoDBProvider


class MongoSuppliesRepository(ISuppliesRepository):

    _COLL_NAME = CONST_ABASTECIMENTOS_COLLECTION

    def __init__(self, mongo_provider: MongoDBProvider) -> None:
        self._collection = mongo_provider.get_collection(self._COLL_NAME)

    @staticmethod
    def return_dates(date: datetime) -> Tuple[datetime, datetime]:
        start_date: datetime = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = date

        # data antiga estou recebendo zerado, tenho que pegar o dia por completo
        if date.date() < datetime.now().date():
            end_date = date.replace(hour=23, minute=59, second=59, microsecond=999999)

        return start_date, end_date

    def get_supplies_by_ibms(self, ibms: list[str], date: datetime) -> Dict[str, Tuple[Venda, Venda]]:
        start_date, end_date = MongoSuppliesRepository.return_dates(date)

        prev_week_start :datetime = start_date - timedelta(days=7)
        prev_week_end: datetime = end_date - timedelta(days=7)

        pipeline = MongoSuppliesRepository.__supplies_pipeline(ibms, start_date, end_date, prev_week_start, prev_week_end)

        results = list(self._collection.aggregate(pipeline))

        by_ibm = {doc["ibm"]: {v["periodo"]: v for v in doc.get("vendas", [])}for doc in results}

        out: Dict[str, Tuple[Venda, Venda]] = {}

        for ibm in ibms:
            vendas_by_period = by_ibm.get(ibm, {})

            semana_doc = vendas_by_period.get("semana_passada") or MongoSuppliesRepository._default_doc(
                ibm, "semana_passada", prev_week_start, prev_week_end
            )
            atual_doc = vendas_by_period.get("atual") or MongoSuppliesRepository._default_doc(
                ibm, "atual", start_date, end_date
            )

            out[ibm] = (MongoSuppliesRepository._to_venda(ibm, semana_doc, prev_week_start),
                        MongoSuppliesRepository._to_venda(ibm, atual_doc, start_date))

        return out


    def find_first_and_last_sale_date(self) -> tuple[datetime, datetime]:
        pass

    @staticmethod
    def __supplies_pipeline(ibms: List[str], current_week_start: datetime, current_week_end:  datetime,
                            prev_week_start: datetime, prev_week_end: datetime) -> List[Dict[str, Any]]:
        """
            Retorna dados de duas semanas:
            - Semana passada (D-7): 00:00:00 até mesmo horário de 'date'
            - Semana atual (D-0): 00:00:00 até horário de 'date'
            """
        #  SEMANA ATUAL: D-0 00:00:00 até date (horário atual)



        # ✅ STAGES REUTILIZÁVEIS
        convert_stage = {
            "$set": {
                "cusDbl": {"$convert": {"input": "$cus", "to": "double", "onError": 0, "onNull": 0}},
                "volDbl": {"$convert": {"input": "$vol", "to": "double", "onError": 0, "onNull": 0}},
                "valDbl": {"$convert": {"input": "$val", "to": "double", "onError": 0, "onNull": 0}},
            }
        }

        cost_stage = {"$set": {"cost": {"$multiply": ["$cusDbl", "$volDbl"]}}}
        profit_stage = {"$set": {"profit": {"$subtract": ["$valDbl", "$cost"]}}}

        group_stage = {
            "$group": {
                "_id": "$ibm",
                "pAbst": {"$min": "$dtHr"},
                "uAbst": {"$max": "$dtHr"},
                "nAbst": {"$sum": 1},
                "tVol": {"$sum": "$volDbl"},
                "tVal": {"$sum": "$valDbl"},
                "tCost": {"$sum": "$cost"},
                "tProfit": {"$sum": "$profit"},
            }
        }

        project_after_group = {
            "$project": {
                "_id": 0,
                "ibm": "$_id",
                "pAbst": 1,
                "uAbst": 1,
                "nAbst": 1,
                "tVol": 1,
                "tVal": 1,
                "tCost": 1,
                "tProfit": 1,
                "periodo": 1,
            }
        }

        pipeline =  [
            # 1) MATCH inicial (atenção: confira se 'lmc' é o campo certo; se for 'lmv', ajuste)
            {
                "$match": {
                    "ibm": {"$in": ibms},
                    "sig": {"$exists": True},
                    "lmc": {"$exists": True},
                    "ori": {"$in": ["0", "1", "5"]},
                    "dtHr": {"$gte": prev_week_start, "$lte": current_week_end}
                }
            },

            # 2) conversões e métricas
            convert_stage,
            cost_stage,
            profit_stage,

            # 3) facet por janelas
            {
                "$facet": {
                    "atual": [
                        {"$match": {"dtHr": {"$gte": current_week_start, "$lte": current_week_end}}},
                        group_stage,
                        {"$addFields": {"periodo": "atual"}},
                        project_after_group,
                    ],
                    "semana_passada": [
                        {"$match": {"dtHr": {"$gte": prev_week_start, "$lte": prev_week_end}}},
                        group_stage,
                        {"$addFields": {"periodo": "semana_passada"}},
                        project_after_group,
                    ],
                }
            },

            # 4) concatena as janelas e mantém só quem tem pelo menos uma
            {"$project": {"all": {"$concatArrays": ["$atual", "$semana_passada"]}}},
            {"$unwind": "$all"},
            {"$group": {"_id": "$all.ibm", "vendas": {"$push": "$all"}}},

            # 5) shape final
            {"$project": {"_id": 0, "ibm": "$_id", "vendas": 1}},
        ]

        return pipeline

    @staticmethod
    def _to_venda(ibm: str, venda: dict, date: datetime) -> Venda:
        n = venda['nAbst']
        vol = venda['tVol']
        val = venda['tVal']
        cost = venda['tCost']
        profit = venda['tProfit']

        primeiro_abastecimento = venda.get('pAbst')
        ultimo_abastecimento = venda.get('uAbst')

        if primeiro_abastecimento is not None and isinstance(primeiro_abastecimento, datetime):
            primeiro_abastecimento.strftime("%H:%M")

        if ultimo_abastecimento is not None and isinstance(ultimo_abastecimento, datetime):
            ultimo_abastecimento.strftime("%H:%M")
        return Venda(
            ibm=ibm,
            data=str(date.date()),
            abastecimentos=n,
            volume=vol,
            valor=val,
            custo=cost,
            lucro=profit,
            ppl=(val / vol) if vol > 0 else 0.0,
            cpl=(cost / vol) if vol > 0 else 0.0,
            lpl=(profit / vol) if vol > 0 else 0.0,
            ticketMedioValor=(val / n) if n > 0 else 0.0,
            ticketMedioVolume=(vol / n) if n > 0 else 0.0,
            ticketMedioLucro=(profit / n) if n > 0 else 0.0,
            ticketMedioCusto=(cost / n) if n > 0 else 0.0,
            primeiro_abastecimento=str(primeiro_abastecimento),
            ultimo_abastecimento=str(ultimo_abastecimento),
        )

    @staticmethod
    def _default_doc( ibm: str, periodo: str, di: datetime, df: datetime) -> dict:
        # Doc “cru” no mesmo formato que sai do Mongo antes do _to_venda
        return {
            "periodo": periodo,
            "dataInicio": di,
            "dataFim": df,
            "pAbst": None,
            "uAbst": None,
            "nAbst": 0,
            "tVol": 0.0,
            "tVal": 0.0,
            "tCost": 0.0,
            "tProfit": 0.0,
            "ibm": ibm,
        }