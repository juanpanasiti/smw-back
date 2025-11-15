import pytest
import copy
from uuid import uuid4

from src.infrastructure.repositories import UserRepositorySQL
from src.domain.auth import User as UserEntity
from src.infrastructure.database.models import UserModel
from tests.fixtures.auth_fixtures import user as user_entity  # noqa: F401
from tests.fixtures.db_fixtures import sqlite_session  # noqa: F401


@pytest.fixture
def user_repo(sqlite_session) -> UserRepositorySQL:
    return UserRepositorySQL(model=UserModel, session_factory=sqlite_session)


def test_user_repository_sql_init(user_repo: UserRepositorySQL):
    assert isinstance(user_repo, UserRepositorySQL)
    assert hasattr(user_repo, 'create')
    assert hasattr(user_repo, 'get_many_by_filter')
    assert hasattr(user_repo, 'count_by_filter')
    assert hasattr(user_repo, 'update')
    assert hasattr(user_repo, 'delete_by_filter')


def test_user_repository_get_filter_params(user_repo: UserRepositorySQL):
    params = {
        'email': 'test@example.com',
        'username': 'testuser',
        'some_key': 'some_value',
    }
    filter_params = user_repo._get_filter_params(params)
    assert filter_params == {
        'email': 'test@example.com',
        'username': 'testuser'
    }
    assert 'some_key' not in filter_params


def test_user_repository_create(user_repo: UserRepositorySQL, user_entity: UserEntity):
    created_user = user_repo.create(user_entity)
    assert isinstance(created_user, UserEntity)
    assert created_user.email == user_entity.email
    assert created_user.username == user_entity.username
    assert created_user.role == user_entity.role
    assert created_user.profile.id == user_entity.profile.id
    assert created_user.profile.first_name == user_entity.profile.first_name
    assert created_user.profile.last_name == user_entity.profile.last_name
    assert created_user.profile.birthdate == user_entity.profile.birthdate
    assert created_user.profile.preferences.id == user_entity.profile.preferences.id
    assert created_user.profile.preferences.monthly_spending_limit == user_entity.profile.preferences.monthly_spending_limit
    # Test if user exists in DB
    users_in_db = user_repo.count_by_filter(filter={'id': user_entity.id})
    assert users_in_db == 1


def test_user_repository_get_many_by_filter(user_repo: UserRepositorySQL, user_entity: UserEntity):
    # Create multiple users
    for i in range(5):
        user_copy = copy.deepcopy(user_entity)
        user_copy.id = uuid4()
        user_copy.email = f'test{i}@example.com'
        user_copy.username = f'SomeUsername{i}'
        user_copy.profile.id = uuid4()
        user_copy.profile.preferences.id = uuid4()
        user_repo.create(user_copy)

    # Test number of users in db
    total_users = user_repo.count_by_filter()
    assert total_users == 5


def test_user_repository_get_by_filter(user_repo: UserRepositorySQL, user_entity: UserEntity):
    created_user = user_repo.create(user_entity)
    fetched_user = user_repo.get_by_filter({'id': created_user.id})
    assert fetched_user is not None
    __compare_users(fetched_user, created_user)
    fetched_user_by_email = user_repo.get_by_filter({'email': created_user.email})
    assert fetched_user_by_email is not None
    __compare_users(fetched_user_by_email, created_user)
    fetched_user_by_username = user_repo.get_by_filter({'username': created_user.username})
    assert fetched_user_by_username is not None
    __compare_users(fetched_user_by_username, created_user)


def test_user_repository_update(user_repo: UserRepositorySQL, user_entity: UserEntity):
    created_user: UserEntity = user_repo.create(user_entity)
    new_email = 'updated@example.com'
    user_copy = copy.deepcopy(created_user)
    user_copy.email = new_email
    updated_user = user_repo.update(user_copy)
    assert updated_user is not None
    __compare_users(updated_user, user_copy)


def test_user_repository_delete_by_filter(user_repo: UserRepositorySQL, user_entity: UserEntity):
    created_user = user_repo.create(user_entity)
    users_in_db = user_repo.count_by_filter(filter={'id': created_user.id})
    assert users_in_db == 1
    user_repo.delete_by_filter({'id': created_user.id})
    users_in_db_after_delete = user_repo.count_by_filter(filter={'id': created_user.id})
    assert users_in_db_after_delete == 0


def test_user_repository_update_non_existent_user(user_repo: UserRepositorySQL, user_entity: UserEntity):
    """Test updating a user that doesn't exist raises ValueError."""
    non_existent_user = copy.deepcopy(user_entity)
    non_existent_user.id = uuid4()
    
    with pytest.raises(ValueError, match=f'User with id {non_existent_user.id} does not exist'):
        user_repo.update(non_existent_user)


def test_user_repository_update_creates_profile_if_not_exists(user_repo: UserRepositorySQL, user_entity: UserEntity):
    """Test that updating a user creates a profile if it doesn't exist."""
    from src.domain.auth import Profile, Preferences
    
    # Create user first
    created_user = user_repo.create(user_entity)
    
    # Delete the profile manually from DB to simulate user without profile
    from src.infrastructure.database.models import ProfileModel
    with user_repo.session_factory() as session:
        session.query(ProfileModel).filter_by(user_id=created_user.id).delete()
        session.commit()
    
    # Now update user with a new profile
    user_copy = copy.deepcopy(created_user)
    new_profile = Profile(
        id=uuid4(),
        first_name='NewFirst',
        last_name='NewLast',
        birthdate=None,
        preferences=Preferences(
            id=uuid4(),
            monthly_spending_limit=500.0
        )
    )
    user_copy.profile = new_profile
    
    updated_user = user_repo.update(user_copy)
    
    # Verify profile was created
    assert updated_user.profile is not None
    assert updated_user.profile.first_name == 'NewFirst'
    assert updated_user.profile.last_name == 'NewLast'
    assert updated_user.profile.preferences.monthly_spending_limit == 500.0

# Auxiliary functions


def __compare_users(user1: UserEntity, user2: UserEntity):
    assert user1.id == user2.id
    assert user1.email == user2.email
    assert user1.username == user2.username
    assert user1.role == user2.role
    assert user1.profile.id == user2.profile.id
    assert user1.profile.first_name == user2.profile.first_name
    assert user1.profile.last_name == user2.profile.last_name
    assert user1.profile.birthdate == user2.profile.birthdate
    assert user1.profile.preferences.id == user2.profile.preferences.id
    assert user1.profile.preferences.monthly_spending_limit == user2.profile.preferences.monthly_spending_limit
