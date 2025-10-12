from abc import ABC, abstractmethod

from src.domain.ports.security.models.user_principal import UserPrincipal



class IAuthGuard(ABC):

    @abstractmethod
    def authenticate(self, access_token: str, refresh_token: str) -> UserPrincipal:
        """Verifica se o token de autenticação é válido."""
        pass


    @abstractmethod
    def validate(self, user: UserPrincipal, requiered_field: bool = False) -> None:
        """Valida se o usuário tem permissão para acessar o recurso."""
        pass