from uuid import UUID, uuid4
from datetime import date

from .preferences import Preferences


class Profile():
    def __init__(self, id: UUID, first_name: str, last_name: str, birthdate: date | None, preferences: Preferences | None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.preferences = preferences or Preferences(uuid4(), 0.0)

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birthdate': self.birthdate.isoformat() if self.birthdate else None,
            'preferences': self.preferences.to_dict() if self.preferences else None
        }

    def set_monthly_spending_limit(self, limit: float):
        self.preferences.monthly_spending_limit = limit
