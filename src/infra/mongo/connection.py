import logging

from src.infra.mongo.settings import MongoSettings
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.database import Database
from src.data.advices.apiError import DataBaseError
from threading import Lock
from typing import Optional


logger = logging.getLogger(__name__)

class MongoDBProvider:
    
    def __init__(self, settings: MongoSettings) -> None:
        self._settings = settings
        self._client: Optional[MongoClient] = None
        self._connected_once = False
        self._lock = Lock()

    def client(self) -> MongoClient:
        if self._client is None:
            with self._lock:
                 # Conexão única
                if self._client is None and not self._connected_once:
                    self._client = MongoClient(
                        self._settings.connection_string,
                        tls=self._settings.tls,
                        serverSelectionTimeoutMS=self._settings.server_selection_timeout_ms,
                    )

                try:
                    self._client.admin.command('ping')

                    logger.info("MongoDB conectado.")

                except PyMongoError as e:
                    self._client = None

                    logger.error("erro ao conectar ao MongoDB")
                    raise DataBaseError("Erro ao conectar ao MongoDB", meta={"details": str(e)}) from e

                logging.info("conectado ao MongoDB")
                self._connected_once = True

        return self._client
    
    
    def get_db(self) -> Database:
        return self.client()[self._settings.db_name]
        
    
    def disconnect(self) -> None:
        if self._client is not None:
            with self._lock:
                try:
                    self.client().close()
                    logger.info("Conexão MongoDB fechada.")
                except PyMongoError as e:
                    logger.error("Erro ao fechar a conexão com o MongoDB.")
                    raise DataBaseError("Erro ao desconectar do MongoDB", meta={"details": str(e)}) from e
                finally:
                    self._client = None
                    self._connected_once = False
        
        
    def get_collection(self, collection_name: str):
        return self.get_db()[collection_name]