from dataclasses import dataclass

@dataclass
class UpdateUserProfileInput:
    user_id: str
    can_access_sensitive_information: bool
    can_use_ai_agent: bool
