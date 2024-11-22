from datetime import date

from sqlalchemy import Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import AccountModel

class CreditCardModel(AccountModel):
    __tablename__ = 'credit_cards'

    account_id: Mapped[int] = mapped_column(Integer, ForeignKey('accounts.id'), primary_key=True)
    main_credit_card_id: Mapped[int] = mapped_column(Integer, ForeignKey('credit_cards.account_id'), nullable=True)
    next_closing_date: Mapped[date] = mapped_column(Date(), nullable=True)
    next_expiring_date: Mapped[date] = mapped_column(Date(), nullable=True)

    # Relationships
    main_credit_card: Mapped['CreditCardModel'] = relationship(
        'CreditCardModel', 
        backref='sub_cards', 
        remote_side=[account_id]
    )

    # Calculated fields
    @property
    def total_spent(self) -> float:
        return sum(expense.remaining_amount for expense in self.expenses)

    __mapper_args__ = {
        'polymorphic_identity': 'credit_card'
    }
