from dataclasses import dataclass
from typing import Sequence

from src.domain.entities.user_profile import UserProfile


@dataclass(frozen=True)
class UserPrincipal:
    email: str
    name: str

    companies: list[dict[str, str]]
    ibms: list[str]
    redes: list[str]

    can_use_ai_agent: bool = False
    can_access_sensitive_information: bool = False
    is_admin: bool = False