from dataclasses import dataclass

from src.domain.entities.user_profile import UserProfile


@dataclass
class Session:
    id: str
    name: str
    email: str
    ibms: list[str]
    companies: list[dict[str, str]]
    redes: list[str]
    user_profile: UserProfile
    lbc_auth_token: str
