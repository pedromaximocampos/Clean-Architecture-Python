from datetime import datetime, timezone
from bson import ObjectId


class UtilsMethods:
    
    @staticmethod
    def now_utc() -> datetime:
        return datetime.now(timezone.utc)
    
    @staticmethod
    def to_oid(value: str | ObjectId) -> ObjectId:
        if isinstance(value, ObjectId):
            return value
        try:
            return ObjectId(value)
        except Exception as exc:
            raise ValueError("Invalid user id") from exc
