from src.application.use_cases_impl.user_profile.get_all import GetAllUserProfilesUseCase
from src.infra.mongo.repositories.mongo_user_profile_repository import MongoUserProfileRepository
from src.presentation.controllers.user_profile.get_all_controller import GetAllUserProfilesController


from src.infra.mongo.provider import get_providers

def user_profile_get_all_composable():
    gmon_provider = get_providers()
    user_profile_repository = MongoUserProfileRepository(gmon_provider)
    get_all_user_profiles_use_case = GetAllUserProfilesUseCase(user_profile_repository)
    get_all_user_profiles_controller = GetAllUserProfilesController(get_all_user_profiles_use_case)
    return get_all_user_profiles_controller.handle_request