from src.exceptions.api_types import ValidationFailed




class LoginValidator:
    @staticmethod
    def validate(request: any) -> None:

        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Basic '):
            raise ValidationFailed("Invalid or missing Authorization header")