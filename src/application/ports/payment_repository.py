from abc import ABC, abstractmethod

from src.domain.expense import Payment


class PaymentRepository(ABC):
    @abstractmethod
    def create(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    def count_by_filter(self, filter: dict) -> int:
        pass

    @abstractmethod
    def get_many_by_filter(self, filter: dict, limit: int, offset: int) -> list[Payment]:
        pass

    @abstractmethod
    def get_by_filter(self, filter: dict) -> Payment | None:
        pass

    @abstractmethod
    def update(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    def delete_by_filter(self, filter: dict) -> None:
        pass