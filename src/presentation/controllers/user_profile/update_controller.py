from src.domain.use_cases.user_profile.update import IUpdateUserProfile
from src.domain.use_cases.models.user_profile.update_user_profile_input import UpdateUserProfileInput
from src.domain.use_cases.models.user_profile.update_user_profile_output import UpdateUserProfileOutput

from src.presentation.http_types import HttpRequest, HttpResponse
from src.presentation.interfaces import IControllerInterface


class UpdateUserProfileController(IControllerInterface):


    def __init__(self, update_user_profile_use_case: IUpdateUserProfile):
        self.update_user_profile_use_case = update_user_profile_use_case


    def handle_request(self, request: HttpRequest) -> HttpResponse:
        update_user_profile_input = self.update_user_profile_input_from_dict(request.body)

        updated_user_profile = self.update_user_profile_use_case.execute(update_user_profile_input)


        return HttpResponse(
            status_code=200,
            body={
                "data": self.return_user_output_as_dict(updated_user_profile)
            }
        )


    @classmethod
    def update_user_profile_input_from_dict(cls, data: dict):
        return UpdateUserProfileInput(
            user_id=data['user_id'],
            can_access_sensitive_information=data['can_access_sensitive_information'],
            can_use_ai_agent=data['can_use_ai_agent']
        )

    @classmethod
    def return_user_output_as_dict(cls, user_profile_output: UpdateUserProfileOutput):
        return {
            'id': user_profile_output.id,
            'email': user_profile_output.email,
            'can_access_sensitive_information': user_profile_output.can_access_sensitive_information,
            'can_use_ai_agent': user_profile_output.can_use_ai_agent,
            'saved_in_big_query': user_profile_output.saved_in_big_query,
            'authorized_by': user_profile_output.authorized_by,
            'authorized_at': user_profile_output.authorized_at.isoformat() if user_profile_output.authorized_at else None,
            'updated_by': user_profile_output.updated_by,
            'updated_at': user_profile_output.updated_at.isoformat() if user_profile_output.updated_at else None
        }