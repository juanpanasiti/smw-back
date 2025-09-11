from uuid import UUID

from ..shared import EntityBase
from ..auth import User


class ExpenseCategory(EntityBase):
    def __init__(
        self,
        id: UUID,
        owner_id: UUID,
        name: str,
        description: str,
        is_income: bool,
    ):
        super().__init__(id)
        self.name = name
        self.owner_id = owner_id
        self.description = description
        self.is_income = is_income
