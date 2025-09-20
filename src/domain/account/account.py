from abc import ABC, abstractmethod
from uuid import UUID
from typing import TYPE_CHECKING

from ..shared import Amount, EntityBase
from ..auth import User

if TYPE_CHECKING:
    from ..expense import Payment


class Account(EntityBase, ABC):
    def __init__(
        self,
        id: UUID,
        owner: User,
        alias: str,
        limit: Amount,
        is_enabled: bool,
    ):
        super().__init__(id)
        self.owner = owner
        self.alias = alias
        self.limit = limit
        self.is_enabled = is_enabled

    @abstractmethod
    def get_payments(self, month: int | None = None, year: int | None = None) -> list['Payment']:
        'Get all payments for this account in a given month and year.'
        ...
