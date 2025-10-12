from src.domain.use_cases.auth.refresh import IAuthRefreshUseCase
from src.domain.ports.repositories.admin_repository import IAdminUserRepository
from src.domain.ports.repositories.session_token_repository import ISessionTokenRepository
from src.domain.ports.security.token_service import ITokenService
from src.domain.ports.repositories.user_profile_repository import IUserProfileRepository
from src.domain.ports.clients.lbc_auth_client import ILBCAuthClient
from src.domain.use_cases.models.auth.lbc_auth_input import LBCAuthInput
from src.domain.use_cases.models.auth.lbc_auth_output import LBCAuthOutput
from src.domain.use_cases.models.auth.refresh_input import RefreshInput
from src.domain.use_cases.models.auth.refresh_output import RefreshOutput
from src.domain.entities.user_profile import UserProfile
from src.domain.use_cases.models.auth.session import Session

from src.exceptions.api_types import AuthError, ForbiddenError

from src.config.settings import EXPIRATION_TIME_ACCESS_TOKEN, EXPIRATION_TIME_REFRESH_TOKEN

class AuthRefreshUseCase(IAuthRefreshUseCase):

    def __init__(self, user_repository: IUserProfileRepository, session_repository: ISessionTokenRepository,
                 lbc_auth_client: ILBCAuthClient, token_service: ITokenService, admin_repository: IAdminUserRepository) -> None:
        self._user_repository = user_repository
        self._session_repository = session_repository
        self._lbc_auth_client = lbc_auth_client
        self._token_service = token_service
        self._admin_repository = admin_repository

    def execute(self, refresh: RefreshInput) -> RefreshOutput:
        """Realiza o refresh do token de autenticação e retorna um novo token e informações de usuário atualizadas"""

        email, user_profile = self.validate_token_outside(refresh.refresh_token)

        old_session: Session = self._session_repository.get_user_info(refresh.refresh_token)

        lbc_auth_response: LBCAuthOutput = self.get_lbc_auth_response(email, old_session.lbc_auth_token)

        is_admin = self._admin_repository.is_admin(lbc_auth_response.email)

        new_access_token, new_refresh_token = self.create_tokens(email)

        new_session: Session = self.create_session(lbc_auth_response, user_profile)

        self._session_repository.save(new_session, new_refresh_token)

        return RefreshOutput(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            email=lbc_auth_response.email,
            name=lbc_auth_response.name,
            ibms=lbc_auth_response.ibms,
            companies=lbc_auth_response.companies,
            redes=lbc_auth_response.redes,
            is_admin=is_admin,
            can_access_sensitive_information=user_profile.can_access_sensitive_information,
            can_use_ai_agent=user_profile.can_use_ai_agent
        )


    def validate_token_outside(self, refresh_token: str) -> tuple[str, UserProfile]:
        """Valida o token de refresh sem retornar novos tokens."""
        email = self._token_service.get_email_from_token(refresh_token)

        if not email:
            raise AuthError

        token_exists = self._session_repository.exists(refresh_token)

        if not token_exists:
            raise AuthError

        user_profile: UserProfile = self._user_repository.find_by_email_active(email)

        if not user_profile:
            raise ForbiddenError


        return email, user_profile

    def get_lbc_auth_response(self, email: str, lbc_auth_token: str) -> LBCAuthOutput:
        """Obtém a resposta de autenticação do LBC Auth."""

        lbc_auth_input = LBCAuthInput(email, lbc_auth_token)

        lbc_auth_response: LBCAuthOutput = self._lbc_auth_client.authenticate(lbc_auth_input)


        return lbc_auth_response


    def create_tokens(self, email: str) -> tuple[str, str]:
        """Cria novos tokens de acesso e refresh."""
        new_access_token = self._token_service.create_token(email, EXPIRATION_TIME_ACCESS_TOKEN)  # 15 minutos
        new_refresh_token = self._token_service.create_token(email, EXPIRATION_TIME_REFRESH_TOKEN)  # 30 dias

        return new_access_token, new_refresh_token


    def replace_sessions(self, old_refresh_token: str, new_refresh_token: str, new_session: Session) -> None:
        """Substitui o token de sessão antigo pelo novo."""

        self._session_repository.delete(old_refresh_token)

        self._session_repository.save(new_session, new_refresh_token)


    @classmethod
    def create_session(cls, auth_response: LBCAuthOutput, user_profile: UserProfile) -> Session:
        return Session(
            id=user_profile.id,
            name=auth_response.name,
            email=auth_response.email,
            ibms=auth_response.ibms,
            companies=auth_response.companies,
            redes=auth_response.redes,
            user_profile=user_profile,
            lbc_auth_token=auth_response.lbc_auth_token
        )