from uuid import UUID

from src.application.dtos import PeriodResponseDTO, PeriodSummaryDTO
from src.application.use_cases.period import PeriodGetOneUseCase, PeriodGetRangeUseCase
from src.application.ports import CreditCardRepository


class PeriodController:
    """Controller for period operations."""
    
    def __init__(
        self,
        credit_card_repository: CreditCardRepository,
    ):
        self._credit_card_repository = credit_card_repository
    
    def get_period(self, user_id: UUID, month: int, year: int) -> PeriodResponseDTO:
        """Get a specific period with enriched payments."""
        use_case = PeriodGetOneUseCase(
            self._credit_card_repository,
        )
        return use_case.execute(user_id, month, year)
    
    def get_periods_projection(
        self, 
        user_id: UUID, 
        months_ahead: int
    ) -> list[PeriodResponseDTO]:
        """Get future period projection with complete payments."""
        use_case = PeriodGetRangeUseCase(
            self._credit_card_repository,
        )
        return use_case.execute(user_id, months_ahead)
