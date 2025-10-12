from abc import ABC, abstractmethod

from src.domain.use_cases.models.auth.refresh_input import RefreshInput
from src.domain.use_cases.models.auth.refresh_output import RefreshOutput

class IAuthRefreshUseCase(ABC):
    @abstractmethod
    def execute(self, refresh: RefreshInput) -> RefreshOutput:
        """Realiza o refresh do token de autenticação e retorna um novo token."""
        pass