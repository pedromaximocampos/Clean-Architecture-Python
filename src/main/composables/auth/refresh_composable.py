# Caso de uso para refresh de token
from src.application.use_cases_impl.auth.refresh import AuthRefreshUseCase
# Repositórios Mongo
from src.infra.mongo.repositories.mongo_admin_repository import MongoAdminUserRepository
from src.infra.mongo.repositories.mongo_user_profile_repository import MongoUserProfileRepository
# Repositório Redis
from src.infra.redis.repositories.redis_session_repository import RedisSessionRepository
# Servicos de token
from src.infra.security.jwt_token_service import JWTTokenService
# Providers de banco de dados
from src.infra.mongo.providers import get_gmon_provider
from src.infra.redis.providers import get_redis_provider
# cliente terceiros
from src.infra.auth.lbc_auth_client import LBCAuthClient
# Controller com o handle request
from src.presentation.controllers.auth.refresh_controller import RefreshController
# envs
from src.config.settings import JWT_SECRET


def get_refresh_composable():

    gmon_provider = get_gmon_provider()
    redis_provider = get_redis_provider()

    user_repository = MongoUserProfileRepository(gmon_provider)
    session_repository = RedisSessionRepository(redis_provider)
    admin_repository = MongoAdminUserRepository(gmon_provider)

    lbc_auth_client = LBCAuthClient()

    token_service = JWTTokenService(JWT_SECRET)

    refresh_use_case = AuthRefreshUseCase(
        user_repository=user_repository,
        session_repository=session_repository,
        lbc_auth_client=lbc_auth_client,
        token_service=token_service,
        admin_repository=admin_repository
    )

    refresh_controller = RefreshController(refresh_use_case)

    return refresh_controller.handle_request