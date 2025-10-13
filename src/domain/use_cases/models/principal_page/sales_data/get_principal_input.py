from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class GetPrincipalInput:
    ibms: list[str]
    rede: list[str]
    date: datetime
