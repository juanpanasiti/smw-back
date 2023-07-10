from typing import List

from sqlalchemy import String, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import BaseModel


class CreditCardModel(BaseModel):
    __tablename__ = 'credit_cards'

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    limit: Mapped[float] = mapped_column(Float(precision=2), default=0.0, nullable=False)

    main_credit_card_id: Mapped[int] = mapped_column(Integer, ForeignKey('credit_cards.id'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    # Relationships
    extensions: Mapped[List['CreditCardModel']] = relationship(back_populates='main_credit_card')
    main_credit_card: Mapped['CreditCardModel'] = relationship(back_populates='extensions')

    def __repr__(self) -> str:
        return f'CreditCard {self.name}'

    def __str__(self) -> str:
        return f'CreditCard {self.name}'
