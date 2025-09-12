
from uuid import UUID
from abc import ABC, abstractmethod


class EntityBase(ABC):
    def __init__(self, id: UUID):
        self.id = id

    @abstractmethod
    def to_dict(self, *args, **kwargs) -> dict:
        '''Convert the entity to a dictionary representation.'''
        ...
