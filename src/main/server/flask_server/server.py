from flask import Flask

# Routes
from src.main.routes.user_profile_routes import user_profile_routes_bp
from src.main.routes.auth_routes import auth_routes_bp
from src.main.routes.principal_routes import principal_route_bp

# User Context
from src.shared.contexts.current_user import clear_current_user

# Security composable
from src.main.composables.security.flask_guard_composable import create_flask_guard_composable


def create_app():

    app = Flask(__name__)

    # Registrar lifecycle events
    register_lifecycle_events(app)

    # Configurar segurança
    flask_guard = create_flask_guard_composable()

    app.before_request(flask_guard.before_request)

    app.after_request(flask_guard.after_request)

    # Registrar blueprints
    register_blueprints(app)

    return app


def register_lifecycle_events(app: Flask):

    @app.after_request
    def _cleanup_context(response):
        clear_current_user()
        return response

    @app.teardown_request
    def _cleanup_context_teardown(exc):
        clear_current_user()


def register_blueprints(app: Flask):
    app.register_blueprint(user_profile_routes_bp)
    app.register_blueprint(auth_routes_bp)
    app.register_blueprint(principal_route_bp)
