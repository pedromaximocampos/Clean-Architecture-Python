from app.domain.entities.user_profile_domain_entity import UserProfile
from typing import Mapping, Any, Dict, Optional
from bson import ObjectId


class UserProfileMapper:
    
    @staticmethod
    def from_document(document: dict) -> UserProfile:
        return UserProfile(
            id=str(document['_id']),
            email=document['email'],
            canAccessSensitiveInformation=document.get('canAccessSensitiveInformation', False),
            canUseAiAgent=document.get('canUseAiAgent', False),
            authorizedBy=document["authorizedBy"],
            authorizedAt=document["authorizedAt"],
            updatedBy=document.get('updatedBy'),
            updatedAt=document.get('updatedAt'),
            deletedBy=document.get('deletedBy'),
            deletedAt=document.get('deletedAt')
        )
        
    @staticmethod
    def to_document(user_profile: UserProfile) -> Dict[str, Any]:
        # NÃO colocamos _id aqui — Mongo gera sozinho no insert
        doc: Dict[str, Any] = {
            "email": user_profile.email,
            "canAccessSensitiveInformation": user_profile.canAccessSensitiveInformation,
            "canUseAiAgent": user_profile.canUseAiAgent,
            "savedInBigQuery": getattr(user_profile, "savedInBigQuery", False),
            "authorizedBy": user_profile.authorizedBy,
            "authorizedAt": user_profile.authorizedAt,
            "updatedBy": user_profile.updatedBy,
            "updatedAt": user_profile.updatedAt,
            "deletedBy": user_profile.deletedBy,
            "deletedAt": user_profile.deletedAt
        }
        # remove None para não gravar null
        return {k: v for k, v in doc.items() if v is not None}