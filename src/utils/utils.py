from datetime import datetime, timezone, timedelta
from bson import ObjectId
from zoneinfo import ZoneInfo



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


    @staticmethod
    def check_data(date: datetime | None = None) -> datetime:
        if date is None:
            today = datetime.now(timezone.utc).replace(second=0, microsecond=0) - timedelta(hours=3, minutes=3,
                                                                                            seconds=0)
            return today
        else:
            today_date = datetime.now()

            date = date.astimezone(timezone.utc)

            if today_date.date() > date.date():
                return date.replace(hour=0, minute=0, second=0, microsecond=0)
            else:
                return date - timedelta(hours=3, minutes=3, seconds=0)


    @staticmethod
    def convert_date_from_isoformat(date_str: str) -> datetime:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date
