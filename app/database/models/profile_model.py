from sqlalchemy import String, Integer, Float, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel


class ProfileModel(BaseModel):
    __tablename__ = 'profiles'

    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    spent_alert: Mapped[float] = mapped_column(Float(precision=2), default=0.0, server_default="0.0", nullable=False)
    monthly_payment_alert: Mapped[float] = mapped_column(Float(precision=2), default=0.0, server_default="0.0", nullable=False)

    # PKs
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
