from app.infra.mongo.settings import MongoSettings
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.database import Database
from app.api.advices.apiError import DataBaseError
from typing import Optional

class MongoDBProvider:
    
    def __init__(self, settings: MongoSettings) -> None:
        self._settings = settings
        self._client: Optional[MongoClient] = None
        

    def client(self) -> MongoClient:
        if self._client is None:
            self._client = MongoClient(
                self._settings.connection_string,
                tls=self._settings.tls,
                serverSelectionTimeoutMS=self._settings.server_selection_timeout_ms,
            )
        
        try:
            self._client.admin.command('ping')
        except PyMongoError as e:
            raise DataBaseError("Erro ao conectar ao MongoDB", meta={"details": str(e)}) from e
        
        return self._client
    
    
    def get_db(self) -> Database:
        return self.client()[self._settings.db_name]
        
    
    def disconnect(self) -> None:
        try:
            self.client().close()
            if self._client is not None:
                self._client = None
        
        except PyMongoError as e:
            raise DataBaseError("Erro ao desconectar do MongoDB", meta={"details": str(e)}) from e
        
        
    def get_collection(self, collection_name: str):
        return self.get_db()[collection_name]