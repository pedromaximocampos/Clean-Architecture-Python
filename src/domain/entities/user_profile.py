from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Optional

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

@dataclass(frozen=True)
class UserProfile:
    id: Optional[str]
    email: str
    name: str

    # Auditoria de liberação 
    authorized_by: Optional[str] = None
    authorized_at: Optional[datetime] = None
    
    # Permissoes
    can_access_sensitive_information: bool = False
    can_use_ai_agent: bool = False
    
    # Soft delete
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[str] = None

    # Auditoria de atualizações
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

    # Integração com BigQuery
    saved_in_bigquery: bool = False

    def update(self, by: str, **kwargs):
        allowed = {
            "can_access_sensitive_information",
            "can_use_ai_agent",
            "saved_in_bigquery",
        }
        # valida campos e tipos básicos (ex.: bools)
        for k in kwargs:
            if k not in allowed:
                raise ValueError(f"Campo inválido para atualização: {k}")

        new_fields = dict(kwargs)
        new_fields["updated_at"] = now_utc()
        new_fields["updated_by"] = by
        return replace(self, **new_fields)

    def authorize(self, by: str):
        # autorizar apenas se ainda não autorizado (opcional)
        if self.authorized_at is not None:
            return self
        return replace(self, authorized_by=by, authorized_at=now_utc())

    def deactivate(self, by: str):
        if self.deleted_at is not None:
            raise ValueError("Usuário já foi desativado.")
        t = now_utc()
        return replace(
            self,
            deleted_at=t,
            deleted_by=by,
            updated_at=t,
            updated_by=by,
        )

    def restore(self, by: str):
        if self.deleted_at is None:
            raise ValueError("Usuário já está ativo.")
        t = now_utc()
        return replace(
            self,
            deleted_at=None,
            deleted_by=None,
            updated_at=t,
            updated_by=by,
        )

    def is_active(self) -> bool:
        return self.deleted_at is None