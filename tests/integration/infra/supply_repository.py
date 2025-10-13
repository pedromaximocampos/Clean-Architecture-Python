from pprint import pprint

import pytest
from src.infra.mongo.connection import MongoDBProvider
from src.infra.mongo.settings import MongoSettings
from src.config.settings import LOCAL_DB_NAME, LOCAL_CONNECTION_STRING
from src.infra.mongo.repositories.mongo_supplies_repository import MongoSuppliesRepository
from datetime import datetime, timedelta


@pytest.mark.integration
class TestMongoSuppliesRepository:


    @pytest.fixture
    def mongo_supply_repository(self):
        gmon_settings = MongoSettings(
            connection_string="mongodb://admin:admin123@localhost:27017/",
            db_name=LOCAL_DB_NAME,
            tls=False,
            server_selection_timeout_ms=5000,
            app_name="gmon-application-dev",
        )

        mongo_provider = MongoDBProvider(gmon_settings)
        supplie_repository = MongoSuppliesRepository(mongo_provider)

        yield supplie_repository
        mongo_provider.disconnect()



    def test_get_supplies_salles_new_pipeline(self, mongo_supply_repository: MongoSuppliesRepository):

        date = datetime.fromisoformat("2025-10-12T23:35:04.997Z") - timedelta(hours=3, minutes=3)

        ibms = [
            "00000000227201",
            "00000000078501",
            "00000000008301",
            "00000000092101",
            "00000000287401",
            "00000000293101",
            "12006700293101"

        ]

        results = mongo_supply_repository.get_supplies_by_ibms(ibms, date)

        pprint(results)
