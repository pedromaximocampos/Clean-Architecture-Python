from contextvars import ContextVar
from typing import Optional
from src.domain.ports.security.models.user_principal import UserPrincipal

_current_user: ContextVar[Optional[UserPrincipal]] = ContextVar("_current_user", default=None)

def set_current_user(principal: UserPrincipal):
    _current_user.set(principal)

def get_current_user() -> Optional[UserPrincipal]:
    return _current_user.get()

def clear_current_user():
    _current_user.set(None)