from abc import ABC
from uuid import UUID

from ..shared import Amount, EntityBase
from ..auth import User


class Account(EntityBase, ABC):
    def __init__(
        self,
        id: UUID,
        owner: User,
        alias: str,
        limit: Amount,
        is_enabled: bool,
    ):
        super().__init__(id)
        self.owner = owner
        self.alias = alias
        self.limit = limit
        self.is_enabled = is_enabled
