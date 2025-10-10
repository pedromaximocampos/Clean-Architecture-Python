from cerberus import Validator
from src.exceptions.api_types import ValidationFailed

class UserProfileUpdateValidator:

    @staticmethod
    def validate(request: any) -> None:

        schema = {
            'user_id': {'type': 'string', 'required': True, 'empty': False},
            'can_access_sensitive_information': {'type': 'boolean', 'required': True},
            'can_use_ai_agent': {'type': 'boolean', 'required': True}
        }

        v = Validator(schema)
        if not v.validate(request):
            raise ValidationFailed(f"Invalid request data: {v.errors}")