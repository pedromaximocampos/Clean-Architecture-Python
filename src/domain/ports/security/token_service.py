from abc import ABC, abstractmethod


class ITokenService(ABC):
    """Contrato do serviço de tokens (domínio não conhece JWT/Flask)."""

    @abstractmethod
    def create_token(self, subject: str, expiration_time: int) -> str:
        """Cria um token de acesso (curto prazo)."""
        raise NotImplementedError

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        """Decodifica o token e retorna o payload."""
        raise NotImplementedError


    @abstractmethod
    def get_email_from_token(self, token: str) -> str:
        """Extrai o email do token decodificado."""
        raise NotImplementedError
