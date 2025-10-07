
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from src.domain.ports.user_profile_repository import IUserProfileRepository
from src.domain.use_cases.models.create_user_profile_input import CreateUserProfileInput
from src.domain.use_cases.models.create_user_profile_output import CreateUserProfileOutput



class ICreateUserProfile(ABC):
    """Contrato do caso de uso de criação de UserProfile."""
    @abstractmethod
    def execute(self, user_data_input: CreateUserProfileInput) -> CreateUserProfileOutput: pass