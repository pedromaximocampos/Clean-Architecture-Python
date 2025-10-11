from src.domain.ports.repositories.user_profile_repository import IUserProfileRepository
from src.domain.use_cases.user_profile.delete import IDeleteUserProfile
from src.domain.entities.user_profile import UserProfile


from src.exceptions.api_types import NotFoundError, BadRequestError


class DeleteUserProfileUseCase(IDeleteUserProfile):
    def __init__(self, user_profile_repository: IUserProfileRepository):
        self.user_profile_repository = user_profile_repository

    def execute(self, user_id: str) -> str:

        user_profile: UserProfile = self.user_profile_repository.find_by_id(user_id)

        if not user_profile:
            raise NotFoundError(f"UserProfile with id:{user_id} not found")

        if not user_profile.is_active():
            raise BadRequestError(f"UserProfile already inactive with id:{user_id}")


        self.user_profile_repository.soft_delete(user_id, by="system")

        return "UserProfile deleted successfully"
    