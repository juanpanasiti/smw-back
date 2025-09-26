from abc import ABC, abstractmethod

from src.domain.expense import ExpenseCategory


class ExpenseCategoryRepository(ABC):
    @abstractmethod
    def create(self, expense_category: ExpenseCategory) -> ExpenseCategory:
        pass

    @abstractmethod
    def count_by_filter(self, filter: dict) -> int:
        pass

    @abstractmethod
    def get_many_by_filter(self, filter: dict, limit: int, offset: int) -> list[ExpenseCategory]:
        pass

    @abstractmethod
    def get_by_filter(self, filter: dict) -> ExpenseCategory | None:
        pass

    @abstractmethod
    def update(self, expense: ExpenseCategory) -> ExpenseCategory:
        pass

    @abstractmethod
    def delete_by_filter(self, filter: dict) -> None:
        pass
