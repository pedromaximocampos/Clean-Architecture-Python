from typing import Iterable, List, Optional
from uuid import uuid4
from src.domain.entities.user_profile import UserProfile as UserProfileEntity, UserProfile
from src.domain.repositories.user_profile_repository import IUserProfileRepository


class MongoUserProfileRepositorySpy(IUserProfileRepository):
    def __init__(self):
        self.calls = []
        self.atributes = {}
        self.last_saved: Optional[UserProfile] = None

    def _next_id(self) -> str:
        # 24 hex chars como ObjectId
        return uuid4().hex[:24]

    def find_by_email_active(self, email: str) -> Optional[UserProfile]:
        pass

    def find_by_id(self, user_id: str) -> Optional[UserProfile]:
        pass

    def save(self, user: UserProfile) -> UserProfile:
        pass

    def list_active(self, *, skip: int = 0, limit: int = 50) -> List[UserProfile]:
        pass

    def soft_delete(self, user_id: str, *, by: str) -> None:
        pass

    def restore(self, user_id: str, *, by: str) -> None:
        pass

    def mark_as_saved_in_bigquery(self, user_ids: Iterable[str]) -> None:
        pass

    def insert(self, user_profile: UserProfileEntity) -> UserProfileEntity:

        inserted_user = UserProfile(
            email=user_profile.email,
            can_access_sensitive_information=user_profile.can_access_sensitive_information,
            can_use_ai_agent=user_profile.can_use_ai_agent,
            authorized_by=user_profile.authorized_by,
            authorized_at=user_profile.authorized_at,
            id=self._next_id()
        )

        self.calls.append(('insert', inserted_user))
        # Simulate inserting and returning the user profile with an ID
        self.last_saved = inserted_user

        return self.last_saved