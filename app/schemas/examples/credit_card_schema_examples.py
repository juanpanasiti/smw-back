CREDIT_CARD_AMOUNT_1 = {
    'single_payment_total': 12500.0,
    'installment_total': 80000.0,
    'monthly_subscriptions_total': 3400.0
}
CREDIT_CARD_AMOUNT_2 = {
    'single_payment_total': 8000.0,
    'installment_total': 20000.0,
    'monthly_subscriptions_total': 1500.0
}
CREDIT_CARD_ITEM_1 = {
    'single_payment_purchases': 5,
    'installment_purchases': 12,
    'new_installment_purchases': 3,
    'last_installment_purchases': 2,
    'subscriptions': 4
}
CREDIT_CARD_ITEM_2 = {
    'single_payment_purchases': 3,
    'installment_purchases': 5,
    'new_installment_purchases': 1,
    'last_installment_purchases': 0,
    'subscriptions': 2
}
CREDIT_CARD_ITEM_3 = {
    'single_payment_purchases': 2,
    'installment_purchases': 4,
    'new_installment_purchases': 1,
    'last_installment_purchases': 1,
    'subscriptions': 1
}


EXTENSION_CREDIT_CARD_1 = {
    'id': 2,
    'alias': 'Company Card - Laura',
    'self_amounts': CREDIT_CARD_AMOUNT_1,
    'self_items': CREDIT_CARD_ITEM_1,
    'created_at': '2024-04-01T12:30:00',
    'updated_at': '2024-04-10T08:45:00',
    'is_enabled': True
}

EXTENSION_CREDIT_CARD_2 = {
    'id': 3,
    'alias': 'Company Card - John',
    'self_amounts': CREDIT_CARD_AMOUNT_2,
    'self_items':CREDIT_CARD_ITEM_2,
    'created_at': '2024-04-02T14:00:00',
    'updated_at': '2024-04-11T09:15:00',
    'is_enabled': True
}

MAIN_CREDIT_CARD_1 = {
    'id': 1,
    'alias': 'Personal Mastercard',
    'limit': 10000,
    'financing_limit': 15000,
    'user_id': 42,
    'next_closing_date': '2024-04-28',
    'next_expiring_date': '2024-05-05',
    'main_credit_card_id': None,
    'self_amounts': CREDIT_CARD_AMOUNT_1,
    'self_items': CREDIT_CARD_ITEM_3,
    'extensions': [
        EXTENSION_CREDIT_CARD_1,
        EXTENSION_CREDIT_CARD_2,
    ],
    'created_at': '2024-01-01T10:00:00',
    'updated_at': '2024-04-01T09:00:00',
    'is_enabled': True
}

