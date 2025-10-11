from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class LoginInput:
    email: str
    password: str
    device: Optional[str] = None