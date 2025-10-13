from datetime import timedelta

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

    def __init__(self, supplies_repository: ISuppliesRepository,
                 daily_consolidation_repository: IDailyConsolidationRepository,
                 principal_cache_repository: IPrincipalDataCacheRepository):
        self.supplies_repository = supplies_repository
        self.daily_consolidation_repository = daily_consolidation_repository
        self.principal_cache_repository = principal_cache_repository


    def execute(self, input_data: GetPrincipalInput) -> GetPrincipalOutput:
        user_principal: UserPrincipal = get_current_user()
        set_input_ibms = set(input_data.ibms)
        ibms_to_search = input_data.ibms


        if UtilsMethods.should_read_cache(input_data.date):






    def _run_today_use_case(self, input_data: GetPrincipalInput, user_principal: UserPrincipal) -> GetPrincipalOutput:
        set_input_ibms = set(input_data.ibms)

        cached_data: list[PostoResumo] = self.principal_cache_repository.get_principal_data(input_data.ibms,
                                                                                            user_principal.email)
        cached_ibms = [data.ibm for data in cached_data]

        ibms_to_search = list(set_input_ibms - set(cached_ibms))

        if not ibms_to_search:
            return GetPrincipalOutput(postos=cached_data)


        sales_data: List[Dict[str, Any]] = self._fetch_and_consolidate_data(ibms_to_search, user_principal)


        today_sales = self.supplies_repository.get_supplies_by_ibms(ibms_to_search, UtilsMethods.get_today_date())
        first_date, last_date = self.supplies_repository.find_first_and_last_sale_date()
        consolidated_data = self.daily_consolidation_repository.get_consolidated_data_by_ibms_and_date_range(ibms_to_search, first_date, last_date)

        postos_resumo: list[PostoResumo] = []

        for ibm in ibms_to_search:
            posto_sales = [sale for sale in today_sales if sale.ibm == ibm]
            posto_consolidated = [data for data in consolidated_data if data.ibm == ibm]

            posto_resumo = PostoResumo(
                ibm=ibm,
                vendas=posto_sales,
                consolidado=posto_consolidated
            )

            postos_resumo.append(posto_resumo)

        self.principal_cache_repository.save_principal_data(postos_resumo, user_principal.email)

        return postos_resumo


    def get_postos_data(self, ibms: list[str], date: datetime) -> list[PostoResumo]:
        past_week_sales: list[Venda] = self.supplies_repository.get_supplies_by_ibms(ibms,
                                                                                    date - timedelta(
                                                                                         days=7))

        week_sales: list[Venda] = self.supplies_repository.get_supplies_by_ibms(ibms, date)

        past_week_map = {venda.ibm: venda for venda in past_week_sales}
        week_map = {venda.ibm: venda for venda in week_sales}

        list_postos: list[PostoResumo] = []

        for key, past_week_venda in past_week_map:
            week_map_sales = week_map.get(key)

            variation = Variacao(
                valor= UtilsMethods.calculate_variation(past_week_venda.valor, week_map_sales.valor),
            )




