from email.policy import default

from redis import Redis
import json
from src.domain.ports.repositories.principal_data_cache_repository import IPrincipalDataCacheRepository
from src.domain.use_cases.models.principal_page import GetPrincipalOutput, PostoResumo
from src.infra.redis.connection import RedisProvider


class RedisPrincipalCacheRepository(IPrincipalDataCacheRepository):

    def __init__(self, redis_client: RedisProvider):
        self.redis_client: Redis = redis_client.client()
        self._page_field = 'principal'


    def get_principal_data(self, ibms: list[str], user_id: str) -> list[PostoResumo]:
        pipeline = self.redis_client.pipeline()

        for key in ibms:
            page_field = f'{self._page_field}:{key}'
            pipeline.hget(user_id, page_field)

        cached_data = pipeline.execute()

        deserialized_data = [PostoResumo.from_json(data) for data in cached_data]

        return deserialized_data

    def set_principal_data(self, data: GetPrincipalOutput) -> None:
        pass

    def delete_principal_data(self, ibms: list[str]) -> None:
        pass

    def check_exists(self, ibms: list[str]) -> dict[str, bool]:
        pass
