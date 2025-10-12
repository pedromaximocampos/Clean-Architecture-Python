from src.domain.use_cases.auth.login import ILoginUseCase
from src.domain.use_cases.models.auth.login_input import LoginInput
from src.domain.use_cases.models.auth.login_output import LoginOutput
from src.presentation.http_types import HttpRequest, HttpResponse
from src.presentation.interfaces.controller_interface import IControllerInterface
from basicauth import decode, encode

from src.exceptions.api_types import BadRequestError


class LoginController(IControllerInterface):

    def __init__(self, login_use_case: ILoginUseCase):
        self.login_use_case = login_use_case

    def handle_request(self, request: HttpRequest) -> HttpResponse:
        authorization_header = request.headers.get('Authorization')

        username, password = self._decode_basic_auth(authorization_header)

        login_input = LoginInput(username, password)

        login_output: LoginOutput = self.login_use_case.execute(login_input)

        return HttpResponse(
            status_code=200,
            body= {
                "token": login_output.access_token,
                "user": {
                        "name": login_output.name,
                        "email": login_output.email,
                        "is_admin": login_output.is_admin
                },
                "redes": login_output.redes,
                "companies": login_output.companies,
                "ibms": login_output.ibms,
                "is_admin": login_output.is_admin
                },
            headers={"refresh-token": login_output.refresh_token}
        )


    @classmethod
    def _decode_basic_auth(cls, authorization_header: str) -> tuple[str, str]:
        username, password = decode(authorization_header)

        if username is None or password is None:
            raise BadRequestError("Credenciais inválidas")

        return username, password
