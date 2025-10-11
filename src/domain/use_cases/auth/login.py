from abc import ABC, abstractmethod
from src.domain.use_cases.models.auth.login_input import LoginInput
from src.domain.use_cases.models.auth.login_output import LoginOutput


class ILoginUseCase(ABC):
    @abstractmethod
    def execute(self, login: LoginInput) -> LoginOutput:
        """Realiza o login do usuário usando o token do LBC Auth e retorna os dados do usuário."""
        pass