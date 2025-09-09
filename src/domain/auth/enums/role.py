from enum import Enum


class Role(str, Enum):
    ADMIN = 'admin'
    FREE_USER = 'free_user'
    PREMIUM_USER = 'premium_user'
    TEST_USER = 'test_user'
