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



    @staticmethod
    def is_today(date: datetime) -> bool:
        now = UtilsMethods.now_utc()
        return date.date() == now.date()


    @staticmethod
    def should_read_cache(date: datetime) -> bool:
       return UtilsMethods.is_today(date)


    @staticmethod
    def calculate_variation(field1: float, field2: float) -> float:
        if field2 != 0:
            return round((((field1 * 100) / field2) - 100), 2)
        else:
            return 0.0