from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interfaces.controller_interface import IControllerInterface
from src.domain.use_cases_interfaces.user_profile.create import ICreateUserProfile
from src.domain.use_cases_interfaces.user_profile.create import CreateUserProfileInput, CreateUserProfileOutput


class CreateUserProfileController(IControllerInterface):
    def __init__(self, create_user_profile_use_case: ICreateUserProfile):
        self.create_user_profile_use_case = create_user_profile_use_case

    def handle_request(self, request: HttpRequest) -> HttpResponse:
        user_profile_input = self.create_user_profile_input_from_dict(request.body)
        created_user_profile = self.create_user_profile_use_case.execute(user_profile_input)


        return HttpResponse(
            status_code=201,
            body={
                "data": self.return_user_output_as_dict(created_user_profile)
            }
        )

    @classmethod
    def create_user_profile_input_from_dict(cls, data: dict):

        return CreateUserProfileInput(
            email=data['email'],
            can_access_sensitive_information=data['can_access_sensitive_information'],
            can_use_ai_agent=data['can_use_ai_agent']
        )


    @classmethod
    def return_user_output_as_dict(cls, user_profile_output: CreateUserProfileOutput):
        return {
            'id': user_profile_output.id,
            'email': user_profile_output.email,
            'can_access_sensitive_information': user_profile_output.can_access_sensitive_information,
            'can_use_ai_agent': user_profile_output.can_use_ai_agent,
            'saved_in_big_query': user_profile_output.saved_in_big_query,
            'authorized_by': user_profile_output.authorized_by,
            'authorized_at': user_profile_output.authorized_at.isoformat(),
            'updated_by': user_profile_output.updated_by,
            'updated_at': user_profile_output.updated_at.isoformat() if user_profile_output.updated_at else None
        }