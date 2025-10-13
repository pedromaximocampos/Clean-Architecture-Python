from dataclasses import asdict

from redis import Redis
import json
from src.domain.ports.repositories.principal_data_cache_repository import IPrincipalDataCacheRepository
from src.domain.use_cases.models.principal_page import  PostoResumo
from src.infra.redis.connection import RedisProvider
from src.config.constants import CACHE_TTL
from src.infra.redis.mappers.serializer import Serializer

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

        if not cached_data or all(data is None for data in cached_data):
            return []

        deserialized_data = [PostoResumo.from_json(data) for data in cached_data]

        return deserialized_data

    def set_principal_data(self, data: list[PostoResumo], user_id: str) -> None:
        save_pipeline = self.redis_client.pipeline()

        for item in data:
            key = item.ibm

            page_field = f'{self._page_field}:{key}'

            gas_summary  = asdict(item)

            serialized_gas_summary = json.dumps(gas_summary, default=Serializer.to_primitive)

            save_pipeline.hset(user_id, page_field, serialized_gas_summary)

            save_pipeline.expire(user_id, CACHE_TTL, nx=True)

        save_pipeline.execute()


    def clear_cache(self, user_id: str) -> None:
        self.redis_client.delete(user_id)
