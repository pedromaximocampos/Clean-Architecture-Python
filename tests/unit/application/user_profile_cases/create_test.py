from datetime import datetime
from src.exceptions.custom_exceptions import UniqueViolation
import pytest
from unittest.mock import create_autospec, MagicMock
from src.domain.ports.repositories.user_profile_repository import IUserProfileRepository
from tests.unit.double.mongo_user_profile_repository_spy import MongoUserProfileRepositorySpy as Repository
from src.domain.use_cases.user_profile.create import CreateUserProfileInput, CreateUserProfileOutput
from src.application.use_cases_impl.user_profile.create import CreateUserProfileUseCase
from src.exceptions.apiError import BadRequest


@pytest.mark.unit
class TestCreateUserProfile:

    @pytest.fixture()
    def setup_repository(self) -> Repository:
        return Repository()


    @pytest.fixture()
    def setup_mocked_repository(self) -> MagicMock:
        return create_autospec(IUserProfileRepository, spec_set=True)


    @pytest.fixture
    def setup_user_profile_input(self) -> CreateUserProfileInput:
        mock_user_profile_input = CreateUserProfileInput(email= "pedromaximocc@gmail.com", can_use_ai_agent=False, can_access_sensitive_information=True)
        return mock_user_profile_input


    @pytest.fixture
    def setup_use_case_with_spy(self, setup_repository: Repository) -> CreateUserProfileUseCase:
        return CreateUserProfileUseCase(setup_repository)


    @pytest.fixture
    def setup_use_case_with_mock(self, setup_mocked_repository: MagicMock) -> CreateUserProfileUseCase:
        return CreateUserProfileUseCase(setup_mocked_repository)


    def test_create_a_valid_user_profile_then_return_created_user(self, setup_user_profile_input: CreateUserProfileInput, setup_repository: Repository,
                                         setup_use_case_with_spy: CreateUserProfileUseCase) -> None:
        # Assign
        mocked_input = setup_user_profile_input
        repository = setup_repository
        # Act
        created_user = setup_use_case_with_spy.execute(userDataInput=setup_user_profile_input)


        # Assert
        assert isinstance(created_user, CreateUserProfileOutput)
        assert created_user.id is not None
        assert created_user.email == mocked_input.email
        assert created_user.can_access_sensitive_information == mocked_input.can_access_sensitive_information
        assert created_user.can_use_ai_agent == mocked_input.can_use_ai_agent
        assert created_user.authorized_by == "system"
        assert isinstance(created_user.authorized_at, datetime)

        assert any(call[0] == "insert" for call in repository.calls)
        assert repository.last_saved is not None
        assert repository.last_saved.id == created_user.id


    def test_create_an_existent_active_user_then_raise_bad_request_exception(self, setup_mocked_repository: MagicMock, setup_user_profile_input: CreateUserProfileInput,
                                                                             setup_use_case_with_mock: CreateUserProfileUseCase) -> None:
        # Assign
        setup_mocked_repository.insert.side_effect = UniqueViolation("email", "pedromaximocc@gmail.com")

        # Act
        with pytest.raises(BadRequest):
            setup_use_case_with_mock.execute(userDataInput=setup_user_profile_input)

        # Assert
        setup_mocked_repository.insert.assert_called_once()