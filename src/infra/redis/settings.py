from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class RedisSettings:
    host: str
    port: int
    password: str
    user: str
    ssl: bool = True
