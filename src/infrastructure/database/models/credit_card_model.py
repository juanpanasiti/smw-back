from datetime import date

from sqlalchemy import Integer, ForeignKey, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import AccountModel


class CreditCardModel(AccountModel):
    __tablename__ = 'credit_cards'

    account_id: Mapped[int] = mapped_column(Integer, ForeignKey('accounts.id', ondelete='CASCADE'), primary_key=True)
    main_credit_card_id: Mapped[int] = mapped_column(Integer, ForeignKey('credit_cards.account_id'), nullable=True)
    next_closing_date: Mapped[date] = mapped_column(Date(), nullable=True)
    next_expiring_date: Mapped[date] = mapped_column(Date(), nullable=True)
    financing_limit: Mapped[float] = mapped_column(Numeric(precision=20, scale=2), default=0.0, nullable=True)

    # Relationships
    main_credit_card: Mapped['CreditCardModel'] = relationship(
        'CreditCardModel',
        remote_side=[account_id],
        foreign_keys=[main_credit_card_id],
        back_populates='extensions',
    )

    extensions: Mapped[list['CreditCardModel']] = relationship(
        'CreditCardModel',
        back_populates='main_credit_card',
        foreign_keys=[main_credit_card_id],
        cascade='all, delete-orphan',
    )

    __mapper_args__ = {
        'polymorphic_identity': 'credit_card'
    }
