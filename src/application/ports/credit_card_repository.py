from abc import ABC, abstractmethod

from src.domain.account import CreditCard


class CreditCardRepository(ABC):
    @abstractmethod
    def create(self, credit_card: CreditCard) -> CreditCard:
        pass

    @abstractmethod
    def count_by_filter(self, filter: dict) -> int:
        pass

    @abstractmethod
    def get_many_by_filter(self, filter: dict) -> list[CreditCard]:
        pass

    @abstractmethod
    def get_by_filter(self, filter: dict) -> CreditCard | None:
        pass

    @abstractmethod
    def update(self, credit_card: CreditCard) -> CreditCard:
        pass

    @abstractmethod
    def delete_by_filter(self, filter: dict) -> None:
        pass
