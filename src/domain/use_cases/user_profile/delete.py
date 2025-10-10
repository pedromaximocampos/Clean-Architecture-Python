from abc import ABC, abstractmethod


class IDeleteUserProfile(ABC):
    """Contrato do caso de uso de remoção de UserProfile."""
    @abstractmethod
    def execute(self, user_profile_id: str) -> str: pass