from os import getenv


DEV = getenv("FLASK_ENV") != "production"


LOCAL_CONNECTION_STRING = getenv("LOCAL_CONNECTION_STRING")
LOCAL_DB_NAME = getenv("LOCAL_DB_NAME")
