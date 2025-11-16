from abc import ABC, abstractmethod

from .entity_base import EntityBase

class EntityFactoryBase(ABC):
    '''Base class for entity factories.'''

    @staticmethod
    @abstractmethod
    def create(*args, **kwargs) -> EntityBase:
        '''Create an entity instance with the given attributes.'''
        ...
