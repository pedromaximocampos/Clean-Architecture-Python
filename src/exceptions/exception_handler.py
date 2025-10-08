# src/presentation/exception_handler.py
from typing import Tuple, Type

from src.presentation.http_types.http_response import HttpResponse
from src.config.settings import DEV

import traceback, sys

from src.exceptions.api_types.cache_error import CacheError
from src.exceptions.api_types.bad_request_error import BadRequestError
from src.exceptions.api_types.authorization_error import AuthError
from src.exceptions.api_types.user_is_not_admin import UserIsNotAdmin
from src.exceptions.api_types.conflict_error import ConflictError
from src.exceptions.api_types.upgrade_error import UpgradeRequired
from src.exceptions.api_types.database_error import DatabaseError
from src.exceptions.api_types.not_found_error import NotFoundError


class ExceptionHandler:
    # tuple de TIPOS (classes), sem duplicatas
    API_EXCEPTIONS: Tuple[Type[Exception], ...] = (
        BadRequestError,
        AuthError,
        UserIsNotAdmin,
        CacheError,
        ConflictError,
        UpgradeRequired,
        DatabaseError,
        NotFoundError,
    )

    @staticmethod
    def handle_exception(e: Exception) -> HttpResponse:
        meta = {}

        if DEV:
            exc_type, exc_value, exc_tb = sys.exc_info()  # informações da exceção
            if exc_tb:
                tb = traceback.extract_tb(sys.exc_info()[2]) # pega a traceback
                if tb:
                    filename, lineno, func, text = tb[-1]         # último frame
                    trace  = f"Erro em {filename}, linha {lineno}, função {func}: {text}"
                    if hasattr(e, 'meta') and isinstance(e.meta, dict):
                        meta =  trace

        # casos mapeados (HTTP-friendly)
        if isinstance(e, ExceptionHandler.API_EXCEPTIONS):
            http_response =  HttpResponse(
                status_code=e.status_code,
                body={
                    "errors": [{
                        "title": e.name,
                        "status": e.status_code,
                    }],
                    "meta": meta
                }
            )
            return http_response

        return HttpResponse(
            status_code=500,
            body={
                "errors": [{
                    "title": "Internal Server Error",
                    "status": 500,
                }],
                "meta": meta
            }
        )