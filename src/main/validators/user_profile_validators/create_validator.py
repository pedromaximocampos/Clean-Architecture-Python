from cerberus import Validator
from src.exceptions.api_types.validation_error import ValidationFailed



class UserProfileCreateValidator:


    @staticmethod
    def validate(request: any) -> None:
        schema = {
            "email": {
                "type": "string",
                "required": True,
                "regex": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            },
            "can_access_sensitive_information": {
                "type": "boolean",
                "required": False,
                "default": False
            },
            "can_use_ai_agent": {
                "type": "boolean",
                "required": False,
                "default": True
            },
        }

        v = Validator(schema)
        if not v.validate(request.json):
            raise ValidationFailed(f"Invalid user profile create data: {v.errors}")
