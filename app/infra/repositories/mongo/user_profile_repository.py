
from app.infra.mongo.connection import MongoDBProvider
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from app.domain.entities.user_profile_domain_entity import UserProfile
from app.infra.mongo.mappers.user_profile_mapper import UserProfileMapper
from typing import Optional
from app.shared.customExceptions import UniqueViolation
from bson import ObjectId

ACTIVE_USER_FILTER = {"deletedAt": {"exists": False}}
USER_COLLECTION = "UserProfile"

class MongoUserProfileRepository:
    ''' 
    Repositório MongoDB para UserProfile 
    - Criado o índice no qual deixa único o email em conjunto com deletedAt == null (logicamente ativo) 
        caso o usuário seja deletado logicamente, e necessario que se crie novamente com o email anterior
    - Garante unicidade de email entre usuários ativos (não deletados)
    - Operações CRUD básicas
    '''

    _collection: Collection
    _USER_COLLECTION_NAME: str = "UserProfile"
    _ACTIVE_USER_FILTER: dict = {"deletedAt": {"$exists": False}}

    def __init__(self, db: MongoDBProvider) -> None:
        self._collection = db.get_collection(self._USER_COLLECTION_NAME)


    def find_by_mongo_id(self, mongo_id: str) -> Optional[UserProfile]:
        document = self._collection.find_one({"_id": mongo_id, **self._ACTIVE_USER_FILTER})
        if document:
            return UserProfileMapper.from_document(document)
        return None


    def find_by_email(self, email: str) -> Optional[UserProfile]:
        document = self._collection.find_one({"email": email, **self._ACTIVE_USER_FILTER})
        if document:
            return UserProfileMapper.from_document(document)
        return None
        
        
    def create_user(self, user: UserProfile) -> UserProfile:
        user_data = UserProfileMapper.to_document(user)
        try:
            result = self._collection.insert_one(user_data)
        except DuplicateKeyError:
            raise UniqueViolation(field="email", value=user.email)
        
        created_user = self.find_by_mongo_id(result.inserted_id)
        return created_user
    
    
    def update_user(self, user: UserProfile) -> UserProfile:
        user_data = UserProfileMapper.to_document(user)
        mongo_id = user.id
        if not mongo_id:
            raise ValueError("User must have a valid MongoDB _id for update.")
        
        try:
            self._collection.update_one(
                {"_id": ObjectId(mongo_id), **self._ACTIVE_USER_FILTER},
                {"$set": user_data}
            )
        except DuplicateKeyError:
            raise UniqueViolation(field="email", value=user.email)
        
        updated_user = self.find_by_mongo_id(mongo_id)
        return updated_user 
    
    
    def get_all_users(self) -> list[UserProfile]:
        documents = self._collection.find(self._ACTIVE_USER_FILTER).sort([("authorizedAt", -1)])
        return [UserProfileMapper.from_document(doc) for doc in documents]


    def mark_users_as_saved_in_bigquery(self, users: list[UserProfile]) -> None:
        user_ids = [user.id for user in users]
        self._collection.update_many(
            {"_id": {"$in": user_ids}, **self._ACTIVE_USER_FILTER},
            {"$set": {"savedInBigQuery": True}}
        )