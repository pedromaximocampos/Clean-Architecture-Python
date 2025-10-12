from flask import request, abort

from src.application.services.security.auth_guard_impl import AuthGuardImpl
from src.domain.ports.security.auth_guard import IAuthGuard
from src.domain.ports.security.models.user_principal import UserPrincipal

from src.shared.contexts.current_user import set_current_user, clear_current_user

from src.exceptions.api_types import AuthError



class FlaskAuthGuardAdapter:

    PUBLIC_ROUTES = [
        '/auth/login',
        '/auth/refresh',
        '/docs',
        '/openapi.json',
        '/health',
    ]

    def __init__(self, auth_guard: AuthGuardImpl):
        self.auth_guard: IAuthGuard = auth_guard


    def before_request(self):
        if request.path in self.PUBLIC_ROUTES:
            return

        access_token = request.headers.get('token')
        refresh_token = request.cookies.get('refresh_token')

        if not access_token or not refresh_token:
            clear_current_user()
            raise AuthError

        try:
            principal: UserPrincipal = self.auth_guard.authenticate(access_token, refresh_token)
            set_current_user(principal)
        except Exception:
            clear_current_user()
            raise AuthError


    def after_request(self, response):
        clear_current_user()
        return response