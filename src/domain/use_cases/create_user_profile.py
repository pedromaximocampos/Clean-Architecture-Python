
from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.domain.repositories.user_profile_repository import IUserProfileRepository
from typing import Dictf


@dataclass
class CreateUserProfileInput:
    email: str
    canAccessSensitiveInformation: bool
    canUseAiAgent: bool


@dataclass
class CreateUserProfileOutput:
    email: str
    canAccessSensitiveInformation: bool
    canUseAiAgent: bool
    savedInBigQuery: bool
    authorizedBy: str
    authorizedAt: str
    updatedBy: str = None
    updatedAt: str = None


class ICreateUserProfile(ABC):
    
    def __init__(self, user_repository: IUserProfileRepository) -> None:
        self._user_repository = user_repository
    
    def execute(self, user_data_input: CreateUserProfileInput) -> CreateUserProfileOutput: pass