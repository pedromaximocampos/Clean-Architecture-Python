from pymongo.collection import Collection

from src.domain.ports.repositories.admin_repository import IAdminUserRepository

from src.config.settings import CONST_ADMINISTRATOR_COLLECTION
from src.infra.mongo.connection import MongoDBProvider


class MongoAdminUserRepository(IAdminUserRepository):


    _COL_NAME = CONST_ADMINISTRATOR_COLLECTION

    def __init__(self, db_provider: MongoDBProvider) -> None:
        self._col: Collection = db_provider.get_collection(self._COL_NAME)

    def is_admin(self, user_email: str) -> bool:

        admin = self._col.find_one({"email": user_email})

        if admin:
            return True
        return False