from abc import ABC, abstractmethod


class ITokenService(ABC):
    """Contrato do serviço de tokens (domínio não conhece JWT/Flask)."""

    @abstractmethod
    def create_access_token(self, subject: str) -> str:
        """Cria um token de acesso (curto prazo)."""
        raise NotImplementedError

    @abstractmethod
    def create_refresh_token(self, subject: str) -> str:
        """Cria um token de atualização (longo prazo)."""
        raise NotImplementedError

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        """Decodifica o token e retorna o payload."""
        raise NotImplementedError