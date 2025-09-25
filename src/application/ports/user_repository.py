from abc import ABC, abstractmethod

from src.domain.auth import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def count_by_filter(self, filter: dict) -> int:
        pass

    @abstractmethod
    def get_many_by_filter(self, filter: dict) -> list[User]:
        pass

    @abstractmethod
    def get_by_filter(self, filter: dict) -> User | None:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def delete_by_filter(self, filter: dict):
        pass
