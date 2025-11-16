from uuid import UUID

from ..shared.entity_base import EntityBase
from .enums import Role
from .profile import Profile


class User(EntityBase):
    def __init__(self, id: UUID, username: str, email: str, encrypted_password: str, role: Role, profile: Profile):
        super().__init__(id)
        self.username = username  # TODO: Add validation -> value_object?
        self.email = email  # TODO: Add validation -> value_object?
        self.encrypted_password = encrypted_password
        self.role = role
        self.profile = profile

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
            'role': self.role.value,
            'profile': self.profile.to_dict()
        }

    def set_monthly_spending_limit(self, limit: float):
        self.profile.set_monthly_spending_limit(limit)
