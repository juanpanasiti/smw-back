from uuid import UUID

from ..shared import Amount
from ..shared.entity_base import EntityBase


class Preferences(EntityBase):
    def __init__(
        self,
        id: UUID,
        monthly_spending_limit: float
        # TODO: add an option to set the first day of the month for the period
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

    def to_dict(self) -> dict:
        return {
            'monthly_spending_limit': self.monthly_spending_limit
        }
