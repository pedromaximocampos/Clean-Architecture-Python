from typing import Optional
import logging
from src.infra.redis.settings import RedisSettings
from redis import Redis, RedisError
from threading import Lock

class RedisProvider:

    def __init__(self, settings: RedisSettings) -> None:
        self._settings = settings
        self._client: Optional[Redis] = None
        self._connected_once = False
        self._lock = Lock()


    def client(self) -> Redis:
        if self._client is None:
            with self._lock:
                # Conexão única (lazy-connection) primeira requisicao estabelece a conexao com o Redis
                if self._client is None and not self._connected_once:
                    self._client = Redis(
                        host=self._settings.host,
                        port=self._settings.port,
                        password=self._settings.password,
                        decode_responses=True,
                        username='default',
                        ssl=True
                    )

                try:
                    self._client.ping()

                    logging.info("Redis conectado.")
                    print("Redis conectado.")
                except RedisError as e:
                    self._client = None
                    logging.error("Erro ao conectar ao Redis")
                    raise RedisError("Erro ao conectar ao Redis") from e

                self._connected_once = True

        assert self._client is not None
        return self._client


    def disconnect(self) -> None:
        if self._client is not None:
            with self._lock:
                try:
                    self.client().close()
                    logging.info("Conexão Redis fechada.")
                except RedisError as e:
                    logging.error("Erro ao desconectar do Redis")
                    raise RedisError("Erro ao desconectar do Redis") from e
                finally:
                    self._client = None
                    self._connected_once = False


