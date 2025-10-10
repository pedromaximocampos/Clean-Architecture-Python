
from abc import ABC, abstractmethod
from src.domain.use_cases.models.user_profile.create_user_profile_input import CreateUserProfileInput
from src.domain.use_cases.models.user_profile.create_user_profile_output import CreateUserProfileOutput



class ICreateUserProfile(ABC):
    """Contrato do caso de uso de criação de UserProfile."""
    @abstractmethod
    def execute(self, user_data_input: CreateUserProfileInput) -> CreateUserProfileOutput: pass