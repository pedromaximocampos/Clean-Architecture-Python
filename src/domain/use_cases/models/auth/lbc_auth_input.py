from dataclasses import dataclass


@dataclass(frozen=True)
class LBCAuthInput:
    email: str
    password: str