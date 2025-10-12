from src.domain.ports.repositories.admin_repository import IAdminUserRepository
from src.domain.ports.repositories.session_token_repository import ISessionTokenRepository
from src.domain.ports.security.token_service import ITokenService
from src.domain.ports.security.auth_guard import IAuthGuard
from src.domain.ports.security.models.user_principal import UserPrincipal
from src.domain.use_cases.models.auth.session import Session
from src.exceptions.api_types import AuthError


class AuthGuardImpl(IAuthGuard):

    def __init__(self, tokens: ITokenService, sessions: ISessionTokenRepository, admin_repository: IAdminUserRepository) -> None:
        self.tokens_service = tokens
        self.sessions_repository = sessions
        self.admin_repository = admin_repository

    def authenticate(self, access_token: str, refresh_token: str) -> UserPrincipal:

        user_email = self.tokens_service.get_email_from_token(access_token)

        try:
            session: Session = self.sessions_repository.get_user_info(refresh_token)
        except Exception:
            raise AuthError

        is_admin = self.admin_repository.is_admin(user_email)

        principal = UserPrincipal(email=session.email, name=session.name, ibms=session.ibms,
                                    companies=session.companies, redes=session.redes, can_use_ai_agent= session.user_profile.can_use_ai_agent,
                                    can_access_sensitive_information= session.user_profile.can_access_sensitive_information,
                                    is_admin=is_admin)

        return principal


    def validate(self, user: UserPrincipal, requiered_field: bool = False) -> None:
        pass