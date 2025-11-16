from uuid import UUID

from ..shared import EntityFactoryBase, Month, Year
from .payment_factory import PaymentFactory


class PeriodFactory(EntityFactoryBase):
    
    @staticmethod
    def create(**kwargs):
        from .period import Period

        id: UUID | None = kwargs.get('id')
        month: Month | None = kwargs.get('month')
        year: Year | None = kwargs.get('year')
        payment_list: list | None = kwargs.get('payments')

        # Validations
        if id is None or not isinstance(id, UUID):
            raise ValueError(f'id must be a UUID, got {type(id)}')
        if month is None or not isinstance(month, Month):
            raise ValueError('month must be a Month or an integer between 1 and 12')
        if year is None or not isinstance(year, Year):
            raise ValueError('year must be a Year or an integer greater than 2000')
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