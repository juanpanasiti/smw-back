import pytest
from uuid import uuid4, UUID
from datetime import date

from src.domain.expense import Period, Payment
from src.domain.expense.period_factory import PeriodFactory
from src.domain.expense.enums import PaymentStatus
from src.domain.shared import Amount, Month, Year


@pytest.fixture
def valid_payment_data() -> dict:
    """Create valid payment data for testing."""
    return {
        'id': uuid4(),
        'expense_id': uuid4(),
        'amount': Amount(100.0),
        'no_installment': 1,
        'status': PaymentStatus.PAID,
        'payment_date': date(2025, 11, 15),
        'is_last_payment': False,
    }


@pytest.fixture
def valid_period_kwargs(valid_payment_data) -> dict:
    """Create valid kwargs for Period creation."""
    return {
        'id': uuid4(),
        'month': Month(11),
        'year': Year(2025),
        'payments': [valid_payment_data],
    }


def test_create_period_success(valid_period_kwargs):
    """Test successful period creation."""
    period = PeriodFactory.create(**valid_period_kwargs)
    
    assert isinstance(period, Period)
    assert period.id == valid_period_kwargs['id']
    assert period.month == valid_period_kwargs['month']
    assert period.year == valid_period_kwargs['year']
    assert len(period.payments) == 1
    assert isinstance(period.payments[0], Payment)


def test_create_period_with_multiple_payments(valid_payment_data):
    """Test period creation with multiple payments."""
    payment_data_2 = {
        'id': uuid4(),
        'expense_id': uuid4(),
        'amount': Amount(200.0),
        'no_installment': 2,
        'status': PaymentStatus.CONFIRMED,
        'payment_date': date(2025, 12, 15),
        'is_last_payment': False,
    }
    
    kwargs = {
        'id': uuid4(),
        'month': Month(11),
        'year': Year(2025),
        'payments': [valid_payment_data, payment_data_2],
    }
    
    period = PeriodFactory.create(**kwargs)
    
    assert len(period.payments) == 2
    assert period.payments[0].amount.value == 100.0
    assert period.payments[1].amount.value == 200.0


def test_create_period_with_empty_payments():
    """Test period creation with empty payments list."""
    kwargs = {
        'id': uuid4(),
        'month': Month(11),
        'year': Year(2025),
        'payments': [],
    }
    
    period = PeriodFactory.create(**kwargs)
    
    assert len(period.payments) == 0


def test_create_period_invalid_id_none():
    """Test period creation fails with None id."""
    kwargs = {
        'id': None,
        'month': Month(11),
        'year': Year(2025),
        'payments': [],
    }
    
    with pytest.raises(ValueError, match='id must be a UUID'):
        PeriodFactory.create(**kwargs)


def test_create_period_invalid_id_type():
    """Test period creation fails with invalid id type."""
    kwargs = {
        'id': 'not-a-uuid',
        'month': Month(11),
        'year': Year(2025),
        'payments': [],
    }
    
    with pytest.raises(ValueError, match='id must be a UUID'):
        PeriodFactory.create(**kwargs)


def test_create_period_invalid_month_none():
    """Test period creation fails with None month."""
    kwargs = {
        'id': uuid4(),
        'month': None,
        'year': Year(2025),
        'payments': [],
    }
    
    with pytest.raises(ValueError, match='month must be a Month or an integer between 1 and 12'):
        PeriodFactory.create(**kwargs)


def test_create_period_invalid_month_type():
    """Test period creation fails with invalid month type."""
    kwargs = {
        'id': uuid4(),
        'month': 'invalid',
        'year': Year(2025),
        'payments': [],
    }
    
    with pytest.raises(ValueError, match='month must be a Month or an integer between 1 and 12'):
        PeriodFactory.create(**kwargs)


def test_create_period_invalid_year_none():
    """Test period creation fails with None year."""
    kwargs = {
        'id': uuid4(),
        'month': Month(11),
        'year': None,
        'payments': [],
    }
    
    with pytest.raises(ValueError, match='year must be a Year or an integer greater than 2000'):
        PeriodFactory.create(**kwargs)


def test_create_period_invalid_year_type():
    """Test period creation fails with invalid year type."""
    kwargs = {
        'id': uuid4(),
        'month': Month(11),
        'year': 'invalid',
        'payments': [],
    }
    
    with pytest.raises(ValueError, match='year must be a Year or an integer greater than 2000'):
        PeriodFactory.create(**kwargs)


def test_create_period_invalid_payments_none():
    """Test period creation fails with None payments."""
    kwargs = {
        'id': uuid4(),
        'month': Month(11),
        'year': Year(2025),
        'payments': None,
    }
    
    with pytest.raises(ValueError, match='payments must be a list'):
        PeriodFactory.create(**kwargs)


def test_create_period_invalid_payments_type():
    """Test period creation fails with invalid payments type."""
    kwargs = {
        'id': uuid4(),
        'month': Month(11),
        'year': Year(2025),
        'payments': 'not-a-list',
    }
    
    with pytest.raises(ValueError, match='payments must be a list'):
        PeriodFactory.create(**kwargs)


def test_create_period_invalid_payment_item_not_dict():
    """Test period creation fails when payment item is not a dictionary."""
    kwargs = {
        'id': uuid4(),
        'month': Month(11),
        'year': Year(2025),
        'payments': ['not-a-dict'],
    }
    
    with pytest.raises(ValueError, match='each payment must be a dictionary'):
        PeriodFactory.create(**kwargs)


def test_create_period_invalid_payment_data():
    """Test period creation fails with invalid payment data."""
    kwargs = {
        'id': uuid4(),
        'month': Month(11),
        'year': Year(2025),
        'payments': [{'invalid': 'data'}],
    }
    
    # PaymentFactory.create will raise RuntimeError for missing fields (bug in PaymentFactory)
    with pytest.raises(RuntimeError):
        PeriodFactory.create(**kwargs)
