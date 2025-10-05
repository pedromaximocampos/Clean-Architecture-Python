
from app.infra.mongo.connection import MongoDBProvider

ACTIVE_USER_FILTER = {"deletedAt": {"exists": False}}
USER_COLLECTION = "UserProfile"

class MongoUserProfileRepository:
    
    def __init__(self, db: MongoDBProvider) -> None:
        self._collection = db.get_collection(USER_COLLECTION)
        
        
    def find_by_email(self, email: str):
        pass