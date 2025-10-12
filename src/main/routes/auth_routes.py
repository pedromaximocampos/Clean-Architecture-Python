
from flask import Blueprint, request, jsonify, make_response


# Composables
from src.main.composables.auth.login_composable import login_composable


# Exception Handler
from src.exceptions.exception_handler import ExceptionHandler
from src.exceptions.api_types import ValidationFailed

# Validators
from src.main.validators.auth_validators.login_validator import LoginValidator


# Adapter (flask)
from src.main.adapters.flask_adapter.flask_adapter import flask_adapter

# Settings
from src.config.settings import DEV, EXPIRATION_TIME_REFRESH_TOKEN


auth_routes_bp = Blueprint('auth_routes', __name__)


@auth_routes_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        LoginValidator.validate(request)

        controller_handle = login_composable()
        http_response = flask_adapter(request, controller_handle)

        refresh_token = http_response.headers.pop('refresh-token')

        response  = make_response(jsonify(http_response.body), http_response.status_code)

        secure = True

        if DEV:
            secure = False

        response.set_cookie('refresh-token', refresh_token, httponly=True, secure=secure, max_age=EXPIRATION_TIME_REFRESH_TOKEN, path="/")

        return response


    except Exception as e:
        http_response = ExceptionHandler.handle_exception(e)
        return jsonify(http_response.body), http_response.status_code

