from enum import Enum


class Role(str, Enum):
    ADMIN = 'admin'
    FREE_USER = 'free_user'
    PREMIUM_USER = 'premium_user'
    TEST_USER = 'test_user'


ALL_ROLES = [role for role in Role]
ADMIN_ROLES = [Role.ADMIN]
PREMIUM_ROLES = [Role.PREMIUM_USER, Role.ADMIN]
FREE_USER_ROLES = [Role.FREE_USER, Role.PREMIUM_USER, Role.ADMIN]
TEST_USER_ROLES = [Role.TEST_USER, Role.ADMIN]
