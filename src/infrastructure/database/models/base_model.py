import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=None,
        unique=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def to_dict(self, include_relationships: bool = False) -> dict:
        data = {
            column.name: getattr(self, column.name)
            for column in self.__class__.__table__.columns
        }
        if include_relationships:
            for relationship in self.__mapper__.relationships:
                related_value = getattr(self, relationship.key)
                data[relationship.key] = (
                    [item.to_dict() for item in related_value]
                    if isinstance(related_value, list)
                    else related_value.to_dict() if related_value
                    else None
                )
        return data

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} id={self.id}>'
