from dataclasses import dataclass
from datetime import datetime

@dataclass
class CreateUserProfileOutput:
    id: str
    email: str
    can_access_sensitive_information: bool
    can_use_ai_agent: bool
    saved_in_big_query: bool
    authorized_by: str
    authorized_at: datetime
