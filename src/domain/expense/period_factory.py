from datetime import date
from uuid import UUID

from ..shared import EntityFactoryBase, Amount
from .payment_factory import PaymentFactory


class PeriodFactory(EntityFactoryBase):
    
    @staticmethod
    def create(**kwargs):
        from .period import Period

        id: UUID | None = kwargs.get('id')
        month: int | None = kwargs.get('month')
        year: int | None = kwargs.get('year')
        payment_list: list | None = kwargs.get('payments')

        # Validations
        if id is None or not isinstance(id, UUID):
            raise ValueError(f'id must be a UUID, got {type(id)}')
        if month is None or not isinstance(month, int) or not (1 <= month <= 12):
            raise ValueError('month must be an integer between 1 and 12')
        if year is None or not isinstance(year, int) or year < 2000:
            raise ValueError('year must be a positive integer greater than 2000')
        if payment_list is None or not isinstance(payment_list, list):
            raise ValueError('payments must be a list')
        payments = []
        for payment_data in payment_list:
            if not isinstance(payment_data, dict):
                raise ValueError('each payment must be a dictionary')
            payment = PaymentFactory.create(**payment_data)
            payments.append(payment)

        return Period(
            id=id,
            month=month,
            year=year,
            payments=payments
        )