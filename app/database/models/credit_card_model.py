from datetime import date

from sqlalchemy import String, Date, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import BaseModel


class CreditCardModel(BaseModel):
    __tablename__= 'credit_cards'

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    closing_date: Mapped[date] = mapped_column(Date(), default=date.today(), nullable=False)
    expiring_date: Mapped[date] = mapped_column(Date(), default=date.today(), nullable=False)
    limit: Mapped[float] = mapped_column(Float(precision=2), default=0.0, nullable=False)

    main_credit_card_id: Mapped[int] = mapped_column(Integer, ForeignKey('credit_cards.id'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    # Relationships
    # extensions = relationship('CreditCardModel', back_populates='main_credit_card')

    def __repr__(self) -> str:
        return f'CreditCard {self.name}'

    def __str__(self) -> str:
        return f'CreditCard {self.name}'
    
    def update_data(self, new_data):
        return super().update_data(new_data)