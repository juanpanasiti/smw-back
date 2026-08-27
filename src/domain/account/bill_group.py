from functools import reduce
from uuid import UUID
from typing import TYPE_CHECKING
from collections import defaultdict

from ..shared import Amount, Month, Year
from .account import Account
from .enums import AccountType


if TYPE_CHECKING:
    from ..expense import Payment, Bill, BillFrequency


class BillGroup(Account):
    """
    BillGroup is a logical container for organizing bills by category.

    Examples:
    - BillGroup("Casa y Auto")
        ├── Bill("Edenor - Luz", $8,500, MONTHLY)
        ├── Bill("Aysa - Agua", $2,100, MONTHLY)
        ├── Bill("Metrogas", $5,300, BIMONTHLY)
        └── Bill("Patente Auto", $125,000, ANNUAL)

    - BillGroup("Trabajo")
        ├── Bill("Monotributo", $85,000, MONTHLY)
        ├── Bill("Clases Inglés", $48,000, SPORADIC)
        └── Bill("Contador", $30,000, QUARTERLY)

    - BillGroup("Salud")
        ├── Bill("OSDE", $65,000, MONTHLY)
        └── Bill("Obra Social", $25,000, MONTHLY)
    """

    AMOUNT_FIELDS = ['limit']

    def __init__(
        self,
        id: UUID,
        owner_id: UUID,
        alias: str,
        is_enabled: bool,
        expenses: list['Bill'],
    ):
        # BillGroups don't have a limit
        super().__init__(id, owner_id, alias, Amount(0), is_enabled)
        self.expenses = expenses

    @property
    def account_type(self) -> AccountType:
        """Return BILL_GROUP as the account type."""
        return AccountType.BILL_GROUP

    @property
    def total_expenses_count(self) -> int:
        """Return the total number of bills in this group."""
        return len(self.expenses)

    @property
    def total_bills_count(self) -> int:
        """Return the total number of bill expenses in this group."""
        from ..expense import ExpenseType
        return len([exp for exp in self.expenses if exp.expense_type == ExpenseType.BILL])

    @property
    def pending_bills_count(self) -> int:
        """Return the number of unpaid bills."""
        return len([exp for exp in self.expenses if not exp.is_fully_paid])

    @property
    def used_limit(self) -> Amount:
        """Calculate total pending amount (unpaid bills)."""
        return sum((exp.pending_amount for exp in self.expenses), Amount(0))

    @property
    def available_limit(self) -> Amount:
        """BillGroups don't have a limit concept."""
        return Amount(0)

    @property
    def total_paid_this_year(self) -> Amount:
        """Calculate total amount paid in bills this year."""
        from datetime import date
        current_year = date.today().year
        total = Amount(0)

        for expense in self.expenses:
            for payment in expense.payments:
                if payment.is_final_status and payment.payment_date.year == current_year:
                    total += payment.amount

        return total

    @property
    def bills_by_frequency(self) -> dict[str, list['Bill']]:
        """Group bills by their frequency for easier visualization."""
        grouped: dict[str, list['Bill']] = defaultdict(list)

        for expense in self.expenses:
            grouped[expense.frequency.value].append(expense)

        return dict(grouped)

    @property
    def estimated_monthly_cost(self) -> Amount:
        """
        Estimate average monthly cost of this bill group.
        Useful for budgeting and cash flow projections.
        """
        from ..expense import BillFrequency

        total = Amount(0)

        for bill in self.expenses:
            # Use the bill amount as estimation
            if bill.amount:
                # Convert to monthly based on frequency
                if bill.frequency == BillFrequency.MONTHLY:
                    total += bill.amount
                elif bill.frequency == BillFrequency.BIMONTHLY:
                    total += Amount(bill.amount.value / 2)
                elif bill.frequency == BillFrequency.QUARTERLY:
                    total += Amount(bill.amount.value / 3)
                elif bill.frequency == BillFrequency.SEMI_ANNUAL:
                    total += Amount(bill.amount.value / 6)
                elif bill.frequency == BillFrequency.ANNUAL:
                    total += Amount(bill.amount.value / 12)
                # SPORADIC and CUSTOM don't contribute to monthly estimate

        return total

    def update_from_dict(self, data: dict) -> None:
        """Update the BillGroup instance with values from a dictionary."""
        for key, value in data.items():
            if key in self.AMOUNT_FIELDS and isinstance(value, (int, float)):
                value = Amount(value)
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self, include_relationships: bool = False) -> dict:
        """Convert the BillGroup instance to a dictionary representation."""
        base_dict = super().to_dict(include_relationships)

        if include_relationships:
            expenses = [e.to_dict(include_relations=True) for e in self.expenses]
        else:
            expenses = [str(e.id) for e in self.expenses]

        base_dict.update({
            'expenses': expenses,
        })

        return base_dict

    def get_payments(self, month: Month | None = None, year: Year | None = None) -> list['Payment']:
        """Get all payments for this bill group in a given month and year."""
        if (month is None and year is not None) or (month is not None and year is None):
            raise ValueError('Both month and year must be provided together or both must be None')

        return reduce(lambda acc, exp: acc + exp.get_payments(month, year), self.expenses, [])
