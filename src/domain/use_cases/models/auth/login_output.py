from dataclasses import dataclass
from typing import Optional


@dataclass
class LoginOutput:
    access_token: str
    refresh_token: str

    email: str
    name: str

    companies: list[dict[str, str]]
    ibms: list[str]
    redes: list[str]

    is_admin: bool = False