from abc import abstractmethod
from typing import TYPE_CHECKING
from uuid import UUID

from src.domain.expense import Bill
from .base_repository import BaseRepository


class BillRepository(BaseRepository[Bill]):

    @abstractmethod
    def get_upcoming_bills(
        self,
        owner_id: UUID,
        year: int | None = None,
        month: int | None = None
    ) -> list[Bill]:
        """Get upcoming bills for a specific period."""
        pass
