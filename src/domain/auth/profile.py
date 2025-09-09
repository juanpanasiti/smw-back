from uuid import UUID, uuid4
from datetime import date

from .preferences import Preferences


class Profile():
    def __init__(self, id: UUID, first_name: str, last_name: str, birth_date: date):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.preferences = Preferences(uuid4(), 0.0)

    @classmethod
    def from_dict(cls, data: dict) -> 'Profile':
        profile = cls(
            id=data['id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            birth_date=data['birth_date']
        )
        if 'preferences' in data and data['preferences'] is not None:
            profile.preferences = Preferences.from_dict(data['preferences'])
        else:
            profile.preferences = Preferences(uuid4(), 0.0)
        return profile

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date.isoformat(),
            'preferences': self.preferences.to_dict() if self.preferences else None
        }

    def set_monthly_spending_limit(self, limit: float):
        self.preferences.monthly_spending_limit = limit
