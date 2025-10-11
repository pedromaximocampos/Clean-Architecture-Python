# Providers
from src.infra.redis.providers import get_redis_provider
from src.infra.mongo.providers import get_providers
# Repositories
from src.infra.mongo.repositories.mongo_user_profile_repository import MongoUserProfileRepository
from src.infra.redis.repositories.redis_session_repository import RedisSessionRepository
# Clients and Services
from src.infra.auth.lbc_auth_client import LBCAuthClient
from src.infra.security.jwt_token_service import JWTTokenService
# Controllers
from src.presentation.controllers.auth.login_controller import LoginController
# Use Case
from src.application.use_cases_impl.auth.login import LoginUseCaseImpl
# Jwt Secret
from src.config.settings import JWT_SECRET

def login_composable():
    mongo_provider = get_providers()
    redis_provider = get_redis_provider()

    user_repository = MongoUserProfileRepository(mongo_provider)
    session_repository = RedisSessionRepository(redis_provider)

    lbc_auth_client = LBCAuthClient()
    token_service = JWTTokenService(JWT_SECRET)

    login_use_case = LoginUseCaseImpl(
        user_repository=user_repository,
        session_repository=session_repository,
        lbc_auth_client=lbc_auth_client,
        token_service=token_service
    )

    login_controller = LoginController(login_use_case)

    return login_controller.handle_request
