from abc import ABC, abstractmethod
from src.domain.use_cases.models.auth.session import Session

class ISessionTokenRepository(ABC):
    """Contrato do repositório de SessionToken (domínio não conhece Redis/Flask)."""

    @abstractmethod
    def save(self, session: Session, token_refresh: str) -> None:
        """Insere token de sessão para o usuário."""
        raise NotImplementedError

    @abstractmethod
    def exists(self, token_refresh: str) -> bool:
        """Verifica se o token de sessão existe para o usuário."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, token_refresh: str) -> None:
        """Deleta o token de sessão do usuário."""
        raise NotImplementedError


    @abstractmethod
    def get_user_info(self, token_refresh: str) -> Session:
        """Retorna as informações da sessão associada ao token de sessão."""
        raise NotImplementedError

