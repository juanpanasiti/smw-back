
from uuid import UUID
from abc import ABC, abstractmethod


class EntityBase(ABC):
    def __init__(self, id: UUID):
        self.id = id

    def to_dict(self, *args, **kwargs) -> dict:
        '''Convert the entity to a dictionary representation.'''
        ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> 'EntityBase':
        '''Create an entity instance from a dictionary representation.'''
        ...
