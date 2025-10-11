from src.presentation.controllers.user_profile.update_controller import UpdateUserProfileController
from src.infra.mongo.repositories.mongo_user_profile_repository import MongoUserProfileRepository
from src.application.use_cases_impl.user_profile.update import UpdateUserProfileUseCase
from src.infra.mongo.providers import get_providers


def user_profile_update_composable():
    gmon_provider = get_providers()
    user_profile_repository = MongoUserProfileRepository(gmon_provider)
    update_user_profile_use_case = UpdateUserProfileUseCase(user_profile_repository)
    update_user_profile_controller = UpdateUserProfileController(update_user_profile_use_case)
    return update_user_profile_controller.handle_request