from src.infra.mongo.providers import get_gmon_provider
from src.infra.redis.providers import get_redis_provider

from src.infra.mongo.repositories.mongo_supplies_repository import MongoSuppliesRepository
from src.infra.redis.repositories.redis_principal_cache_repository import RedisPrincipalCacheRepository

from src.application.use_cases_impl.principal.sales_data.get_principal_data_impl import GetPrincipalDataImpl

from src.presentation.controllers.principal.sales_data.principal_sales_controller import PrincipalSalesController


def get_principal_composable():
    gmon_provider = get_gmon_provider()
    redis_provider = get_redis_provider()

    supplies_repository = MongoSuppliesRepository(gmon_provider)
    principal_cache_repository = RedisPrincipalCacheRepository(redis_provider)

    get_principal_data_use_case = GetPrincipalDataImpl(
        supplies_repository=supplies_repository,
        principal_cache_repository=principal_cache_repository
    )

    principal_sales_controller = PrincipalSalesController(get_principal_data_use_case)

    return principal_sales_controller.handle_request
