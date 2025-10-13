from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple

from src.domain.ports.repositories.supplies_repository import ISuppliesRepository


from src.config.settings import CONST_ABASTECIMENTOS_COLLECTION
from src.domain.use_cases.models.principal_page import Venda
from src.infra.mongo.connection import MongoDBProvider


class MongoSuppliesRepository(ISuppliesRepository):

    # _COLL_NAME = CONST_ABASTECIMENTOS_COLLECTION
    _COLL_NAME = "Abastecimentos"

    def __init__(self, mongo_provider: MongoDBProvider) -> None:
        self._db = mongo_provider.get_db()
        self._collection = mongo_provider.get_collection(self._COLL_NAME)

    def get_supplies_by_ibms(self, ibms: list[str], date: datetime) -> Dict[str, Tuple[Venda, Venda]]:
        pipeline = self.__supplies_pipeline(ibms, date)
        results = list(self._db.aggregate(pipeline))

        out: Dict[str, Tuple[Venda, Venda]] = {}

        for result in results:
            ibm = result['ibm']
            vendas_by_period = {v['periodo']: v for v in result['vendas']}
            semana = self._to_venda(ibm, vendas_by_period['semana_passada'])
            atual = self._to_venda(ibm, vendas_by_period['atual'])
            out[ibm] = (semana, atual)

        return out


    def find_first_and_last_sale_date(self) -> tuple[datetime, datetime]:
        pass

    def __supplies_pipeline(self,ibms: List[str], date: datetime) -> List[Dict[str, Any]]:
        # Referências de tempo
        date_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        date_end = date
        past_week_start = date_start - timedelta(days=7)
        past_week_end = date_end - timedelta(days=7)

        seed = [{"ibm": i} for i in ibms]

        # Sub-pipeline comum com melhor uso de índice:
        # 1º $match com filtros fixos (aproveita índices)
        # 2º $match com $expr para vincular $$ibm
        def lookup_pipeline(period_start, period_end):
            return [
                {"$match": {
                    "dtHr": {"$gte": period_start, "$lte": period_end},
                    "ori": {"$in": ["0", "1", "5"]},
                    "sig": {"$ne": None},
                    "lmc": {"$ne": None}
                }},
                {"$match": {"$expr": {"$eq": ["$ibm", "$$ibm"]}}},
                {"$set": {
                    "cusDbl": {"$convert": {"input": "$cus", "to": "double", "onError": 0, "onNull": 0}},
                    "volDbl": {"$convert": {"input": "$vol", "to": "double", "onError": 0, "onNull": 0}},
                    "valDbl": {"$convert": {"input": "$val", "to": "double", "onError": 0, "onNull": 0}}
                }},
                {"$set": {
                    "cost": {"$multiply": ["$cusDbl", "$volDbl"]},
                    "profit": {"$subtract": ["$valDbl", "$cost"]}
                }},
                {"$group": {
                    "_id": None,
                    "pAbst": {"$min": "$dtHr"},
                    "uAbst": {"$max": "$dtHr"},
                    "nAbst": {"$sum": 1},
                    "tVol": {"$sum": "$volDbl"},
                    "tVal": {"$sum": "$valDbl"},
                    "tCost": {"$sum": "$cost"},
                    "tProfit": {"$sum": "$profit"}
                }},
                {"$project": {"_id": 0, "pAbst": 1, "uAbst": 1, "nAbst": 1, "tVol": 1, "tVal": 1, "tCost": 1,
                              "tProfit": 1}}
            ]

        return [
            {"$documents": seed},

            # Hoje (dia de interesse) [today_start, next_day_start)
            {"$lookup": {
                "from": self._COLL_NAME,
                "let": {"ibm": "$ibm"},
                "pipeline": lookup_pipeline(date_start, date_end),
                "as": "hoje"
            }},

            # Semana passada [last_week_start, today_start)
            {"$lookup": {
                "from": self._COLL_NAME,
                "let": {"ibm": "$ibm"},
                "pipeline": lookup_pipeline(past_week_start, past_week_end),
                "as": "ultSemana"
            }},

            # Zera quando faltar
            {"$set": {
                "vendaHoje": {
                    "$ifNull": [
                        {"$first": "$hoje"},
                        {"pAbst": None, "uAbst": None, "nAbst": 0, "tVol": 0, "tVal": 0, "tCost": 0, "tProfit": 0}
                    ]
                },
                "vendaUltSemana": {
                    "$ifNull": [
                        {"$first": "$ultSemana"},
                        {"pAbst": None, "uAbst": None, "nAbst": 0, "tVol": 0, "tVal": 0, "tCost": 0, "tProfit": 0}
                    ]
                }
            }},

            # Saída final
            {"$project": {
                "_id": 0,
                "ibm": 1,
                "vendas": [
                    {"$mergeObjects": [
                        {"periodo": "semana_passada", "dataInicio": past_week_start,
                         "dataFim": past_week_end},
                        "$vendaUltSemana"
                    ]},
                    {"$mergeObjects": [
                        {"periodo": "atual", "dataInicio": date_start, "dataFim": date_end},
                        "$vendaHoje"
                    ]}
                ]
            }}
        ]

    def _to_venda(self, ibm: str, venda: dict) -> Venda:
        n = venda['nAbst']
        vol = venda['tVol']
        val = venda['tVal']
        cost = venda['tCost']
        profit = venda['tProfit']
        return Venda(
            ibm=ibm,
            data=venda['dataFim'].date(),
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
            primeiro_abastecimento=venda.get('pAbst'),
            ultimo_abastecimento=venda.get('uAbst'),
        )

