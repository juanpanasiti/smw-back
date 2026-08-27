from uuid import UUID
from datetime import date
from typing import TYPE_CHECKING

from ..shared import Amount, Month, Year, EntityBase
from .enums import ExpenseType, BillFrequency, PaymentStatus
from .payment import Payment


if TYPE_CHECKING:
    pass


class Bill(EntityBase):
    """
    Bill represents a recurring payment obligation with variable amounts.

    Unlike Subscription (fixed amount), Bill amounts can vary each period.
    Examples:
    - Utilities: electricity, water, gas (consumption-based)
    - Taxes: property tax, car registration (inflation-adjusted)
    - Services: phone, internet (plan changes)
    - Sporadic: English classes (every X classes)

    Structure:
    Bill("Luz", $8,500, frequency=MONTHLY, next_bill_date=(2, 2025))
      └── Payment(pay_before: 2025-02-10)

    Attributes:
        frequency: How often this bill recurs
        next_bill_month: Month when next bill is expected (1-12)
        next_bill_year: Year when next bill is expected
        notes: Optional notes about the bill (e.g., "Meter read around 20th")
    """

    AMOUNT_FIELDS = ['amount']

    def __init__(
        self,
        id: UUID,
        account_id: UUID,
        description: str,
        amount: Amount,
        date: date,
        frequency: BillFrequency,
        next_bill_month: int | None,
        next_bill_year: int | None,
        notes: str,
        payments: list[Payment],
    ):
        super().__init__(id)
        self.account_id = account_id
        self.description = description
        self.amount = amount
        self.date = date
        self.frequency = frequency
        self.next_bill_month = next_bill_month
        self.next_bill_year = next_bill_year
        self.notes = notes
        self.payments = payments if payments is not None else []

    @property
    def expense_type(self) -> ExpenseType:
        """Return BILL as the expense type."""
        return ExpenseType.BILL

    @property
    def total_amount(self) -> Amount:
        """Calculate total amount of this bill."""
        return sum((p.amount for p in self.payments), Amount(0))

    @property
    def paid_amount(self) -> Amount:
        """Calculate the amount already paid."""
        return sum((p.amount for p in self.payments if p.is_final_status), Amount(0))

    @property
    def pending_amount(self) -> Amount:
        """Calculate the amount still pending."""
        return sum((p.amount for p in self.payments if not p.is_final_status), Amount(0))

    @property
    def is_fully_paid(self) -> bool:
        """Check if all payments are completed."""
        return all(p.is_final_status for p in self.payments) if self.payments else False

    @property
    def pending_financing_amount(self) -> Amount:
        """Bills don't have financing, return 0."""
        return Amount(0)

    @property
    def has_next_bill_date(self) -> bool:
        """Check if next bill date is set."""
        return self.next_bill_month is not None and self.next_bill_year is not None

    @property
    def next_bill_date_display(self) -> str | None:
        """Get next bill date as readable string (e.g., 'Febrero 2025')."""
        if not self.has_next_bill_date:
            return None

        months = [
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ]
        # Type guard already checked via has_next_bill_date
        assert self.next_bill_month is not None and self.next_bill_year is not None
        return f"{months[self.next_bill_month - 1]} {self.next_bill_year}"

    def set_next_bill_date(self, month: int, year: int) -> None:
        """
        Set the next expected bill date.

        Args:
            month: Month (1-12)
            year: Year (e.g., 2025)

        Raises:
            ValueError: If month is not between 1-12
        """
        if not 1 <= month <= 12:
            raise ValueError(f"Month must be between 1 and 12, got {month}")

        self.next_bill_month = month
        self.next_bill_year = year

    def clear_next_bill_date(self) -> None:
        """Clear the next bill date (set to None)."""
        self.next_bill_month = None
        self.next_bill_year = None

    def get_payments(self, month: Month | None = None, year: Year | None = None) -> list[Payment]:
        """Get all payments for this bill in a given month and year."""
        if (month is None and year is not None) or (month is not None and year is None):
            raise ValueError('Both month and year must be provided together or both must be None')

        if month is None and year is None:
            return self.payments

        return [
            payment for payment in self.payments
            if payment.payment_date.month == month and payment.payment_date.year == year
        ]

    def update_from_dict(self, data: dict) -> None:
        """Update the Bill instance with values from a dictionary."""
        for key, value in data.items():
            if key in self.AMOUNT_FIELDS and isinstance(value, (int, float)):
                value = Amount(value)
            if key == 'frequency' and isinstance(value, str):
                value = BillFrequency(value)
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self, include_relations: bool = False) -> dict:
        """Convert the Bill instance to a dictionary representation."""
        if include_relations:
            payments = [payment.to_dict() for payment in self.payments]
        else:
            payments = [str(payment.id) for payment in self.payments]

        return {
            'id': str(self.id),
            'account_id': str(self.account_id),
            'description': self.description,
            'amount': float(self.amount.value),
            'date': self.date.isoformat(),
            'expense_type': self.expense_type.value,
            'frequency': self.frequency.value,
            'next_bill_month': self.next_bill_month,
            'next_bill_year': self.next_bill_year,
            'notes': self.notes,
            'payments': payments,
        }

    def __repr__(self) -> str:
        return f'<Bill id={self.id} description="{self.description}" frequency={self.frequency.value}>'
