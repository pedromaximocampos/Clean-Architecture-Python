from src.domain.ports.security.models.user_principal import UserPrincipal
from src.domain.use_cases.auth.refresh import IAuthRefreshUseCase
from src.domain.use_cases.models.auth.refresh_input import RefreshInput
from src.domain.use_cases.models.auth.refresh_output import RefreshOutput
from src.presentation.http_types import HttpRequest, HttpResponse
from src.presentation.interfaces import IControllerInterface


from src.exceptions.api_types import BadRequestError

from src.shared.contexts.current_user import get_current_user


class RefreshController(IControllerInterface):


    def __init__(self, refresh_use_case: IAuthRefreshUseCase):
        self.refresh_use_case = refresh_use_case

    def handle_request(self, request: HttpRequest) -> HttpResponse:

        refresh_token = request.refresh_token
        if not refresh_token:
            raise BadRequestError("Refresh Token is missing")

        logged_user: UserPrincipal = get_current_user()

        if not logged_user:
            raise BadRequestError("Error getting current user")

        refresh_input = RefreshInput(logged_user.email, refresh_token)

        refresh_output: RefreshOutput = self.refresh_use_case.execute(refresh_input)

        return HttpResponse(
            status_code=200,
            body={
                "token": refresh_output.access_token,
                "user": {
                    "name": refresh_output.name,
                    "email": refresh_output.email,
                    "is_admin": refresh_output.is_admin,
                    "can_access_sensitive_information": refresh_output.can_access_sensitive_information,
                    "can_use_ai_agent": refresh_output.can_use_ai_agent
                },
                "redes": refresh_output.redes,
                "companies": refresh_output.companies,
                "ibms": refresh_output.ibms
            },
            headers={"refresh-token": refresh_output.refresh_token}
        )