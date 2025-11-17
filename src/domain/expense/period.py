from uuid import UUID

from ..shared import EntityBase, Amount, Month, Year
from ..account import Account
from .period_payment import PeriodPayment
from .enums import PaymentStatus


class Period(EntityBase):
    def __init__(
        self,
        id: UUID,
        month: Month,
        year: Year,
        payments: list[PeriodPayment],
    ):
        super().__init__(id)
        self.month = month
        self.year = year
        self.payments = payments

    @property
    def period_str(self) -> str:
        'Return the period in MM/YYYY format.'
        return f'{self.month:02}/{self.year}'

    @property
    def total_amount(self) -> Amount:
        'Calculate the total amount of all payments in this period.'
        total = sum(payment.amount.value for payment in self.payments)
        return Amount(total)

    @property
    def total_paid_amount(self) -> Amount:
        'Calculate the total amount of all paid payments in this period.'
        total = sum(payment.amount.value for payment in self.payments if payment.status == PaymentStatus.PAID)
        return Amount(total)
    
    @property
    def total_confirmed_amount(self) -> Amount:
        'Calculate the total amount of all confirmed/paid payments in this period.'
        confirmed_statuses = {PaymentStatus.CONFIRMED, PaymentStatus.PAID}
        total = sum(
            payment.amount.value 
            for payment in self.payments 
            if payment.status in confirmed_statuses
        )
        return Amount(total)

    @property
    def total_pending_amount(self) -> Amount:
        'Calculate the total amount of all unconfirmed payments in this period.'
        total = sum(payment.amount.value for payment in self.payments if payment.status == PaymentStatus.UNCONFIRMED)
        return Amount(total)

    @property
    def pending_payments(self) -> list[PeriodPayment]:
        'Return a list of payments that are not in a final status.'
        return [payment for payment in self.payments if not payment.is_final_status]

    @property
    def completed_payments(self) -> list[PeriodPayment]:
        'Return a list of payments that are in a final status.'
        return [payment for payment in self.payments if payment.is_final_status]

    @property
    def total_payments(self) -> int:
        'Return the total number of payments in this period.'
        return len(self.payments)

    def to_dict(self, include_relationships: bool = False) -> dict:
        '''Convert the Period instance to a dictionary representation.'''
        return {
            'id': str(self.id),
            'month': self.month,
            'year': self.year,
            'payments': [p.to_dict() for p in self.payments] if include_relationships else [str(p.payment_id) for p in self.payments],
        }
    
    def add_payment(self, payment: PeriodPayment):
        'Add a payment to the period.'
        if not isinstance(payment, PeriodPayment):
            raise ValueError('payment must be an instance of PeriodPayment')
        existing_payment = next((p for p in self.payments if p.payment_id == payment.payment_id), None)
        if not existing_payment:
            self.payments.append(payment)

    def fill_from_account(self, account: Account, expenses: list | None = None):
        """
        Fill the period with payments from the given account.
        
        For subscriptions, if the last payment is before this period and the subscription
        is still active, a simulated payment will be added.
        
        Args:
            account: Account entity (e.g., CreditCard)
            expenses: Optional list of expenses. If None and account has expenses attribute, uses it.
        """
        from .period_payment_factory import PeriodPaymentFactory
        from .enums import ExpenseType, ExpenseStatus, PaymentStatus
        from datetime import date
        from uuid import uuid4
        
        # Try to get expenses from account if not provided
        if expenses is None:
            expenses = getattr(account, 'expenses', [])
        
        # Ensure expenses is a list at this point
        expenses_list = expenses if expenses is not None else []
        
        # Create a mapping of expense_id -> expense for quick lookup
        expense_map = {exp.id: exp for exp in expenses_list}
        
        # 1. Add real payments from the account
        real_payments_expense_ids = set()
        for payment in account.get_payments(self.month, self.year):
            # Get the expense associated with this payment
            expense = expense_map.get(payment.expense_id)
            if not expense:
                continue
            
            # Track which expenses have real payments in this period
            real_payments_expense_ids.add(expense.id)
            
            # Get category name if exists
            category_name = None  # TODO: fetch from category repository if needed
            
            # Create PeriodPayment
            period_payment = PeriodPaymentFactory.create_from_entities(
                payment=payment,
                expense=expense,
                account=account,
                category_name=category_name,
            )
            
            try:
                self.add_payment(period_payment)
            except ValueError:
                continue
        
        # 2. Check subscriptions for simulated payments
        for expense in expenses_list:
            # Only process subscriptions
            if expense.expense_type != ExpenseType.SUBSCRIPTION:
                continue
            
            # Skip if this subscription already has a real payment in this period
            if expense.id in real_payments_expense_ids:
                continue
            
            # Skip if subscription is not active
            if expense.status not in {ExpenseStatus.ACTIVE, ExpenseStatus.PENDING}:
                continue
            
            # Check if this subscription should have a payment in this period
            # A subscription should have a simulated payment if:
            # 1. It has at least one payment (it has started)
            # 2. The last payment is in a period before this one
            if not expense.payments:
                continue
            
            # Get the last payment date
            last_payment = max(expense.payments, key=lambda p: p.payment_date)
            last_payment_date = last_payment.payment_date
            
            # Calculate if this period comes after the last payment
            period_date = date(self.year, self.month, 1)
            last_payment_period_date = date(
                last_payment_date.year, 
                last_payment_date.month, 
                1
            )
            
            # If this period is after the last payment period, create simulated payment
            if period_date > last_payment_period_date:
                # Calculate the payment date for this period (same day as first payment)
                payment_day = expense.first_payment_date.day
                # Adjust day if it exceeds the month's days
                from calendar import monthrange
                max_day = monthrange(self.year, self.month)[1]
                payment_day = min(payment_day, max_day)
                
                simulated_payment_date = date(self.year, self.month, payment_day)
                
                # Calculate installment number (subscriptions continue indefinitely)
                months_diff = (self.year - last_payment_date.year) * 12 + (self.month - last_payment_date.month)
                simulated_installment = last_payment.no_installment + months_diff
                
                # Create simulated PeriodPayment
                from .payment import Payment
                simulated_payment = Payment(
                    id=uuid4(),  # Temporary ID (not persisted)
                    expense_id=expense.id,
                    amount=expense.amount,
                    no_installment=simulated_installment,
                    status=PaymentStatus.SIMULATED,
                    payment_date=simulated_payment_date,
                    is_last_payment=False,  # Subscriptions don't have a last payment
                )
                
                category_name = None  # TODO: fetch from category repository if needed
                
                simulated_period_payment = PeriodPaymentFactory.create_from_entities(
                    payment=simulated_payment,
                    expense=expense,
                    account=account,
                    category_name=category_name,
                )
                
                try:
                    self.add_payment(simulated_period_payment)
                except ValueError:
                    continue
