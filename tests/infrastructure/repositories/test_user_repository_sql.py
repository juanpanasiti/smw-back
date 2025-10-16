import pytest
import copy
from uuid import uuid4

from src.infrastructure.repositories import UserRepositorySQL
from src.domain.auth import User as UserEntity, UserFactory
from src.infrastructure.database.models import UserModel
from tests.fixtures.auth_fixtures import user as user_entity
from tests.fixtures.db_fixtures import sqlite_session


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
