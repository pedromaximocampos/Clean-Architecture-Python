from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class UserProfile:
    id: str
    email: str
    
    # flags de negócio
    canAccessSensitiveInformation: bool = False
    canUseAiAgent: bool = False
    savedInBigQuery: bool = False
    
    # Autorizacao
    authorizedBy: str = None
    authorizedAt: datetime = None
    
    # Auditoria
    updatedBy: Optional[str] = None
    updatedAt: Optional[datetime] = None
    deletedBy: Optional[str] = None
    deletedAt: Optional[datetime] = None
    
    # Roles
    is_Admin: bool = False
    