from abc import ABC, abstractmethod

from src.domain.shared import EntityBase

from typing import Generic, TypeVar

T = TypeVar('T', bound=EntityBase)


class BaseRepository(Generic[T], ABC):
    @abstractmethod
    def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def count_by_filter(self, filter: dict) -> int:
        pass

    @abstractmethod
    def get_many_by_filter(self, filter: dict, limit: int, offset: int) -> list[T]:
        pass

    @abstractmethod
    def get_by_filter(self, filter: dict) -> T | None:
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        pass

    @abstractmethod
    def delete_by_filter(self, filter: dict) -> None:
        pass
