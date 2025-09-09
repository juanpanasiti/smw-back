from uuid import UUID

from ..shared import Amount
from ..shared.entity_base import EntityBase


class Preferences(EntityBase):
    def __init__(
        self,
        id: UUID,
        monthly_spending_limit: float
    ):
        super().__init__(id)
        self.__monthly_spending_limit: Amount = Amount(monthly_spending_limit)

    @property
    def monthly_spending_limit(self) -> float:
        return self.__monthly_spending_limit.value

    @monthly_spending_limit.setter
    def monthly_spending_limit(self, value: float):
        if value < 0:
            raise ValueError('Monthly spending limit cannot be negative')
        self.__monthly_spending_limit = Amount(value)

    @classmethod
    def from_dict(cls, data: dict) -> 'Preferences':
        return cls(
            id=data['id'],
            monthly_spending_limit=data['monthly_spending_limit']
        )

    def to_dict(self) -> dict:
        return {
            'monthly_spending_limit': self.monthly_spending_limit
        }
