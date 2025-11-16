from typing import TypeVar

from src.domain.expense import Expense
from .base_repository import BaseRepository


T = TypeVar('T', bound=Expense)


class ExpenseRepository(BaseRepository[T]):
    pass
