
import json
import dataclasses
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID


class Serializer:

    @staticmethod
    def to_primitive(o):
        if is_dataclass(o):
            return asdict(o)
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        if isinstance(o, Decimal):
            return float(o)
        if isinstance(o, UUID):
            return str(o)
        # sets, etc.
        if isinstance(o, set):
            return list(o)
        raise TypeError(f"Tipo não serializável: {o.__class__.__name__}")


    @staticmethod
    def to_datetime(date_str: str) -> datetime:
        try:
            return datetime.fromisoformat(date_str)
        except ValueError as e:
            raise ValueError(f"Formato de data inválido: {date_str}") from e

