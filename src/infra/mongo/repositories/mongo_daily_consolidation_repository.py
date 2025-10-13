from pymongo.collection import Collection
from datetime import datetime
from src.domain.ports.repositories.daily_consolidation_repository import IDailyConsolidationRepository
from src.domain.use_cases.models.principal_page import Venda
from src.infra.mongo.connection import MongoDBProvider

from src.config.settings import CONST_CONSOLIDATE_COLLECTION


class ConsolidationRepository(IDailyConsolidationRepository):

    _COL_NAME = CONST_CONSOLIDATE_COLLECTION

    def __init__(self, mongo_provider: MongoDBProvider) -> None:
        self._collection: Collection = mongo_provider.get_collection(self._COL_NAME)

    def get_consolidation_by_date(self, date: datetime, ibm:  list[str]) -> list[Venda]:
        formated_data= date.replace(hour=0, minute=0, second=0, microsecond=0)

        q = {"data": formated_data, "ibm": {"$in": ibm}}
        found_count = self._collection.count_documents(q)

        if found_count != len(set(ibm)):
            return []

        docs = list(self._collection.find(q))
        vendas: list[Venda] = []

        for doc in docs:

            qab = doc["qAb"]

            custo = doc["tCost"]
            lucro = doc["tProf"]
            valor = doc["tVal"]
            volume = doc["tVol"]

            custo_por_litro = round(custo / volume, 2) if volume != 0 else 0
            lucro_por_litro = round(lucro / volume, 2) if volume != 0 else 0
            preco_por_litro = round(valor / volume, 2) if volume != 0 else 0


            venda = Venda(
                data=doc["dtHr"],
                ibm=doc["ibm"],
                abastecimentos=qab,
                custo=custo,
                lucro=lucro,
                valor=valor,
                volume=volume,
                ticketMedioValor=doc["tmVal"],
                ticketMedioVolume=doc["tmVol"],
                ticketMedioCusto=doc["tmCost"],
                ticketMedioLucro=doc["tmProf"],
                cpl=custo_por_litro,
                ppl=preco_por_litro,
                lpl=lucro_por_litro

            )
            vendas.append(venda)

        return vendas


    def save_consolidation(self, venda: Venda) -> None:
        pass

    def delete_d2_to_d0_consolidations(self) -> None:
        pass

    def delete_old_consolidations(self) -> None:
        pass

    def consolidate_today_and_yesterday(self) -> None:
        pass

    def chek_if_consolidation_exists(self) -> None:
        pass