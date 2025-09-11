
from uuid import UUID
from abc import ABC


class EntityBase(ABC):
    def __init__(self, id: UUID):
        self.id = id

    def to_dict(self, *args, **kwargs) -> dict:
        '''Convert the entity to a dictionary representation.'''
        ...
