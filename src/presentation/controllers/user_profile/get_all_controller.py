
from dataclasses import asdict
from src.presentation.interfaces.controller_interface import IControllerInterface
from src.domain.use_cases.user_profile.get_all import IGetAllUserProfiles

from src.presentation.http_types import HttpRequest, HttpResponse


class GetAllUserProfilesController(IControllerInterface):
    """Controlador para o caso de uso de listagem de todos os UserProfiles."""
    def __init__(self, get_all_user_profiles_use_case: IGetAllUserProfiles) -> None:
        self.get_all_user_profiles_use_case = get_all_user_profiles_use_case

    def handle_request(self, request: HttpRequest) -> HttpResponse:
        user_profiles = self.get_all_user_profiles_use_case.execute()

        users = [asdict(user_profile) for user_profile in user_profiles]

        return HttpResponse(
            status_code=200,
            body={
                "data": users
            }
        )