from uuid import UUID, uuid4

from src.application.dtos import PeriodResponseDTO, PeriodPaymentDTO
from src.application.ports import CreditCardRepository
from src.domain.expense import PeriodFactory
from src.domain.shared import Month, Year


class PeriodGetOneUseCase:
    """Get a specific period with all enriched payments."""
    
    def __init__(
        self,
        credit_card_repository: CreditCardRepository,
    ):
        self.credit_card_repository = credit_card_repository
    
    def execute(self, user_id: UUID, month: int, year: int) -> PeriodResponseDTO:
        """
        Get period with enriched payments.
        
        Args:
            user_id: Owner user ID
            month: Period month (1-12)
            year: Period year
            
        Returns:
            PeriodResponseDTO with enriched payments
        """
        period_month = Month(month)
        period_year = Year(year)
        
        # 1. Get all user's credit cards with their expenses
        credit_cards = self.credit_card_repository.get_many_by_filter(
            filter={'owner_id': user_id},
            limit=1000,  # Get all cards
            offset=0,
        )
        
        # 2. Create period with generated UUID
        period = PeriodFactory.create(
            id=uuid4(),
            month=period_month,
            year=period_year,
            payments=[],
        )
        
        # 3. Fill period with payments from all credit cards
        for card in credit_cards:
            period.fill_from_account(card)
        
        # 4. Convertir PeriodPayments a DTOs
        payment_dtos = [
            PeriodPaymentDTO(
                # Payment data
                payment_id=pp.payment_id,
                amount=pp.amount.value,
                status=pp.status,
                payment_date=pp.payment_date,
                no_installment=pp.no_installment,
                is_last_payment=pp.is_last_payment,
                
                # Expense data
                expense_id=pp.expense_id,
                expense_title=pp.expense_title,
                expense_cc_name=pp.expense_cc_name,
                expense_acquired_at=pp.expense_acquired_at,
                expense_installments=pp.expense_installments,
                expense_status=pp.expense_status,
                expense_category_name=pp.expense_category_name,
                
                # Account data
                account_id=pp.account_id,
                account_alias=pp.account_alias,
                account_is_enabled=pp.account_is_enabled,
                account_type=pp.account_type,
            )
            for pp in period.payments
        ]
        
        # 5. Construir response
        return PeriodResponseDTO(
            id=period.id,
            period_str=period.period_str,
            month=month,
            year=year,
            total_amount=period.total_amount.value,
            total_confirmed_amount=period.total_confirmed_amount.value,
            total_paid_amount=period.total_paid_amount.value,
            total_pending_amount=period.total_pending_amount.value,
            total_payments=period.total_payments,
            pending_payments_count=len(period.pending_payments),
            completed_payments_count=len(period.completed_payments),
            payments=payment_dtos,
        )
