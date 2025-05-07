from .base_repository import BaseRepository
from .account_repository import AccountRepository
from app.database.models import CreditCardModel, AccountModel
from app.core.enums import SortableCreditCardFieldsEnum


class CreditCardRepository(BaseRepository[CreditCardModel]):
    VALID_ORDER_BY_FIELDS: list[str] = [field.value for field in SortableCreditCardFieldsEnum]

    def __init__(self) -> None:
        super().__init__()
        self.model = CreditCardModel
        self.account_repository = AccountRepository()

    def _get_filter_params(self, params: dict = ...) -> dict:
        user_id = params.get('user_id')
        is_enabled = params.get('is_enabled')
        main_credit_card_id = params.get('main_credit_card_id')
        filter_params = {
            'main_credit_card_id': main_credit_card_id,
        }
        if user_id is not None:
            filter_params['user_id'] = user_id
        if is_enabled is not None:
            filter_params['is_enabled'] = is_enabled
        return filter_params

    def delete(self, cc_id):
        query = self.db.query(AccountModel).filter(AccountModel.id == cc_id)
        count = query.delete(synchronize_session=False)
        self.db.commit()
        return count
        # super().delete(search_filter)
        # return self.account_repository.delete(search_filter)
