from uuid import UUID
from datetime import datetime

from ..shared import EntityFactoryBase
from .user import User
from .profile import Profile
from .preferences import Preferences
from .enums import Role


class UserFactory(EntityFactoryBase):
    @classmethod
    def create(cls, **kwargs):
        id: UUID | None = kwargs.get('id')
        username: str | None = kwargs.get('username')
        email: str | None = kwargs.get('email')
        encrypted_password: str | None = kwargs.get('encrypted_password')
        role: str | None = kwargs.get('role')
        profile: dict | None = kwargs.get('profile')
        # Validations
        if id is None or not isinstance(id, UUID):
            raise ValueError('A valid UUID is required to create a User instance.')
        if username is None or not isinstance(username, str) or not username.strip():
            raise ValueError('A valid username is required to create a User instance.')
        if email is None or not isinstance(email, str) or not email.strip():
            raise ValueError('A valid email is required to create a User instance.')
        if encrypted_password is None or not isinstance(encrypted_password, str) or not encrypted_password.strip():
            raise ValueError('A valid encrypted_password is required to create a User instance.')
        if role is None or not isinstance(role, str) or role not in Role._value2member_map_:
            raise ValueError(f'A valid role is required to create a User instance. Valid roles are: {list(Role._value2member_map_.keys())}')
        role = Role(role)
        profile_instance = cls.__create_profile(profile)
        return User(
            id=id,
            username=username,
            email=email,
            encrypted_password=encrypted_password,
            role=role,
            profile=profile_instance
        )

    @classmethod
    def __create_profile(cls, profile: dict | None) -> Profile:
        if profile is None:
            raise ValueError('Profile data is required to create a Profile instance.')
        id: UUID | None = profile.get('id')
        first_name: str | None = profile.get('first_name')
        last_name: str | None = profile.get('last_name')
        birthdate: str | None = str(profile.get('birthdate',''))
        preferences: dict = profile.get('preferences', {})
        # Validations
        if id is None or not isinstance(id, UUID):
            raise ValueError('A valid UUID is required to create a Profile instance.')
        if first_name is None or not isinstance(first_name, str) or not first_name.strip():
            raise ValueError('A valid first_name is required to create a Profile instance.')
        if last_name is None or not isinstance(last_name, str) or not last_name.strip():
            raise ValueError('A valid last_name is required to create a Profile instance.')
        preferences_instance = cls.__create_preferences(preferences)
        if isinstance(birthdate, str):
            try:
                birthdate_date = datetime.fromisoformat(birthdate).date()
            except ValueError:
                birthdate_date = None

        return Profile(
            id=id,
            first_name=first_name,
            last_name=last_name,
            birthdate=birthdate_date,
            preferences=preferences_instance
        )

    @classmethod
    def __create_preferences(cls, preferences: dict) -> Preferences:
        id: UUID | None = preferences.get('id')
        monthly_spending_limit: float | None = preferences.get('monthly_spending_limit', 0.0)
        # Validations
        if id is None or not isinstance(id, UUID):
            raise ValueError('A valid UUID is required to create a Preferences instance.')
        if monthly_spending_limit is None or not isinstance(monthly_spending_limit, (int, float)):
            monthly_spending_limit = 0.0
        return Preferences(
            id=id,
            monthly_spending_limit=monthly_spending_limit
        )
