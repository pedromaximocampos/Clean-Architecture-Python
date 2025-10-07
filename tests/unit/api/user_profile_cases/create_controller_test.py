from datetime import datetime

import pytest
from unittest.mock import MagicMock, create_autospec
from src.application.controllers.user_profile.create_controller import CreateUserProfileController
from src.domain.use_cases_interfaces.user_profile.create import ICreateUserProfile, CreateUserProfileOutput
from src.application.http_types import HttpRequest
from src.application.http_types import HttpResponse


class TestCreateUserProfileController:


    @pytest.fixture
    def setup_create_use_case(self) -> MagicMock:
        return create_autospec(ICreateUserProfile)


    @pytest.fixture
    def setup_controller(self, setup_create_use_case: MagicMock) -> CreateUserProfileController:
        return CreateUserProfileController(create_user_profile_use_case=setup_create_use_case)


    @pytest.fixture
    def setup_http_request(self) -> HttpRequest:
        return HttpRequest(
            url='http://example.com',
            method='POST',
            body={
                'email': 'pedromaximocc@gmail.com',
                'can_access_sensitive_information': True,
                'can_use_ai_agent': False
            }
        )


    def test_handle_request_success(self, setup_controller: CreateUserProfileController, setup_create_use_case: MagicMock, setup_http_request: HttpRequest) -> None:
        # Assing
        setup_create_use_case.execute.return_value = CreateUserProfileOutput(
            id='12345',
            email= setup_http_request.body.get('email'),
            can_access_sensitive_information= setup_http_request.body.get('can_access_sensitive_information'),
            can_use_ai_agent= setup_http_request.body.get('can_use_ai_agent'),
            saved_in_big_query=False,
            authorized_by='system',
            authorized_at=datetime.utcnow(),
            updated_by=None,
            updated_at=None
        )


        # Act
        response: HttpResponse = setup_controller.handle_request(setup_http_request)
        user_response = response.body
        status_code = response.status_code

        # Assert
        assert status_code == 201
        assert user_response.get("id") == "12345"
        assert user_response.get("email") == setup_http_request.body.get('email')
        assert user_response.get("can_access_sensitive_information") == setup_http_request.body.get('can_access_sensitive_information')
        assert user_response.get("can_use_ai_agent") == setup_http_request.body.get('can_use_ai_agent')
        assert user_response.get("saved_in_big_query") is False
        assert user_response.get("authorized_by") == 'system'
        assert isinstance(user_response.get("authorized_at"), str)
