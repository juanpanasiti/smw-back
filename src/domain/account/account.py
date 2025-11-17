from abc import ABC, abstractmethod
from uuid import UUID
from typing import TYPE_CHECKING

from ..shared import Amount, EntityBase, Month, Year
from .enums import AccountType

if TYPE_CHECKING:
    from ..expense import Payment


class Account(EntityBase, ABC):
    def __init__(
        self,
        id: UUID,
        owner_id: UUID,
        alias: str,
        limit: Amount,
        is_enabled: bool,
    ):
        super().__init__(id)
        self.owner_id = owner_id
        self.alias = alias
        self.limit = limit
        self.is_enabled = is_enabled

    @property
    @abstractmethod
    def account_type(self) -> AccountType:
        """Return the account type. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def get_payments(self, month: Month | None = None, year: Year | None = None) -> list['Payment']:
        'Get all payments for this account in a given month and year.'
        ...

    def to_dict(self, include_relationships: bool = False) -> dict:
        """Convert the Account instance to a dictionary representation."""
        return {
            'id': str(self.id),
            'owner_id': str(self.owner_id),
            'alias': self.alias,
            'limit': self.limit.value,
            'is_enabled': self.is_enabled,
            'account_type': self.account_type.value,
        }
