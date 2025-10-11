from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class LBCAuthOutput:
    lbc_auth_token: str
    email: str
    name : Optional[str] = None
    companies: Optional[list[dict[str, str]]] = None
    ibms: Optional[list[str]] = None
    redes: Optional[list[str]] = None