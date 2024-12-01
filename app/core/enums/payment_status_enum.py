from enum import Enum


class PaymentStatusEnum(str, Enum):
    UNCONFIRMED = 'unconfirmed'
    CONFIRMED = 'confirmed'
    PAID = 'paid'
    CANCELED = 'canceled'
    SIMULATED = 'simulated'


FINISHED_PAYMENT_STATUSES = [PaymentStatusEnum.PAID, PaymentStatusEnum.CANCELED]
