from dataclasses import dataclass


@dataclass(frozen=True)
class RefreshInput:
    refresh_token: str
    user_email: str