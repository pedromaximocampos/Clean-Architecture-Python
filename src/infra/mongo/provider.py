from src.infra.mongo.settings import MongoSettings
from src.infra.mongo.connection import MongoDBProvider
from src.config.settings import LOCAL_DB_NAME, LOCAL_CONNECTION_STRING, DEV



gmon_settings = MongoSettings(
        connection_string=LOCAL_CONNECTION_STRING,
        db_name=LOCAL_DB_NAME,
        tls=False,
        server_selection_timeout_ms=5000,
        app_name="gmon-data-dev",
    )

gmon_provider = MongoDBProvider(gmon_settings)

def get_providers() -> MongoDBProvider:
    return gmon_provider
