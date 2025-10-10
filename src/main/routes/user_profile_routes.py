from flask import Blueprint, request, jsonify
from src.main.composables.user_profile.user_profile_create import user_profile_create_composable
from src.exceptions.exception_handler import ExceptionHandler
from src.main.adapters.flask_adapter.flask_adapter import flask_adapter
from src.main.validators.user_profile_validators.create_validator import UserProfileCreateValidator

user_profile_routes_bp = Blueprint('user_profile_routes', __name__)


@user_profile_routes_bp.route('/usuarios/criar', methods=['POST'])
def create_user_profile():
    try:

        UserProfileCreateValidator.validate(request)
        controller_handle = user_profile_create_composable()
        http_response = flask_adapter(request, controller_handle)

    except Exception as e:
        http_response = ExceptionHandler.handle_exception(e)

    return jsonify(http_response.body), http_response.status_code