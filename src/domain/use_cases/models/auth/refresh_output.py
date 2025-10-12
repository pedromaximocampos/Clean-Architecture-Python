from dataclasses import dataclass


@dataclass
class RefreshOutput:
    access_token: str
    refresh_token: str

    email: str
    name: str

    companies: list[dict[str, str]]
    ibms: list[str]
    redes: list[str]

    is_admin: bool = False
    can_access_sensitive_information: bool = False
    can_use_ai_agent: bool = False