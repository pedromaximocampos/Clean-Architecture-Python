from flask import Flask, request, jsonify
from src.main.server.advices.globalExceptionHandler import GlobalExceptionHandler
from src.main.routes.user_profile_routes import user_profile_routes_bp

def create_app():

    app = Flask(__name__)

    # Registrar manipuladores globais de exceções
    GlobalExceptionHandler.register_error_handlers(app)

    # Registrar blueprints
    app.register_blueprint(user_profile_routes_bp)

    return app