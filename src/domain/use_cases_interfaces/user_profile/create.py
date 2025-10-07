
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from src.domain.repositories_interfaces.user_profile_repository import IUserProfileRepository


@dataclass
class CreateUserProfileInput:
    email: str
    can_access_sensitive_information: bool
    can_use_ai_agent: bool


@dataclass
class CreateUserProfileOutput:
    id: str
    email: str
    can_access_sensitive_information: bool
    can_use_ai_agent: bool
    saved_in_big_query: bool
    authorized_by: str
    authorized_at: datetime
    updated_by: str = None
    updated_at: datetime = None


class ICreateUserProfile(ABC):
    """Contrato do caso de uso de criação de UserProfile."""
    @abstractmethod
    def execute(self, user_data_input: CreateUserProfileInput) -> CreateUserProfileOutput: pass