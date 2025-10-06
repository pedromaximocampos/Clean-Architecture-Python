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
            can_access_sensitive_information=True,
            can_use_ai_agent=True,
            saved_in_big_query=False,
            authorized_by="admin",
            authorized_at=datetime.now(),
        )
        
        mocked_document = UserProfileMapper.to_document(mocked_user)
        
        return mocked_user, mocked_document
        
        
    def test_create_new_user_success(self, setup_repository, setup_mock_collection, setup_mock_user):
        # Arrange
        mock_user, mock_document = setup_mock_user
        # When insert_one is called, it returns an object with inserted_id
        setup_mock_collection.insert_one.return_value.inserted_id = "507f1f77bcf86cd799439011"
        setup_mock_collection.find_one.return_value = {**mock_document, "_id": "507f1f77bcf86cd799439011"}
        
        # Act
        created_user = setup_repository.insert(mock_user)
        
        # Assert
        assert created_user is not None
        assert created_user.id == "507f1f77bcf86cd799439011"
        assert created_user.email == mock_user.email
        assert created_user.can_access_sensitive_information == mock_user.can_access_sensitive_information
        assert created_user.can_use_ai_agent == mock_user.can_use_ai_agent
        assert created_user.saved_in_big_query == mock_user.saved_in_big_query
        assert created_user.authorized_by == mock_user.authorized_by
        assert created_user.authorized_at == mock_user.authorized_at
        assert created_user.updated_at == None
        assert created_user.updated_by == None
        assert created_user.deleted_at == None
        assert created_user.deleted_by == None
        
        setup_mock_collection.insert_one.assert_called_once()
        setup_mock_collection.find_one.assert_called_once_with({"_id": "507f1f77bcf86cd799439011", **setup_repository._ACTIVE_FILTER})
        
    
    def test_create_user_duplicate_email_raises_unique_violation(self, setup_repository, setup_mock_collection, setup_mock_user):
        # Arrange
        mock_user, _ = setup_mock_user
        setup_mock_collection.insert_one.side_effect = Exception("DuplicateKeyError")
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            setup_repository.insert(mock_user)
        
        assert "DuplicateKeyError" in str(exc_info.value)
        setup_mock_collection.insert_one.assert_called_once()
        
        
    def test_update_user_success(self, setup_repository, setup_mock_collection, setup_mock_user):
        # Arrange
        mock_user, mock_document = setup_mock_user

        updated_email = "updated_user@example.com"
        can_use_ai_agent = False
        saved_in_big_query = True
        updated_by = "admin_updater"

        updated_user_profile = mock_user.update(by="admin",email=updated_email, can_use_ai_agent=can_use_ai_agent, saved_in_big_query=saved_in_big_query)
        
        updated_document = UserProfileMapper.to_document(updated_user_profile)
        
        setup_mock_collection.find_one.return_value = {**updated_document, "_id": "507f1f77bcf86cd799439011"}
        
        # Act
        updated_user = setup_repository.save(mock_user)
        
        
        # Assert
        assert updated_user is not None
        assert updated_user.id == "507f1f77bcf86cd799439011"
        assert updated_user.email == updated_email
        assert updated_user.can_use_ai_agent == can_use_ai_agent
        assert updated_user.saved_in_big_query == saved_in_big_query
        assert updated_user.updated_by == updated_by
        assert updated_user.can_access_sensitive_information == mock_user.can_access_sensitive_information
        assert updated_user.authorized_by == mock_user.authorized_by
        assert updated_user.authorized_at == mock_user.authorized_at
        assert updated_user.deleted_at == None
        assert updated_user.deleted_by == None
        
        
        setup_mock_collection.update_one.assert_called_once_with(
            {"_id": ObjectId(mock_user.id), **setup_repository._ACTIVE_FILTER},
            {"$set": updated_document}
        )
        
        
        