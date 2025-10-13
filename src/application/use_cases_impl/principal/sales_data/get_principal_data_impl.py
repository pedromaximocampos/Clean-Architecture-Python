from datetime import timedelta, datetime
from typing import Dict, Tuple

from src.domain.ports.security.models.user_principal import UserPrincipal
from src.domain.use_cases.models.principal_page import GetPrincipalInput, GetPrincipalOutput, PostoResumo, Venda, \
    Variacao
from src.domain.use_cases.principal_page.sales_data.get_principal_data import IGetPrincipalDataUseCase
from src.domain.ports.repositories.supplies_repository import ISuppliesRepository
from src.domain.ports.repositories.daily_consolidation_repository import IDailyConsolidationRepository
from src.domain.ports.repositories.principal_data_cache_repository import IPrincipalDataCacheRepository

from src.utils.utils import UtilsMethods
from src.shared.contexts.current_user import get_current_user

class GetPrincipalDataImpl(IGetPrincipalDataUseCase):

    def __init__(self, supplies_repository: ISuppliesRepository, principal_cache_repository: IPrincipalDataCacheRepository):
        self.supplies_repository = supplies_repository
        self.principal_cache_repository = principal_cache_repository


    def execute(self, input_data: GetPrincipalInput) -> GetPrincipalOutput:
        user_principal: UserPrincipal = get_current_user()

        if UtilsMethods.should_read_cache(input_data.date):
            return self._run_today_use_case(input_data, user_principal)
        else:
            return self._run_old_date_use_case(input_data, user_principal)


    def _run_old_date_use_case(self, input_data: GetPrincipalInput, user_principal: UserPrincipal) -> GetPrincipalOutput:
        stations: list[PostoResumo] = self.get_postos_data(input_data.ibms, input_data.date)

        response  = GetPrincipalOutput(postos=stations)

        return response


    def _run_today_use_case(self, input_data: GetPrincipalInput, user_principal: UserPrincipal) -> GetPrincipalOutput:
        set_input_ibms = set(input_data.ibms)

        cached_data: list[PostoResumo] = self.principal_cache_repository.get_principal_data(input_data.ibms,
                                                                                            user_principal.email)
        cached_ibms = [data.ibm for data in cached_data]

        ibms_to_search = list(set_input_ibms - set(cached_ibms))

        if not ibms_to_search:
            return GetPrincipalOutput(postos=cached_data)


        found_in_mongo: list[PostoResumo] = self.get_postos_data(ibms_to_search, input_data.date)

        # self.manage_redis_cache()

        self.principal_cache_repository.set_principal_data(found_in_mongo, user_principal.email)

        stations: list[PostoResumo] = cached_data + found_in_mongo

        response  = GetPrincipalOutput(postos=stations)

        return response

    def manage_redis_cacha(self, found_in_mongo: list[PostoResumo], user_email: str):
        if len(found_in_mongo) > 10:
            # self.principal_cache_repository.clear_oldest_cache()
            pass


    def get_postos_data(self, ibms: list[str], date: datetime) -> list[PostoResumo]:

        sales_data: Dict[str, Tuple[Venda, Venda]] = self.supplies_repository.get_supplies_by_ibms(ibms, date)

        postos: list[PostoResumo] = []
        for ibm, sales_data in sales_data.items():
            past_week_sales: Venda = sales_data[0]
            date_of_interest_sales: Venda = sales_data[1]
            lista_venda : list[Venda] = [past_week_sales, date_of_interest_sales]

            variation: Variacao = GetPrincipalDataImpl._calculate_variation(sales_data)
            posto_resumo = PostoResumo(
                ibm=ibm,
                vendas=lista_venda,
                variacao=variation,
                primeiro_abastecimento=date_of_interest_sales.primeiro_abastecimento,
                ultimo_abastecimento=date_of_interest_sales.ultimo_abastecimento,
            )
            postos.append(posto_resumo)

        return postos



    @staticmethod
    def _calculate_variation(sales_data: tuple[Venda, Venda]) -> Variacao:

        past_week_sales, date_of_interest_sales = sales_data

        variation = Variacao(
            abastecimentos=UtilsMethods.calculate_variation(date_of_interest_sales.abastecimentos, past_week_sales.abastecimentos),
            custo=UtilsMethods.calculate_variation(date_of_interest_sales.custo, past_week_sales.custo),
            lucro=UtilsMethods.calculate_variation(date_of_interest_sales.lucro, past_week_sales.lucro),
            valor=UtilsMethods.calculate_variation(date_of_interest_sales.valor, past_week_sales.valor),
            volume=UtilsMethods.calculate_variation(date_of_interest_sales.volume, past_week_sales.volume),
            lpl=UtilsMethods.calculate_variation(date_of_interest_sales.lpl, past_week_sales.lpl),
            ppl=UtilsMethods.calculate_variation(date_of_interest_sales.ppl, past_week_sales.ppl),
            cpl=UtilsMethods.calculate_variation(date_of_interest_sales.cpl, past_week_sales.cpl),
            ticketMedioValor=UtilsMethods.calculate_variation(date_of_interest_sales.ticketMedioValor, past_week_sales.ticketMedioValor),
            ticketMedioVolume=UtilsMethods.calculate_variation(date_of_interest_sales.ticketMedioVolume, past_week_sales.ticketMedioVolume)
        )

        return variation

