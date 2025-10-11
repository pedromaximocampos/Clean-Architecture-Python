from src.presentation.controllers.user_profile.create_controller import CreateUserProfileController
from src.infra.mongo.repositories.mongo_user_profile_repository import MongoUserProfileRepository
from src.application.use_cases_impl.user_profile.create import CreateUserProfileUseCase
from src.infra.mongo.providers import get_providers

def user_profile_create_composable():
    gmon_provider = get_providers()
    user_profile_repository = MongoUserProfileRepository(gmon_provider)
    create_user_profile_use_case = CreateUserProfileUseCase(user_profile_repository)
    create_user_profile_controller = CreateUserProfileController(create_user_profile_use_case)
    return create_user_profile_controller.handle_request