from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = 'admin'
    COMMON = 'common'

ALL_ROLES = [RoleEnum.ADMIN, RoleEnum.COMMON]