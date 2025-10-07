from dataclasses import dataclass, asdict, field
from typing import Optional, Dict
from uuid import uuid4

@dataclass
class ApiError(Exception):
    error: str
    status: int
    meta: Dict = field(default_factory=dict) # aqui para recriar um dict vazio para cada instancia e nao compartilhar entre todas
    error_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self):
        if self.meta is None:
            self.meta = {}
        self.meta.setdefault("error_id", str(self.error_id))
    
    def to_dict(self):
        return asdict(self)

class ResourceNotFound(ApiError):
    def __init__(self, error: str = "Resource not found", meta: Optional[Dict] = None):
        super().__init__(error=error, status=404, meta=meta)

class Conflict(ApiError):
    def __init__(self, error: str = "Resource conflict", meta: Optional[Dict] = None):
        super().__init__(error=error, status=409, meta=meta)

class ValidationFailed(ApiError):
    def __init__(self, error: str = "Validation failed", meta: Optional[Dict] = None):
        super().__init__(error=error, status=422, meta=meta)
        
class UpgradeRequired(ApiError):
    def __init__(self, error: str = "Upgrade required", meta: Optional[Dict] = None):
        super().__init__(error=error, status=426, meta=meta)
        
class AuthError(ApiError):
    def __init__(self, error: str = "Expired credentials", meta: Optional[Dict] = None):
        super().__init__(error=error, status=401, meta=meta)
        
class DataBaseError(ApiError):
    def __init__(self, error: str= "Erro ao conectar com a LBC", meta: Optional[Dict] = None):
        super().__init__(error=error, status=503, meta=meta)
        
class CacheError(ApiError):
    def __init__(self, error: str = "Erro ao conectar com a LBC", meta: Optional[Dict] = None):
        super().__init__(error=error, status=503, meta=meta)
        
class BadRequest(ApiError):
    def __init__(self, error: str = "Bad request", meta: Optional[Dict] = None):
        super().__init__(error=error, status=400, meta=meta)
        
class UserIsNotAdmin(ApiError):
    def __init__(self, error: str = "User is not admin", meta: Optional[Dict] = None):
        super().__init__(error=error, status=403, meta=meta)