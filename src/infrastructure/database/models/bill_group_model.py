import uuid

from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column

from . import AccountModel


class BillGroupModel(AccountModel):
    """Model for bill groups (containers for bills like utilities, taxes, services)."""
    
    __tablename__ = 'bill_groups'

    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey('accounts.id', ondelete='CASCADE'), 
        primary_key=True
    )

    __mapper_args__ = {
        'polymorphic_identity': 'bill_group'
    }
