
from dataclasses import dataclass
from datetime import datetime
from typing import Optional



@dataclass
class GetUserProfileOutput:
    id: str
    email: str
    can_access_sensitive_information: bool
    can_use_ai_agent: bool
    authorized_at: datetime
    authorized_by: str
    saved_in_big_query: bool
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None