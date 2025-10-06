from src.domain.entities.user_profile import UserProfile as UserProfileEntity
from typing import Mapping, Any, Dict, Optional
from bson import ObjectId


class UserProfileMapper:
    
    @staticmethod
    def from_document(document: dict) -> UserProfileEntity:
        return UserProfileEntity(
            id=str(document['_id']),
            email=document['email'],
            can_access_sensitive_information=document.get('canAccessSensitiveInformation', False),
            can_use_ai_agent=document.get('canUseAiAgent', False),
            saved_in_big_query=document.get('savedInBigQuery', False),
            authorized_by=document["authorizedBy"],
            authorized_at=document["authorizedAt"],
            updated_by=document.get('updatedBy'),
            updated_at=document.get('updatedAt'),
            deleted_by=document.get('deletedBy'),
            deleted_at=document.get('deletedAt')
        )
        
    @staticmethod
    def to_document(user_profile: UserProfileEntity) -> Dict[str, Any]:
        # NÃO colocamos _id aqui — Mongo gera sozinho no insert
        doc: Dict[str, Any] = {
            "email": user_profile.email,
            "canAccessSensitiveInformation": user_profile.can_access_sensitive_information,
            "canUseAiAgent": user_profile.can_use_ai_agent,
            "savedInBigQuery": user_profile.saved_in_big_query,
            "authorizedBy": user_profile.authorized_by,
            "authorizedAt": user_profile.authorized_at,
            "updatedBy": user_profile.updated_by,
            "updatedAt": user_profile.updated_at,
            "deletedBy": user_profile.deleted_by,
            "deletedAt": user_profile.deleted_at
        }
        doc.pop("id", None)  # remove id se existir
        # remove None para não gravar null
        return {k: v for k, v in doc.items() if v is not None}