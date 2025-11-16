import pytest
from uuid import uuid4
from datetime import datetime

from src.infrastructure.database.models.base_model import BaseModel
from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.database.models.profile_model import ProfileModel  
from src.infrastructure.database.models.preferences_model import PreferencesModel
from src.infrastructure.database.models.payment_model import PaymentModel
from src.infrastructure.database.models.expense_model import ExpenseModel
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


@pytest.fixture
def db_session():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    BaseModel.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()


def test_base_model_repr():
    """Test BaseModel __repr__ method via UserModel."""
    user_id = uuid4()
    user = UserModel(id=user_id, username='testuser', email='test@example.com', password_hash='hashed', role='free_user')
    repr_str = repr(user)
    assert '<UserModel' in repr_str
    assert str(user_id) in repr_str


def test_base_model_to_dict_with_none_relationship(db_session):
    """Test BaseModel to_dict method with None relationship."""
    user_id = uuid4()
    user = UserModel(id=user_id, username='testuser', email='test@example.com', password_hash='hashed', role='free_user')
    db_session.add(user)
    db_session.commit()
    
    # to_dict with include_relationships should handle None relationships
    user_dict = user.to_dict(include_relationships=True)
    assert 'id' in user_dict
    assert user_dict['profile'] is None  # profile relationship is None


def test_user_model_repr():
    """Test UserModel __repr__ method."""
    user_id = uuid4()
    user = UserModel(id=user_id, username='testuser', email='test@example.com', password_hash='hashed', role='free_user')
    repr_str = repr(user)
    assert '<UserModel' in repr_str
    assert 'test@example.com' in repr_str


def test_profile_model_repr():
    """Test ProfileModel __repr__ method."""
    profile_id = uuid4()
    user_id = uuid4()
    profile = ProfileModel(
        id=profile_id,
        user_id=user_id,
        first_name='John',
        last_name='Doe'
    )
    repr_str = repr(profile)
    assert '<ProfileModel' in repr_str
    assert str(user_id) in repr_str


def test_preferences_model_repr():
    """Test PreferencesModel __repr__ method."""
    prefs_id = uuid4()
    profile_id = uuid4()
    prefs = PreferencesModel(
        id=prefs_id,
        profile_id=profile_id
    )
    repr_str = repr(prefs)
    assert '<PreferencesModel' in repr_str
    assert str(profile_id) in repr_str


def test_payment_model_repr():
    """Test PaymentModel __repr__ method."""
    payment_id = uuid4()
    expense_id = uuid4()
    payment = PaymentModel(
        id=payment_id,
        expense_id=expense_id,
        amount=100.0,
        no_installment=1,
        status='paid',
        payment_date=datetime.now()
    )
    repr_str = repr(payment)
    assert 'Payment N°' in repr_str or 'PaymentModel' in repr_str
    assert str(expense_id) in repr_str


def test_payment_model_str():
    """Test PaymentModel __str__ method."""
    payment_id = uuid4()
    expense_id = uuid4()
    payment = PaymentModel(
        id=payment_id,
        expense_id=expense_id,
        amount=100.0,
        no_installment=2,
        status='paid',
        payment_date=datetime.now()
    )
    str_repr = str(payment)
    assert 'Payment N° 2' in str_repr
    assert str(expense_id) in str_repr


def test_expense_model_repr():
    """Test ExpenseModel __repr__ method."""
    expense_id = uuid4()
    account_id = uuid4()
    expense = ExpenseModel(
        id=expense_id,
        account_id=account_id,
        title='Test Expense',
        amount=100.0,
        installments=3,
        expense_type='purchase'
    )
    repr_str = repr(expense)
    assert 'Expense:' in repr_str
    assert 'Test Expense' in repr_str


def test_expense_model_str():
    """Test ExpenseModel __str__ method."""
    expense_id = uuid4()
    account_id = uuid4()
    expense = ExpenseModel(
        id=expense_id,
        account_id=account_id,
        title='Monthly Subscription',
        amount=50.0,
        installments=1,
        expense_type='subscription'
    )
    str_repr = str(expense)
    assert 'Expense:' in str_repr
    assert 'Monthly Subscription' in str_repr


def test_expense_model_owner_id_property(db_session):
    """Test ExpenseModel owner_id hybrid property with mock account."""
    from src.infrastructure.database.models.account_model import AccountModel
    from unittest.mock import MagicMock
    
    # Create a mock account with owner_id
    owner_id = uuid4()
    mock_account = MagicMock()
    mock_account.owner_id = owner_id
    
    # Create an expense and manually set the account relationship
    expense = ExpenseModel(
        id=uuid4(),
        account_id=uuid4(),
        title='Test Expense',
        cc_name='Test Card',
        acquired_at=datetime.now().date(),
        amount=100.0,
        installments=1,
        first_payment_date=datetime.now().date(),
        status='active',
        expense_type='purchase',
        category_id=uuid4()
    )
    expense.account = mock_account
    
    # Test the hybrid property
    assert expense.owner_id == owner_id
