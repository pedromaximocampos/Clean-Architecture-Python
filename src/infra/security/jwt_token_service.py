from src.domain.ports.security.token_service import ITokenService
import jwt

import uuid
from datetime import datetime, timezone, timedelta

from hashlib import sha256

from src.exceptions.api_types import AuthError


class JWTTokenService(ITokenService):

    def __init__(self, jwt_secret: str) -> None:
        self._jwt_secret = jwt_secret


    def create_access_token(self, subject: str) -> str:
        salt = self.get_salt_token(subject)

        payload = {
            "sub": subject,
            "jti": salt,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30), # Token válido por 15 minutos
            "iss": "gmon-service",
        }
        token = jwt.encode(payload, self._jwt_secret, algorithm="HS256")

        return token

    def create_refresh_token(self, subject: str) -> str:
        salt = self.get_salt_token(subject)

        payload = {
            "sub": subject,
            "jti": salt,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(days=30),  # Token válido por 30 dias
            "iss": "gmon-service",
        }
        token = jwt.encode(payload, self._jwt_secret, algorithm="HS256")

        return token

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                self._jwt_secret,
                algorithms=["HS256"],
                options={
                    "verify_exp": True,
                    "verify_iat": True,
                    "require": ["exp", "iat", "sub", "jti", "iss"]
                }
            )

        except Exception as e:
            raise AuthError("Token inválido ou expirado.") from e


    @classmethod
    def get_salt_token(cls, subject: str) -> str:
        """Gera um salt único para o token."""
        unique_id = str(uuid.uuid4())
        timestamp = str(int(datetime.now(timezone.utc).timestamp()))

        unique_id = sha256(
            f"{subject}:{unique_id}:{timestamp}:".encode()
        ).hexdigest()

        return unique_id