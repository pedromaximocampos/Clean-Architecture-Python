from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interfaces.controller_interface import IControllerInterface
from src.domain.use_cases.user_profile.delete import IDeleteUserProfile


class DeleteUserProfileController(IControllerInterface):
    def __init__(self, delete_user_profile_use_case: IDeleteUserProfile):
        self.delete_user_profile_use_case = delete_user_profile_use_case

    def handle_request(self, request: HttpRequest) -> HttpResponse:
        user_profile_id = request.query_params.get('user_id')
        result_message = self.delete_user_profile_use_case.execute(user_profile_id)

        return HttpResponse(
            status_code=200,
            body={
                "message": result_message
            }
        )