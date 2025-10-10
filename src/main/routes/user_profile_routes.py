# Libs
from flask import Blueprint, request, jsonify


# Composable
from src.main.composables.user_profile.create import user_profile_create_composable
from src.main.composables.user_profile.update import user_profile_update_composable
from src.main.composables.user_profile.delete import user_profile_delete_composable
from src.main.composables.user_profile.get_all import user_profile_get_all_composable


# Exception Handler
from src.exceptions.exception_handler import ExceptionHandler
from src.exceptions.api_types import ValidationFailed


# Adapter (flask)
from src.main.adapters.flask_adapter.flask_adapter import flask_adapter

# Validators
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


@user_profile_routes_bp.route('/usuarios/atualizar', methods=['PATCH'])
def update_user_profile():
    try:
        controller_handle = user_profile_update_composable()
        http_response = flask_adapter(request, controller_handle)

    except Exception as e:
        http_response = ExceptionHandler.handle_exception(e)

    return jsonify(http_response.body), http_response.status_code


@user_profile_routes_bp.route ('/usuarios/deletar', methods=['DELETE'])
def delete_user_profile():
    try:
        if not request.args.get('user_id'):
            raise ValidationFailed("Parâmetro 'user_id' é obrigatório na query param.")

        controller_handle = user_profile_delete_composable()
        http_response = flask_adapter(request, controller_handle)

    except Exception as e:
        http_response = ExceptionHandler.handle_exception(e)

    return jsonify(http_response.body), http_response.status_code


@user_profile_routes_bp.route('/usuarios/get-all', methods=['GET'])
def get_all_user_profiles():
    try:

        controller_handle = user_profile_get_all_composable()
        http_response = flask_adapter(request, controller_handle)

    except Exception as e:
        http_response = ExceptionHandler.handle_exception(e)

    return jsonify(http_response.body), http_response.status_code