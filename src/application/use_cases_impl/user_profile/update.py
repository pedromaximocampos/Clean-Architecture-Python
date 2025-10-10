from src.domain.use_cases.user_profile.update import IUpdateUserProfile
from src.domain.use_cases.models.user_profile.update_user_profile_input import UpdateUserProfileInput
from src.domain.use_cases.models.user_profile.update_user_profile_output import UpdateUserProfileOutput
from src.domain.ports.user_profile_repository import IUserProfileRepository
from src.domain.entities.user_profile import UserProfile

from src.exceptions.api_types import NotFoundError


class UpdateUserProfileUseCase(IUpdateUserProfile):
    def __init__(self, user_repository: IUserProfileRepository):
        self.user_repository = user_repository

    def execute(self, update_data:  UpdateUserProfileInput) -> UpdateUserProfileOutput:
        user_profile: UserProfile = self.user_repository.find_by_id(update_data.user_id)
        if not user_profile:
            raise NotFoundError(f"User with id:{update_data.user_id} not found")

        updated_user = user_profile.update(by="system", can_access_sensitive_information=update_data.can_access_sensitive_information, can_use_ai_agent=update_data.can_use_ai_agent)

        self.user_repository.save(updated_user)

        return self._create_update_user_profile_output(updated_user)


    @classmethod
    def _create_update_user_profile_output(cls, user_profile: UserProfile) -> UpdateUserProfileOutput:
        return UpdateUserProfileOutput(
            id=user_profile.id,
            email=user_profile.email,
            can_access_sensitive_information=user_profile.can_access_sensitive_information,
            can_use_ai_agent=user_profile.can_use_ai_agent,
            saved_in_big_query=user_profile.saved_in_big_query,
            authorized_by=user_profile.authorized_by,
            authorized_at=user_profile.authorized_at,
            updated_by=user_profile.updated_by,
            updated_at=user_profile.updated_at
        )