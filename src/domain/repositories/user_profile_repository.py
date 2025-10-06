from abc import ABC, abstractmethod
from typing import Optional, List, Iterable
from src.domain.entities.user_profile import UserProfile

class IUserProfileRepository(ABC):
    """Contrato do repositório de UserProfile (domínio não conhece Mongo/Flask)."""

    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[UserProfile]:
        """Retorna usuário ativo por id ou None."""
        raise NotImplementedError

    @abstractmethod
    def find_by_email_active(self, email: str) -> Optional[UserProfile]:
        """Retorna usuário ativo por email ou None."""
        raise NotImplementedError

    @abstractmethod
    def insert(self, user: UserProfile) -> UserProfile:
        """Insere e retorna o usuário salvo (estado canônico)."""
        raise NotImplementedError

    @abstractmethod
    def save(self, user: UserProfile) -> UserProfile:
        """Atualiza (somente se ativo) e retorna o usuário salvo."""
        raise NotImplementedError

    @abstractmethod
    def list_active(self, *, skip: int = 0, limit: int = 50) -> List[UserProfile]:
        """Lista usuários ativos paginados."""
        raise NotImplementedError

    @abstractmethod
    def soft_delete(self, user_id: str, *, by: str) -> None:
        """Marca deletedAt/deletedBy mantendo o doc (soft delete)."""
        raise NotImplementedError

    @abstractmethod
    def restore(self, user_id: str, *, by: str) -> None:
        """Restaura (deletedAt=None/deletedBy=None). Pode falhar por unicidade de email."""
        raise NotImplementedError

    @abstractmethod
    def mark_as_saved_in_bigquery(self, user_ids: Iterable[str]) -> None:
        """Marca flag savedInBigQuery=True para ids ativos."""
        raise NotImplementedError