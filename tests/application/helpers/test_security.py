from datetime import timedelta
from uuid import uuid4

import pytest

from src.application.helpers.security import hash_password, verify_password, encode_jwt, decode_jwt, create_access_token
from src.common.exceptions import JWTExpiredError, JWTInvalidError, JWTInvalidSignatureError
from src.domain.auth import User, UserFactory


@pytest.fixture
def user() -> User:
    return UserFactory.create(
        id=uuid4(),
        username='testuser',
        email='user@example.com',
        role='free_user',
        encrypted_password='hashedpassword',
        profile={
            'id': uuid4(),
            'first_name': 'Test',
            'last_name': 'User',
            'birthdate': None,
            'preferences': {
                'id': uuid4(),
            }
        }
    )


def test_hash_and_verify_password():
    password = 'SecurePassword123!'
    hashed = hash_password(password)
    assert hashed != password  # Ensure the password is hashed
    assert verify_password(password, hashed)  # Verify the password matches the hash
    assert not verify_password('WrongPassword', hashed)  # Verify a wrong password does not match


def test_hash_is_different_each_time():
    password = 'AnotherSecurePassword!'
    hashed1 = hash_password(password)
    hashed2 = hash_password(password)
    assert hashed1 != hashed2  # Ensure that hashing the same password twice gives different results
    assert verify_password(password, hashed1)  # Both hashes should verify the original password
    assert verify_password(password, hashed2)


def test_encode_and_decode_jwt(user: User):
    data = {'sub': str(user.id), 'role': user.role.value, 'email': user.email}
    secret = 'supersecretkey'
    token = encode_jwt(data, secret, 'HS256', timedelta(minutes=5))
    assert token is not None
    decoded = decode_jwt(token, secret, 'HS256')
    assert decoded['sub'] == str(user.id)
    assert decoded['role'] == user.role.value
    assert decoded['email'] == user.email


def test_decode_jwt_expired():
    data = {'sub': '1234567890', 'name': 'John Doe', 'admin': True}
    secret = 'supersecretkey'
    token = encode_jwt(data, secret, 'HS256', timedelta(seconds=-1))
    assert token is not None
    with pytest.raises(JWTExpiredError):
        decode_jwt(token, secret, 'HS256')


def test_decode_jwt_invalid_signature():
    data = {'sub': '1234567890', 'name': 'John Doe', 'admin': True}
    secret = 'supersecretkey'
    token = encode_jwt(data, secret, 'HS256', timedelta(minutes=5))
    assert token is not None
    with pytest.raises(JWTInvalidSignatureError):
        decode_jwt(token, 'wrongsecret', 'HS256')


def test_decode_jwt_invalid_token():
    invalid_token = 'invalidtoken'
    secret = 'supersecretkey'
    with pytest.raises(JWTInvalidError):
        decode_jwt(invalid_token, secret, 'HS256')


def test_create_access_token(user: User):
    from src.config import settings
    token = create_access_token(user)
    assert token is not None
    decoded = decode_jwt(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
    assert decoded['sub'] == str(user.id)
    assert decoded['role'] == user.role.value
    assert decoded['email'] == user.email
    assert 'exp' in decoded  # Ensure the token has an expiration claim
