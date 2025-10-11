from abc import ABC, abstractmethod
from src.domain.use_cases.models.auth.lbc_auth_input import LBCAuthInput
from src.domain.use_cases.models.auth.lbc_auth_output import LBCAuthOutput



class ILBCAuthClient(ABC):
    """Interface para o cliente de autenticação LBC."""
    @abstractmethod
    def authenticate(self, auth_input: LBCAuthInput) -> LBCAuthOutput: pass