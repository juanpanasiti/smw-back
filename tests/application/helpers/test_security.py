from src.application.helpers.security import hash_password, verify_password


def test_hash_and_verify_password():
    password = "SecurePassword123!"
    hashed = hash_password(password)
    assert hashed != password  # Ensure the password is hashed
    assert verify_password(password, hashed)  # Verify the password matches the hash
    assert not verify_password("WrongPassword", hashed)  # Verify a wrong password does not match


def test_hash_is_different_each_time():
    password = "AnotherSecurePassword!"
    hashed1 = hash_password(password)
    hashed2 = hash_password(password)
    assert hashed1 != hashed2  # Ensure that hashing the same password twice gives different results
    assert verify_password(password, hashed1)  # Both hashes should verify the original password
    assert verify_password(password, hashed2)
