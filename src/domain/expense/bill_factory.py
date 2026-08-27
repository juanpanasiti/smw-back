from uuid import UUID
from datetime import date
from typing import TYPE_CHECKING

from ..shared import Amount
from .bill import Bill
from .enums import BillFrequency
from .payment import Payment


if TYPE_CHECKING:
    pass


class BillFactory:
    """Factory for creating Bill expense instances."""

    @staticmethod
    def create(
        id: UUID,
        account_id: UUID,
        description: str,
        amount: float | Amount,
        date: date,
        frequency: BillFrequency | str = BillFrequency.MONTHLY,
        next_bill_month: int | None = None,
        next_bill_year: int | None = None,
        notes: str = '',
        payments: list[Payment] | None = None,
        **kwargs,  # Ignore extra fields for flexibility
    ) -> Bill:
        """
        Create a new Bill instance.

        Args:
            id: Unique identifier for the bill
            account_id: BillGroup this bill belongs to
            description: Service name (e.g., "Edenor", "Aysa", "Monotributo")
            amount: Amount of THIS specific bill instance
            date: Date when the bill was issued
            frequency: How often this bill recurs (default: MONTHLY)
            next_bill_month: Month when next bill is expected (1-12, optional)
            next_bill_year: Year when next bill is expected (optional)
            notes: Optional notes (e.g., "Meter read around 20th", default: '')
            payments: List of payments for this bill

        Returns:
            A new Bill instance
        """
        if not isinstance(amount, Amount):
            amount = Amount(amount)

        if isinstance(frequency, str):
            frequency = BillFrequency(frequency)

        # Validate next_bill_month if provided
        if next_bill_month is not None:
            if not 1 <= next_bill_month <= 12:
                raise ValueError(f"next_bill_month must be between 1 and 12, got {next_bill_month}")
            if next_bill_year is None:
                raise ValueError("next_bill_year must be provided when next_bill_month is set")

        return Bill(
            id=id,
            account_id=account_id,
            description=description,
            amount=amount,
            date=date,
            frequency=frequency,
            next_bill_month=next_bill_month,
            next_bill_year=next_bill_year,
            notes=notes,
            payments=payments or [],
        )
