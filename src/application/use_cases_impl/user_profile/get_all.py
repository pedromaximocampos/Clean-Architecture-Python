from src.domain.use_cases.user_profile.get_all import IGetAllUserProfiles
from src.domain.ports.repositories.user_profile_repository import IUserProfileRepository

from src.domain.use_cases.models.user_profile.get_all_output import GetUserProfileOutput
from src.domain.entities.user_profile import UserProfile


class GetAllUserProfilesUseCase(IGetAllUserProfiles):
    """Implementação do caso de uso de listagem de todos os UserProfiles."""
    def __init__(self, user_profile_repository: IUserProfileRepository) -> None:
        self.user_profile_repository = user_profile_repository

    def execute(self) -> list[GetUserProfileOutput]:

        list_to_return : list[GetUserProfileOutput] = []

        users_profiles : list[UserProfile] = self.user_profile_repository.list_active()

        for user_profile in users_profiles:
            list_to_return.append(self._to_get_user_profile_output(user_profile))

        return list_to_return


    @classmethod
    def _to_get_user_profile_output(cls, user_profile: UserProfile) -> GetUserProfileOutput:
        return GetUserProfileOutput(
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