from flask import Flask
from src.main.routes.user_profile_routes import user_profile_routes_bp
from src.main.routes.auth_routes import auth_routes_bp

def create_app():

    app = Flask(__name__)

    # Registrar blueprints
    app.register_blueprint(user_profile_routes_bp)
    app.register_blueprint(auth_routes_bp)

    return app