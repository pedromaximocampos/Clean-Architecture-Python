from src.exceptions.api_types import ValidationFailed




class RefreshValidator:
    @staticmethod
    def validate(request: any) -> None:

        refresh_token = request.cookies.get("refresh-token")

        if not refresh_token:
            raise ValidationFailed("Missing refresh token in cookies")