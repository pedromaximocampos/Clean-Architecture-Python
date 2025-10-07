from __future__ import annotations
from typing import Iterable, List, Optional

from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from src.domain.repositories_interfaces.user_profile_repository import IUserProfileRepository
from src.domain.entities.user_profile import UserProfile as UserProfileEntity
from src.infra.mongo.connection import MongoDBProvider
from src.infra.mongo.mappers.user_profile_mapper import UserProfileMapper

from src.data.shared.custom_exceptions import UniqueViolation

from src.application.shared.utils import UtilsMethods

class MongoUserProfileRepository(IUserProfileRepository):
    """
    Repositório MongoDB para UserProfile.

    Convenções:
    - Ativo: deletedAt == null
    - Índice único parcial: email unique onde deletedAt == null
    - Sempre retornar/aceitar UserProfile (domínio)
    """

    _COL_NAME = "UserProfile"
    _ACTIVE_FILTER = {"deletedAt": None}

    def __init__(self, db_provider: MongoDBProvider) -> None:
        self._col: Collection = db_provider.get_collection(self._COL_NAME)
        # Índices unico parcial
        self._col.create_index(
            [("email", 1)],
            unique=True,
            partialFilterExpression={"deletedAt": {"$eq": None}},
        )
        self._col.create_index([("authorizedAt", -1)])

    # ---------- contrato ----------
    def find_by_id(self, user_id: str) -> Optional[UserProfileEntity]:
        oid = UtilsMethods.to_oid(user_id)
        doc = self._col.find_one({"_id": oid, **self._ACTIVE_FILTER})
        return UserProfileMapper.from_document(doc) if doc else None


    def find_by_email_active(self, email: str) -> Optional[UserProfileEntity]:
        doc = self._col.find_one({"email": email, **self._ACTIVE_FILTER})
        return UserProfileMapper.from_document(doc) if doc else None


    def insert(self, user: UserProfileEntity) -> UserProfileEntity:
        doc = UserProfileMapper.to_document(user)
        try:
            res = self._col.insert_one(doc)
        except DuplicateKeyError:
            raise UniqueViolation("email", user.email)
        return self.find_by_id(str(res.inserted_id))  # estado canônico


    def save(self, user: UserProfileEntity) -> UserProfileEntity:
        if not user.id:
            raise ValueError("User must have a valid id to be saved.")
        oid = UtilsMethods.to_oid(user.id)
        doc = UserProfileMapper.to_document(user)
        try:
            self._col.update_one({"_id": oid, **self._ACTIVE_FILTER}, {"$set": doc})
        except DuplicateKeyError:
            raise UniqueViolation("email", user.email)
        return self.find_by_id(str(oid))


    def list_active(self, *, skip: int = 0, limit: int = 50) -> List[UserProfileEntity]:
        cursor = (
            self._col.find(self._ACTIVE_FILTER)
            .sort([("authorizedAt", -1)])
        )
        return [UserProfileMapper.from_document(d) for d in cursor]


    def soft_delete(self, user_id: str, *, by: str) -> None:
        oid = UtilsMethods.to_oid(user_id)
        t = UtilsMethods.now_utc()
        self._col.update_one(
            {"_id": oid, **self._ACTIVE_FILTER},
            {"$set": {"deletedAt": t, "deletedBy": by, "updatedAt": t, "updatedBy": by}},
        )


    def restore(self, user_id: str, *, by: str) -> None:
        # Pode falhar por unicidade se já houver outro ativo com o mesmo email.
        try:
            oid = UtilsMethods.to_oid(user_id)
            t = UtilsMethods.now_utc()
            self._col.update_one(
                {"_id": oid, "deletedAt": {"$ne": None}},
                {"$set": {"deletedAt": None, "deletedBy": None, "updatedAt": t, "updatedBy": by}},
            )
        except DuplicateKeyError:
            raise UniqueViolation("email", "unknown")


    def mark_as_saved_in_bigquery(self, user_ids: Iterable[str]) -> None:
        oids = [UtilsMethods.to_oid(uid) for uid in user_ids]
        if not oids:
            return
        self._col.update_many(
            {"_id": {"$in": oids}, **self._ACTIVE_FILTER},
            {"$set": {"savedInBigQuery": True}},
        )
