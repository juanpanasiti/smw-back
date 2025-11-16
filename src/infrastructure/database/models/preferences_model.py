from sqlalchemy import Float, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import BaseModel


class PreferencesModel(BaseModel):
    __tablename__ = 'preferences'

    monthly_spending_limit: Mapped[float | None] = mapped_column(Float, nullable=True)
    profile_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('profiles.id'), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f'<PreferencesModel id={self.id} profile_id={self.profile_id}>'
