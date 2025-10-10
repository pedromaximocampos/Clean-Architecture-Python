from abc import ABC, abstractmethod
from src.domain.use_cases.models.user_profile.update_user_profile_input import UpdateUserProfileInput
from src.domain.use_cases.models.user_profile.update_user_profile_output import UpdateUserProfileOutput



class IUpdateUserProfile(ABC):
    """Contrato do caso de uso de atualização de UserProfile."""
    @abstractmethod
    def execute(self, update_input: UpdateUserProfileInput ) -> UpdateUserProfileOutput: pass