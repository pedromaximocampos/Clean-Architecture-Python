import pytest
from app.infra.mongo.connection import MongoDBProvider
from app.infra.mongo.settings import MongoSettings

@pytest.mark.integration
class TestMongoProviderIntegration:
    
    @pytest.fixture
    def setup_mongo_settings(self):
        return MongoSettings(
            connection_string="mongodb://admin:admin123@localhost:27017/",
            db_name="GMON_Clean_Arch_Refactor",
            tls=False,
            server_selection_timeout_ms=5000,
        )
        
        
    @pytest.fixture
    def setup_mongo_provider(self, setup_mongo_settings):
        mongo_provider = MongoDBProvider(setup_mongo_settings)
        mongo_provider.client()  
        yield mongo_provider
        mongo_provider.disconnect()
        


    def test_mongo_client_connection(self, setup_mongo_provider):
        # Arrange e Act
        client = setup_mongo_provider.client()
        
        # Assert
        assert client is not None
        assert client.address is not None  # Verifica se o cliente está conectado a um endereço
        assert client.admin.command('ping')['ok'] == 1.0  # Verifica se o ping ao servidor MongoDB é bem-sucedido