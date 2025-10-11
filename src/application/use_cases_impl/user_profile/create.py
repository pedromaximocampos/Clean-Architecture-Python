from src.domain.use_cases.user_profile.create import ICreateUserProfile
from src.domain.use_cases.models.user_profile.create_user_profile_output import CreateUserProfileOutput
from src.domain.use_cases.models.user_profile.create_user_profile_input import CreateUserProfileInput
from src.domain.entities.user_profile import UserProfile
from src.exceptions.custom_exceptions import UniqueViolation
from src.exceptions.api_types import BadRequestError
from src.domain.ports.repositories.user_profile_repository import IUserProfileRepository


class CreateUserProfileUseCase(ICreateUserProfile):

    def __init__(self, user_repository: IUserProfileRepository):
        self.user_profile_repository = user_repository

    def execute(self, userDataInput: CreateUserProfileInput) -> CreateUserProfileOutput:
        # Business logic for creating a user profile

        new_user_profile: UserProfile = self._create_user_profile_entity(userDataInput)

        authorized_user: UserProfile = new_user_profile.authorize("system")  # Exemplo: sistema autoriza

        try:

            user_profile = self.user_profile_repository.insert(authorized_user)

        except UniqueViolation as e:
            raise BadRequestError(f"Não é possível criar o perfil do usuário. com email {userDataInput.email}."
                             f" Usuário já ativo no sistema") from e

        user_profile_output: CreateUserProfileOutput = self._create_user_profile_output(user_profile)

        return user_profile_output


    @classmethod
    def _create_user_profile_entity(cls, userDataInput: CreateUserProfileInput) -> UserProfile:
        return UserProfile(
            id = None,
            email=userDataInput.email,
            can_access_sensitive_information=userDataInput.can_access_sensitive_information,
            can_use_ai_agent=userDataInput.can_use_ai_agent,
        )


    @classmethod
    def _create_user_profile_output(cls, user_profile: UserProfile) -> CreateUserProfileOutput:
        return CreateUserProfileOutput(
            id = user_profile.id,
            email= user_profile.email,
            can_access_sensitive_information= user_profile.can_access_sensitive_information,
            can_use_ai_agent= user_profile.can_use_ai_agent,
            saved_in_big_query= user_profile.saved_in_big_query,
            authorized_by= user_profile.authorized_by,
            authorized_at= user_profile.authorized_at,
        )