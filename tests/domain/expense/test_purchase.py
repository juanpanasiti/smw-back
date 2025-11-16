import copy
from uuid import uuid4
from datetime import date

import pytest

from src.domain.expense import Purchase, Payment, PaymentStatus, ExpenseStatus
from src.domain.shared import Amount


@pytest.fixture
def purchase() -> Purchase:
    return Purchase(
        id=uuid4(),
        account_id=uuid4(),
        title='Laptop',
        cc_name='A new laptop for work',
        acquired_at=date.today(),
        amount=Amount(1500),
        installments=3,
        first_payment_date=date.today(),
        category_id=uuid4(),
        payments=[],
    )


def test_is_one_time_payment(purchase: Purchase):
    assert purchase.is_one_time_payment is False  # 3 installments
    purchase.installments = 1
    assert purchase.is_one_time_payment is True


def test_number_of_payments(purchase: Purchase):
    assert len(purchase.payments) == 3  # Should have 3 payments for 3 installments


def test_paid_and_pending_installments(purchase: Purchase):
    # Initially, no payments are made
    paid_amount = Amount(0)
    pending_amount = purchase.amount
    assert len(purchase.payments) == 3
    assert purchase.paid_amount == paid_amount
    assert purchase.pending_installments == 3
    assert purchase.done_installments == 0
    assert purchase.pending_amount == pending_amount
    assert purchase.pending_financing_amount == pending_amount
    for payment in purchase.payments:
        assert payment.status == PaymentStatus.UNCONFIRMED
    assert purchase.status == ExpenseStatus.PENDING

    # Simulate paying the first installment
    payment_0 = copy.deepcopy(purchase.payments[0])
    payment_0.status = PaymentStatus.PAID
    purchase.update_payment(payment_0)
    paid_amount += payment_0.amount
    pending_amount -= payment_0.amount
    assert purchase.paid_amount == paid_amount
    assert purchase.pending_installments == 2
    assert purchase.done_installments == 1
    assert purchase.payments[0].is_final_status is True
    assert purchase.payments[1].is_final_status is False
    assert purchase.payments[2].is_final_status is False
    assert purchase.pending_amount == pending_amount
    assert purchase.pending_financing_amount == pending_amount
    assert purchase.status == ExpenseStatus.PENDING

    # Simulate paying the second installment
    payment_1 = copy.deepcopy(purchase.payments[1])
    payment_1.status = PaymentStatus.PAID
    purchase.update_payment(payment_1)
    paid_amount += payment_1.amount
    pending_amount -= payment_1.amount
    assert purchase.paid_amount == paid_amount
    assert purchase.pending_installments == 1
    assert purchase.done_installments == 2
    assert purchase.payments[0].is_final_status is True
    assert purchase.payments[1].is_final_status is True
    assert purchase.payments[2].is_final_status is False
    assert purchase.pending_amount == pending_amount
    assert purchase.pending_financing_amount == pending_amount
    assert purchase.status == ExpenseStatus.PENDING

    # Simulate paying the last installment
    payment_2 = copy.deepcopy(purchase.payments[2])
    payment_2.status = PaymentStatus.PAID
    purchase.update_payment(payment_2)
    paid_amount += payment_2.amount
    pending_amount -= payment_2.amount
    assert purchase.paid_amount == paid_amount
    assert purchase.pending_installments == 0
    assert purchase.done_installments == 3
    assert purchase.payments[0].is_final_status is True
    assert purchase.payments[1].is_final_status is True
    assert purchase.payments[2].is_final_status is True
    assert purchase.pending_amount == pending_amount
    assert purchase.pending_amount.value == 0.0
    assert purchase.pending_financing_amount.value == 0.0
    assert purchase.status == ExpenseStatus.FINISHED


def test_update_payment_rebalances_non_final_amounts(purchase: Purchase):
    # Create a fresh purchase with 1000 total
    test_purchase = Purchase(
        id=uuid4(),
        account_id=uuid4(),
        title='Test Purchase',
        cc_name='Test Card',
        acquired_at=date.today(),
        amount=Amount(1000),
        installments=3,
        first_payment_date=date.today(),
        category_id=uuid4(),
        payments=[],
    )
    
    # Verify initial distribution: 333.33, 333.34, 333.33
    assert len(test_purchase.payments) == 3
    total_check = sum(p.amount.value for p in test_purchase.payments)
    assert total_check == pytest.approx(1000.0)

    # Now update first payment from 333.33 to 333.34
    updated_payment = copy.deepcopy(test_purchase.payments[0])
    updated_payment.amount = Amount(333.34)
    test_purchase.update_payment(updated_payment)

    # After update: first=333.34, others should be 333.33 each
    assert test_purchase.payments[0].amount.value == pytest.approx(333.34)
    assert test_purchase.payments[1].amount.value == pytest.approx(333.33)
    assert test_purchase.payments[2].amount.value == pytest.approx(333.33)
    assert sum(p.amount.value for p in test_purchase.payments) == pytest.approx(1000.0)


def test_update_payment_does_not_change_finalized_amounts(purchase: Purchase):
    paid_payment = copy.deepcopy(purchase.payments[0])
    paid_payment.status = PaymentStatus.PAID
    purchase.update_payment(paid_payment)

    frozen_amount = purchase.payments[0].amount.value

    updated_payment = copy.deepcopy(purchase.payments[1])
    updated_payment.amount = Amount(450)
    purchase.update_payment(updated_payment)

    assert purchase.payments[0].amount.value == pytest.approx(frozen_amount)
    expected_last_amount = purchase.amount.value - frozen_amount - updated_payment.amount.value
    assert purchase.payments[2].amount.value == pytest.approx(expected_last_amount)


def test_update_payment_raises_when_exceeding_pending_amount(purchase: Purchase):
    updated_payment = copy.deepcopy(purchase.payments[0])
    updated_payment.amount = Amount(purchase.amount.value + 10)

    with pytest.raises(ValueError):
        purchase.update_payment(updated_payment)


def test_update_payment_raises_when_payment_not_found():
    """Test that updating a non-existent payment raises PaymentNotFoundInExpenseException."""
    from src.domain.expense.exceptions import PaymentNotFoundInExpenseException
    
    purchase = Purchase(
        id=uuid4(),
        account_id=uuid4(),
        title='Test Purchase',
        cc_name='Test Card',
        acquired_at=date.today(),
        amount=Amount(1000),
        installments=3,
        first_payment_date=date.today(),
        category_id=uuid4(),
        payments=[]
    )
    purchase.calculate_payments()
    
    # Create a payment with a different ID (not in purchase)
    non_existent_payment = Payment(
        id=uuid4(),  # Different ID
        expense_id=purchase.id,
        amount=Amount(500),
        no_installment=1,
        status=PaymentStatus.UNCONFIRMED,
        payment_date=date.today(),
        is_last_payment=False
    )
    
    with pytest.raises(PaymentNotFoundInExpenseException, match='Payment with id .* not found in purchase'):
        purchase.update_payment(non_existent_payment)


def test_calculate_payments(purchase: Purchase):
    # Create a purchase with 5 installments
    purchase.installments = 5
    purchase.payments = []
    purchase.calculate_payments()
    assert len(purchase.payments) == 5
    total_amount = sum(payment.amount.value for payment in purchase.payments)
    assert total_amount == pytest.approx(purchase.amount.value)

    # Create a purchase with 1 installment
    purchase.installments = 1
    purchase.payments = []
    purchase.calculate_payments()
    assert len(purchase.payments) == 1
    total_amount = sum(payment.amount.value for payment in purchase.payments)
    assert total_amount == pytest.approx(purchase.amount.value)


def test_to_dict(purchase: Purchase):
    purchase_dict = purchase.to_dict()
    assert purchase_dict['id'] == str(purchase.id)
    assert purchase_dict['title'] == purchase.title
    assert purchase_dict['cc_name'] == purchase.cc_name
    assert purchase_dict['acquired_at'] == purchase.acquired_at.isoformat()
    assert purchase_dict['amount'] == purchase.amount.value
    assert purchase_dict['installments'] == purchase.installments
    assert purchase_dict['first_payment_date'] == purchase.first_payment_date.isoformat()
    assert len(purchase_dict['payments']) == len(purchase.payments)
    assert purchase_dict['status'] == purchase.status.value
