from src.infra.redis.settings import RedisSettings
from src.infra.redis.connection import RedisProvider
from src.config.settings import LOCAL_REDIS_HOST, LOCAL_REDIS_PORT, LOCAL_REDIS_PASSWORD, LOCAL_REDIS_USER
from src.config.settings import DEV

ssl = True

if DEV:
    ssl = False


redis_settings = RedisSettings(
        host=LOCAL_REDIS_HOST,
        port=int(LOCAL_REDIS_PORT),
        password=LOCAL_REDIS_PASSWORD,
        user= LOCAL_REDIS_USER,
        ssl=ssl
)


redis_provider = RedisProvider(redis_settings)


def get_redis_provider() -> RedisProvider:
    return redis_provider