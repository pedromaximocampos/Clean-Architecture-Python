from unittest.mock import MagicMock
import pytest
from src.infra.mongo.repositories.mongo_user_profile_repository import MongoUserProfileRepository
from datetime import datetime
from src.infra.mongo.mappers.user_profile_mapper import UserProfileMapper
from bson import ObjectId


@pytest.mark.unit
class TestUserProfileRepository:
    
    @pytest.fixture
    def setup_mock_collection(self):
        return MagicMock()

    @pytest.fixture
    def setup_repository(self, setup_mock_collection):
        db = MagicMock()
        db.get_collection.return_value = setup_mock_collection
        return MongoUserProfileRepository(db)
    
    @pytest.fixture
    def setup_mock_user(self):
        from src.domain.entities.user_profile import UserProfile
        mocked_user =  UserProfile(
            id="",
            email="user123@example.com",
            canAccessSensitiveInformation=True,
            canUseAiAgent=True,
            savedInBigQuery=False,
            authorizedBy="admin",
            authorizedAt=datetime.now(),
        )
        
        mocked_document = UserProfileMapper.to_document(mocked_user)
        
        return mocked_user, mocked_document
        
        
    def test_create_new_user_success(self, setup_repository, setup_mock_collection, setup_mock_user):
        # Arrange
        mock_user, mock_document = setup_mock_user
        # When insert_one is called, it returns an object with inserted_id
        setup_mock_collection.insert_one.return_value.inserted_id = "generated_id_123"
        setup_mock_collection.find_one.return_value = {**mock_document, "_id": "generated_id_123"}
        
        # Act
        created_user = setup_repository.create_user(mock_user)
        
        # Assert
        assert created_user is not None
        assert created_user.id == "generated_id_123"
        assert created_user.email == mock_user.email
        assert created_user.canAccessSensitiveInformation == mock_user.canAccessSensitiveInformation
        assert created_user.canUseAiAgent == mock_user.canUseAiAgent
        assert created_user.savedInBigQuery == mock_user.savedInBigQuery
        assert created_user.authorizedBy == mock_user.authorizedBy
        assert created_user.authorizedAt == mock_user.authorizedAt
        assert created_user.updatedAt == None
        assert created_user.updatedBy == None
        assert created_user.deletedAt == None
        assert created_user.deletedBy == None
        
        setup_mock_collection.insert_one.assert_called_once()
        setup_mock_collection.find_one.assert_called_once_with({"_id": "generated_id_123", **setup_repository._ACTIVE_USER_FILTER})
        
    
    def test_create_user_duplicate_email_raises_unique_violation(self, setup_repository, setup_mock_collection, setup_mock_user):
        # Arrange
        mock_user, _ = setup_mock_user
        setup_mock_collection.insert_one.side_effect = Exception("DuplicateKeyError")
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            setup_repository.create_user(mock_user)
        
        assert "DuplicateKeyError" in str(exc_info.value)
        setup_mock_collection.insert_one.assert_called_once()
        
        
    def test_update_user_success(self, setup_repository, setup_mock_collection, setup_mock_user):
        # Arrange
        mock_user, mock_document = setup_mock_user
        mock_user.id = "507f1f77bcf86cd799439011"
        
        updated_email = "updated_user@example.com"
        can_use_ai_agent = False
        saved_in_bigquery = True
        updated_by = "admin_updater"
        updated_at = datetime.now()
        
        mock_user.email = updated_email
        mock_user.canUseAiAgent = can_use_ai_agent
        mock_user.savedInBigQuery = saved_in_bigquery
        mock_user.updatedBy = updated_by
        mock_user.updatedAt = updated_at
        
        updated_document = UserProfileMapper.to_document(mock_user)
        
        setup_mock_collection.find_one.return_value = {**updated_document, "_id": "507f1f77bcf86cd799439011"}
        
        # Act
        updated_user = setup_repository.update_user(mock_user)
        
        
        # Assert
        assert updated_user is not None
        assert updated_user.id == "507f1f77bcf86cd799439011"
        assert updated_user.email == updated_email
        assert updated_user.canUseAiAgent == can_use_ai_agent
        assert updated_user.savedInBigQuery == saved_in_bigquery
        assert updated_user.updatedBy == updated_by
        assert updated_user.updatedAt == updated_at
        assert updated_user.canAccessSensitiveInformation == mock_user.canAccessSensitiveInformation
        assert updated_user.authorizedBy == mock_user.authorizedBy
        assert updated_user.authorizedAt == mock_user.authorizedAt
        assert updated_user.deletedAt == None
        assert updated_user.deletedBy == None
        
        
        setup_mock_collection.update_one.assert_called_once_with(
            {"_id": ObjectId(mock_user.id), **setup_repository._ACTIVE_USER_FILTER},
            {"$set": updated_document}
        )
        
        
        