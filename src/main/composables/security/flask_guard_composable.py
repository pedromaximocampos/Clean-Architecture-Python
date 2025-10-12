from src.infra.redis.providers import get_redis_provider
from src.infra.mongo.providers import get_gmon_provider

from src.infra.redis.repositories.redis_session_repository import RedisSessionRepository
from src.infra.mongo.repositories.mongo_admin_repository import MongoAdminUserRepository
from src.infra.security.jwt_token_service import JWTTokenService

from src.main.adapters.flask_adapter.flask_auth_guard_adapter import FlaskAuthGuardAdapter

from src.application.services.security.auth_guard_impl import AuthGuardImpl

from src.config.settings import JWT_SECRET

def create_flask_guard_composable() -> FlaskAuthGuardAdapter:
    redis_provider = get_redis_provider()
    gmon_provider = get_gmon_provider()

    session_repository = RedisSessionRepository(redis_provider)
    admin_repository = MongoAdminUserRepository(gmon_provider)

    auth_guard_adapter = AuthGuardImpl(JWTTokenService(JWT_SECRET), session_repository, admin_repository)
    flask_guard = FlaskAuthGuardAdapter(auth_guard_adapter)
    
    return flask_guard