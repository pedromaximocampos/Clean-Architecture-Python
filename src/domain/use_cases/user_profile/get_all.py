from dataclasses import dataclass
from abc import ABC, abstractmethod

from src.domain.entities.user_profile import UserProfile


class IGetAllUserProfiles(ABC):
    """Contrato do caso de uso de listagem de todos os UserProfiles."""
    @abstractmethod
    def execute(self) -> list[UserProfile]: pass