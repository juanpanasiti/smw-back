import uuid

from sqlalchemy import String, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column


from . import BaseModel


class ExpenseCategoryModel(BaseModel):
    __tablename__ = 'expense_categories'

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), default='')
    is_income: Mapped[bool] = mapped_column(default=False)

    # FKs
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
