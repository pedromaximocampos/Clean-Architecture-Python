from os import access

from src.domain.entities.user_profile import UserProfile
from src.domain.ports.repositories.user_profile_repository import IUserProfileRepository
from src.domain.ports.repositories.session_token_repository import ISessionTokenRepository
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
                 lbc_auth_client: ILBCAuthClient, token_service: ITokenService):
        self._user_repository = user_repository
        self._session_repository = session_repository
        self._lbc_auth_client = lbc_auth_client
        self._token_service = token_service


    def execute(self, login: LoginInput) -> LoginOutput:
        """Realiza o login do usuário usando o username e password presentes no LBC Auth e retorna os dados do usuário."""

        lbc_auth_input: LBCAuthInput = self.login_input_to_lbc_auth_input(login)

        auth_response: LBCAuthOutput  = self._lbc_auth_client.authenticate(lbc_auth_input)

        access_token =  self._token_service.create_token(auth_response.email, EXPIRATION_TIME_ACCESS_TOKEN)

        refresh_token = self._token_service.create_token(auth_response.email, EXPIRATION_TIME_REFRESH_TOKEN)

        user_profile: UserProfile = self._user_repository.find_by_email_active(auth_response.email)

        if not user_profile:
            raise ForbiddenError

        session: Session = self.create_session(auth_response, user_profile)

        self._session_repository.save(session, refresh_token)

        # TODO:  verificar se é admin na outra collection

        return LoginOutput(
            access_token=access_token,
            refresh_token=refresh_token,
            email=auth_response.email,
            name=auth_response.name,
            ibms=auth_response.ibms,
            companies=auth_response.companies,
            redes=auth_response.redes,
            is_admin= True,
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