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

    # Calculated fields
    @property
    def total_spent(self) -> float:
        total = self.subtotal_spent
        total += sum(card.subtotal_spent for card in self.extensions)
        return total

    @property
    def subtotal_spent(self) -> float:
        return sum(expense.remaining_amount for expense in self.expenses)

    __mapper_args__ = {
        'polymorphic_identity': 'credit_card'
    }

    def to_dict(self, include_relationships=False):
        credit_card_dict = {
            'id': self.account_id,
            'alias': self.alias,
            'limit': self.limit,
            'financing_limit': self.financing_limit,
            'is_enabled': self.is_enabled,
            'type': self.type,
            'user_id': self.user_id,
            'main_credit_card_id': self.main_credit_card_id,
            'next_closing_date': self.next_closing_date,
            'next_expiring_date': self.next_expiring_date,
            'subtotal_spent': self.subtotal_spent,
            'total_spent': self.total_spent,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
        return credit_card_dict
