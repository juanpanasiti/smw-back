from enum import Enum


class PaymentStatus(str, Enum):
    UNCONFIRMED = 'unconfirmed'
    CONFIRMED = 'confirmed'
    PAID = 'paid'
    CANCELED = 'canceled'
    SIMULATED = 'simulated'
