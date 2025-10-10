from src.presentation.controllers.user_profile.delete_controller import DeleteUserProfileController
from src.infra.mongo.repositories.mongo_user_profile_repository import MongoUserProfileRepository
from src.application.use_cases_impl.user_profile.delete import DeleteUserProfileUseCase
from src.infra.mongo.provider import get_providers


def user_profile_delete_composable():
    gmon_provider = get_providers()
    user_profile_repository = MongoUserProfileRepository(gmon_provider)
    delete_user_profile_use_case = DeleteUserProfileUseCase(user_profile_repository)
    delete_user_profile_controller = DeleteUserProfileController(delete_user_profile_use_case)
    return delete_user_profile_controller.handle_request