from flask import jsonify, request, g
from werkzeug.exceptions import HTTPException
from src.api.advices.apiError import ApiError
import traceback, sys
from uuid import uuid4

class GlobalExceptionHandler:
    """
    Classe para registrar manipuladores globais de exceções no aplicativo Flask.
    """
    developmentMode = True
    
    @staticmethod
    def register_error_handlers(app):
        
        @app.errorhandler(ApiError)
        def handle_custom_exception(error: ApiError):
            if GlobalExceptionHandler.developmentMode:
                exc_type, exc_value, exc_tb = sys.exc_info()  # informações da exceção
                if exc_tb:
                    tb = traceback.extract_tb(sys.exc_info()[2]) # pega a traceback
                    if tb:
                        filename, lineno, func, text = tb[-1]         # último frame
                        trace  = f"Erro em {filename}, linha {lineno}, função {func}: {text}"
                        error.meta["traceback"] =  trace
            app.logger.warning("ApiError %s", error.error, extra={"status": error.status, **(error.meta or {})})
            response = jsonify(error.to_dict()), error.status
            return response
        
        
        @app.errorhandler(HTTPException)
        def handle_http_exception(error: HTTPException):
            body = {
                "error": error.name,            # ex: "Not Found"
                "status": error.code,           # 404, 405...
                "detail": error.description,    # descrição do Werkzeug
                "path": request.path
            }
            
            response = jsonify({
                "error": error.description,
                "status": error.code
            }), error.code
            return response
        
        
        @app.errorhandler(Exception)
        def handle_general_exception(error : Exception):
            error_id = str(uuid4())
            
            app.logger.exception("Unhandled exception", extra={
                "error_id": error_id,
                "path": request.path,
                "method": request.method,
                "correlation_id": getattr(g, "correlation_id", None),
            })
            
            body = {
                "error": "Internal Server Error",
                "status": 500,
                "meta": {
                    "error_id": error_id,
                    "correlation_id": getattr(g, "correlation_id", None)
                }
            }
            if GlobalExceptionHandler.developmentMode:
                exc_type, exc_value, exc_tb = sys.exc_info()  # informações da exceção
                if exc_tb:
                    tb = traceback.extract_tb(sys.exc_info()[2]) # pega a traceback
                    if tb:
                        filename, lineno, func, text = tb[-1]         # último frame
                        trace  = f"Erro em {filename}, linha {lineno}, função {func}: {text}"
                        body["meta"]["traceback"] =  trace
                body["meta"]["message"] = str(error)
            response = jsonify(body), 500
            return response