from src.domain.use_cases.user_profile.create import ICreateUserProfile, CreateUserProfileOutput, CreateUserProfileInput
from src.domain.entities.user_profile import UserProfile
from src.shared.custom_exceptions import UniqueViolation
from src.api.advices.apiError import BadRequest
from src.domain.repositories.user_profile_repository import IUserProfileRepository

class CreateUserProfileUseCase(ICreateUserProfile):

    def __init__(self, user_repository: IUserProfileRepository):
        self.user_profile_repository = user_repository

    def execute(self, userDataInput: CreateUserProfileInput) -> CreateUserProfileOutput:
        # Business logic for creating a user profile
        try:
            new_user_profile = UserProfile(
                id = None,
                email=userDataInput.email,
                can_access_sensitive_information=userDataInput.can_access_sensitive_information,
                can_use_ai_agent=userDataInput.can_use_ai_agent,
            )

            user_profile = self.user_profile_repository.insert(new_user_profile)
        except UniqueViolation as e:
            raise BadRequest(f"Não é possível criar o perfil do usuário. com email {userDataInput.email}."
                             f" Usuário já ativo no sistema") from e

        created_output = CreateUserProfileOutput(
            id = user_profile.id,
            email=user_profile.email,
            can_access_sensitive_information=user_profile.can_access_sensitive_information,
            can_use_ai_agent=user_profile.can_use_ai_agent,
            saved_in_big_query=user_profile.saved_in_big_query,
            authorized_by=user_profile.authorized_by,
            authorized_at=user_profile.authorized_at,
            updated_by=user_profile.updated_by,
            updated_at=user_profile.updated_at
        )
        return created_output