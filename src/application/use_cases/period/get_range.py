from uuid import UUID, uuid4
from datetime import date, timedelta

from src.application.dtos import PeriodResponseDTO, PeriodPaymentDTO
from src.application.ports import CreditCardRepository
from src.domain.expense import PeriodFactory
from src.domain.shared import Month, Year


class PeriodGetRangeUseCase:
    """Obtiene un rango de períodos (para gráficos de proyección)."""
    
    def __init__(
        self,
        credit_card_repository: CreditCardRepository,
    ):
        self.credit_card_repository = credit_card_repository
    
    def execute(
        self, 
        user_id: UUID, 
        months_ahead: int = 12
    ) -> list[PeriodResponseDTO]:
        """
        Obtiene períodos futuros completos con payments enriquecidos para proyecciones.
        
        Args:
            user_id: ID del usuario
            months_ahead: Cantidad de meses hacia adelante (default: 12)
            
        Returns:
            Lista de PeriodResponseDTO con payments enriquecidos
        """
        current_date = date.today()
        periods = []
        
        # Obtener todas las tarjetas del usuario una sola vez
        credit_cards = self.credit_card_repository.get_many_by_filter(
            filter={'owner_id': user_id},
            limit=1000,  # Get all cards
            offset=0,
        )
        
        for i in range(months_ahead):
            # Calculate target month/year
            target_month = current_date.month + i
            target_year = current_date.year
            
            while target_month > 12:
                target_month -= 12
                target_year += 1
            
            month = Month(target_month)
            year = Year(target_year)
            
            # Crear período con UUID generado
            period = PeriodFactory.create(
                id=uuid4(),
                month=month,
                year=year,
                payments=[],
            )
            
            # Llenar con payments de todas las tarjetas
            for card in credit_cards:
                period.fill_from_account(card)
            
            # Convertir PeriodPayments a DTOs
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
            
            # Crear response completo
            period_response = PeriodResponseDTO(
                id=period.id,
                period_str=period.period_str,
                month=target_month,
                year=target_year,
                total_amount=period.total_amount.value,
                total_confirmed_amount=period.total_confirmed_amount.value,
                total_paid_amount=period.total_paid_amount.value,
                total_pending_amount=period.total_pending_amount.value,
                total_payments=period.total_payments,
                pending_payments_count=len(period.pending_payments),
                completed_payments_count=len(period.completed_payments),
                payments=payment_dtos,
            )
            
            periods.append(period_response)
        
        return periods
