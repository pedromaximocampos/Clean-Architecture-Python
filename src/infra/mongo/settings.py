from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class MongoSettings:
    connection_string: str  # ex: "mongodb+srv://user:pass@host/db?retryWrites=true&w=majority"
    db_name: str            # ex: "mydb"
    tls: bool = True
    server_selection_timeout_ms: int = 5000
    app_name: str = "gmon-application"