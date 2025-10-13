from flask import Blueprint, request, jsonify, make_response


# Composables
from src.main.composables.principal.sales_data.get_principal_composable import get_principal_composable


# Exception Handler
from src.exceptions.exception_handler import ExceptionHandler

# Validators
from src.main.validators.principal_validators.sales_validators.principal_sales_validator import PrincipalSalesValidator


# Adapter (flask)
from src.main.adapters.flask_adapter.flask_adapter import flask_adapter


principal_route_bp = Blueprint('principal_routes', __name__)

@principal_route_bp.route('/vendas/comparativo/principal', methods=['POST'])
def get_principal_data():
    try:
        PrincipalSalesValidator.validate(request)

        controller_handle = get_principal_composable()

        http_response = flask_adapter(request, controller_handle)

    except Exception as e:
        http_response =  ExceptionHandler.handle_exception(e)

    return jsonify(http_response.body), http_response.status_code