from flask import Blueprint, request, jsonify
from src.main.composables.user_profile.user_profile_create import user_profile_create_composable
from src.main.adapters.flask_adapter.flask_adapter import flask_adapter

user_profile_routes_bp = Blueprint('user_profile_routes', __name__)


@user_profile_routes_bp.route('/usuarios/criar', methods=['POST'])
def create_user_profile():
    controller_handle = user_profile_create_composable()
    http_response = flask_adapter(request, controller_handle)

    return jsonify(http_response.body), http_response.status_code