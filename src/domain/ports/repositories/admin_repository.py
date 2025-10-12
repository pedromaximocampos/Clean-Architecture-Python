from abc import ABC, abstractmethod



class IAdminUserRepository(ABC):
    @abstractmethod
    def is_admin(self, user_email: str) -> bool:
        """Verifica se o usuário é um administrador."""
        pass