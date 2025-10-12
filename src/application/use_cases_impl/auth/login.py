from os import access

from src.domain.entities.user_profile import UserProfile
from src.domain.ports.repositories.user_profile_repository import IUserProfileRepository
from src.domain.ports.repositories.session_token_repository import ISessionTokenRepository
from src.domain.ports.repositories.admin_repository import IAdminUserRepository
from src.domain.ports.security.token_service import ITokenService

from src.domain.use_cases.auth.login import ILoginUseCase
from src.domain.use_cases.models.auth.lbc_auth_output import LBCAuthOutput
from src.domain.use_cases.models.auth.lbc_auth_input import LBCAuthInput
from src.domain.use_cases.models.auth.login_input import LoginInput
from src.domain.use_cases.models.auth.login_output import LoginOutput
from src.domain.ports.clients.lbc_auth_client import  ILBCAuthClient
from src.domain.use_cases.models.auth.session import Session

from src.exceptions.api_types import ForbiddenError

from src.config.settings import EXPIRATION_TIME_ACCESS_TOKEN, EXPIRATION_TIME_REFRESH_TOKEN

class LoginUseCaseImpl(ILoginUseCase):
    def __init__(self, user_repository: IUserProfileRepository, session_repository: ISessionTokenRepository,
                 lbc_auth_client: ILBCAuthClient, token_service: ITokenService, admin_repository: IAdminUserRepository) -> None:
        self._user_repository = user_repository
        self._session_repository = session_repository
        self._lbc_auth_client = lbc_auth_client
        self._token_service = token_service
        self._admin_repository = admin_repository


    def execute(self, login: LoginInput) -> LoginOutput:
        """Realiza o login do usuário usando o username e senha presentes no LBC Auth e retorna os dados do usuário."""

        auth_response: LBCAuthOutput  = self.return_lbc_auth_response(login)

        is_admin : bool = self._admin_repository.is_admin(auth_response.email)

        access_token, refresh_token =  self.create_tokens(auth_response.email)

        user_profile: UserProfile = self._user_repository.find_by_email_active(auth_response.email)

        if not user_profile:
            raise ForbiddenError

        session: Session = self.create_session(auth_response, user_profile)

        self._session_repository.save(session, refresh_token)


        return LoginOutput(
            access_token=access_token,
            refresh_token=refresh_token,
            email=auth_response.email,
            name=auth_response.name,
            ibms=auth_response.ibms,
            companies=auth_response.companies,
            redes=auth_response.redes,
            is_admin= is_admin,
            can_access_sensitive_information= user_profile.can_access_sensitive_information,
            can_use_ai_agent= user_profile.can_use_ai_agent,
        )




    @classmethod
    def login_input_to_lbc_auth_input(cls, login: LoginInput) -> LBCAuthInput:
        return LBCAuthInput(
            email=login.email,
            password=login.password
        )


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

    def return_lbc_auth_response(self, login: LoginInput) -> LBCAuthOutput:
        """Retorna a resposta do LBC Auth para o login fornecido."""
        lbc_auth_input: LBCAuthInput = self.login_input_to_lbc_auth_input(login)

        auth_response: LBCAuthOutput  = self._lbc_auth_client.authenticate(lbc_auth_input)

        return auth_response

    def create_tokens(self, email: str) -> tuple[str, str]:
        """Cria novos tokens de acesso e refresh."""
        access_token = self._token_service.create_token(email, EXPIRATION_TIME_ACCESS_TOKEN)  # 15 minutos
        refresh_token = self._token_service.create_token(email, EXPIRATION_TIME_REFRESH_TOKEN)  # 30 dias

        return access_token, refresh_token