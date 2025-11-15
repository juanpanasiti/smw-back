import pytest
import copy
from uuid import uuid4

from src.infrastructure.repositories import ExpenseRepositorySQL
from src.infrastructure.database.models import ExpenseModel, PaymentModel
from src.domain.expense import Purchase as PurchaseEntity
from tests.fixtures.db_fixtures import sqlite_session  # noqa: F401
from tests.fixtures.expense_fixtures import purchase  # noqa: F401
from tests.fixtures.account_fixtures import main_credit_card  # noqa: F401
from tests.fixtures.auth_fixtures import user  # noqa: F401


@pytest.fixture
def expense_repo(sqlite_session) -> ExpenseRepositorySQL:
    return ExpenseRepositorySQL(model=ExpenseModel, session_factory=sqlite_session)


def test_expense_repository_sql_init(expense_repo: ExpenseRepositorySQL):
    assert isinstance(expense_repo, ExpenseRepositorySQL)
    assert hasattr(expense_repo, 'create')
    assert hasattr(expense_repo, 'get_many_by_filter')
    assert hasattr(expense_repo, 'count_by_filter')
    assert hasattr(expense_repo, 'update')
    assert hasattr(expense_repo, 'delete_by_filter')


def test_expense_repository_get_filter_params(expense_repo: ExpenseRepositorySQL):
    params = {
        'account_id': uuid4(),
        'category_id': uuid4(),
        'expense_type': 'purchase',
        'status': 'active',
        'other_param': 'skip',
    }
    filter_params = expense_repo._get_filter_params(params)
    assert 'account_id' in filter_params
    assert 'category_id' in filter_params
    assert 'expense_type' in filter_params
    assert 'status' in filter_params
    assert 'other_param' not in filter_params


def test_expense_repository_create(expense_repo: ExpenseRepositorySQL, purchase: PurchaseEntity):
    created = expense_repo.create(purchase)
    assert isinstance(created, PurchaseEntity)
    assert created.title == purchase.title
    assert expense_repo.count_by_filter(filter={'id': purchase.id}) == 1


def test_expense_repository_create_persists_payments(
    expense_repo: ExpenseRepositorySQL,
    sqlite_session,
    purchase: PurchaseEntity,
):
    created = expense_repo.create(purchase)
    assert len(created.payments) == purchase.installments

    with sqlite_session() as session:
        stored_payments = session.query(PaymentModel).filter_by(expense_id=purchase.id).all()
        assert len(stored_payments) == purchase.installments


def test_expense_repository_get_many_by_filter(expense_repo: ExpenseRepositorySQL, purchase: PurchaseEntity):
    for i in range(3):
        exp = copy.deepcopy(purchase)
        exp.id = uuid4()
        exp.title = f'Expense{i}'
        exp.payments = []
        exp.calculate_payments()
        expense_repo.create(exp)
    total = expense_repo.count_by_filter()
    assert total == 3


def test_expense_repository_get_by_filter(expense_repo: ExpenseRepositorySQL, purchase: PurchaseEntity):
    created = expense_repo.create(purchase)
    fetched = expense_repo.get_by_filter({'id': created.id})
    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.title == created.title


def test_expense_repository_update(expense_repo: ExpenseRepositorySQL, purchase: PurchaseEntity):
    created = expense_repo.create(purchase)
    created.title = 'Updated Expense Title'
    updated = expense_repo.update(created)
    assert updated.title == 'Updated Expense Title'


def test_expense_repository_delete_by_filter(expense_repo: ExpenseRepositorySQL, purchase: PurchaseEntity):
    created = expense_repo.create(purchase)
    cnt = expense_repo.count_by_filter(filter={'id': created.id})
    assert cnt == 1
    expense_repo.delete_by_filter({'id': created.id})
    cnt_after = expense_repo.count_by_filter(filter={'id': created.id})
    assert cnt_after == 0


# Unit tests with mocks for exception paths and complex logic

from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_session_factory():
    """Create a mock session factory."""
    mock_session = MagicMock()
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__enter__ = MagicMock(return_value=mock_session)
    mock_session_factory.return_value.__exit__ = MagicMock(return_value=None)
    return mock_session_factory, mock_session


@pytest.fixture
def mock_expense_repo(mock_session_factory):
    """Create a repository with mocked session."""
    session_factory, _ = mock_session_factory
    return ExpenseRepositorySQL(ExpenseModel, session_factory)


def test_create_exception(mock_expense_repo, mock_session_factory, purchase: PurchaseEntity):
    """Test create raises exception on database error."""
    _, mock_session = mock_session_factory
    mock_session.flush.side_effect = Exception('Database error')
    
    with patch.object(mock_expense_repo, '_parse_entity_to_model', return_value=MagicMock(id=purchase.id)):
        with pytest.raises(Exception, match='Database error'):
            mock_expense_repo.create(purchase)


def test_update_not_found(mock_expense_repo, mock_session_factory, purchase: PurchaseEntity):
    """Test update raises ValueError when expense not found."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    mock_query.filter_by.return_value = mock_query
    mock_query.first.return_value = None
    
    with pytest.raises(ValueError, match=f'Expense with id {purchase.id} not found'):
        mock_expense_repo.update(purchase)


def test_update_exception(mock_expense_repo, mock_session_factory, purchase: PurchaseEntity):
    """Test update raises exception on database error."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    mock_query.filter_by.return_value = mock_query
    
    # Mock expense model
    mock_model = MagicMock()
    mock_query.first.return_value = mock_model
    mock_session.commit.side_effect = Exception('Database error')
    
    with pytest.raises(Exception, match='Database error'):
        mock_expense_repo.update(purchase)


def test_get_many_by_filter_with_owner_id_join(mock_expense_repo, mock_session_factory):
    """Test get_many_by_filter with owner_id performs JOIN."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    
    # Setup chain
    mock_query.join.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.all.return_value = [MagicMock()]
    
    with patch.object(mock_expense_repo, '_get_filter_params', return_value={'owner_id': uuid4()}):
        with patch.object(mock_expense_repo, '_parse_model_to_entity', return_value=MagicMock()):
            result = mock_expense_repo.get_many_by_filter({'owner_id': uuid4()}, limit=10, offset=0)
            
            assert len(result) == 1
            mock_query.join.assert_called_once()


def test_get_many_by_filter_with_owner_id_and_ordering(mock_expense_repo, mock_session_factory):
    """Test get_many_by_filter with owner_id and ordering."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    
    # Setup chain
    mock_query.join.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.all.return_value = [MagicMock()]
    
    with patch.object(mock_expense_repo, '_get_filter_params', return_value={'owner_id': uuid4()}):
        with patch.object(mock_expense_repo, '_parse_model_to_entity', return_value=MagicMock()):
            result = mock_expense_repo.get_many_by_filter({'owner_id': uuid4(), 'order_by': 'id'}, limit=10, offset=0)
            
            assert len(result) == 1
            mock_query.order_by.assert_called_once()


def test_get_many_by_filter_with_owner_id_and_filters(mock_expense_repo, mock_session_factory):
    """Test get_many_by_filter with owner_id and additional filters."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    
    # Setup chain
    mock_query.join.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.all.return_value = [MagicMock()]
    
    owner_id = uuid4()
    account_id = uuid4()
    with patch.object(mock_expense_repo, '_get_filter_params', return_value={'owner_id': owner_id, 'account_id': account_id}):
        with patch.object(mock_expense_repo, '_parse_model_to_entity', return_value=MagicMock()):
            result = mock_expense_repo.get_many_by_filter({'owner_id': owner_id, 'account_id': account_id}, limit=10, offset=0)
            
            assert len(result) == 1
            # Should call filter multiple times
            assert mock_query.filter.call_count >= 2


def test_get_many_by_filter_without_owner_id_uses_filter_by(mock_expense_repo, mock_session_factory):
    """Test get_many_by_filter without owner_id uses filter_by."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    
    # Setup chain
    mock_query.filter_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.all.return_value = [MagicMock()]
    
    account_id = uuid4()
    with patch.object(mock_expense_repo, '_get_filter_params', return_value={'account_id': account_id}):
        with patch.object(mock_expense_repo, '_parse_model_to_entity', return_value=MagicMock()):
            result = mock_expense_repo.get_many_by_filter({'account_id': account_id}, limit=10, offset=0)
            
            assert len(result) == 1
            mock_query.filter_by.assert_called_once()


def test_get_many_by_filter_exception(mock_expense_repo, mock_session_factory):
    """Test get_many_by_filter raises exception on database error."""
    _, mock_session = mock_session_factory
    mock_session.query.side_effect = Exception('Database error')
    
    with pytest.raises(Exception, match='Database error'):
        mock_expense_repo.get_many_by_filter({}, limit=10, offset=0)


def test_count_by_filter_with_owner_id_join(mock_expense_repo, mock_session_factory):
    """Test count_by_filter with owner_id performs JOIN."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    
    # Setup chain
    mock_query.join.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.count.return_value = 5
    
    with patch.object(mock_expense_repo, '_get_filter_params', return_value={'owner_id': uuid4()}):
        result = mock_expense_repo.count_by_filter({'owner_id': uuid4()})
        
        assert result == 5
        mock_query.join.assert_called_once()


def test_count_by_filter_with_owner_id_and_filters(mock_expense_repo, mock_session_factory):
    """Test count_by_filter with owner_id and additional filters."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    
    # Setup chain
    mock_query.join.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.count.return_value = 3
    
    owner_id = uuid4()
    account_id = uuid4()
    with patch.object(mock_expense_repo, '_get_filter_params', return_value={'owner_id': owner_id, 'account_id': account_id}):
        result = mock_expense_repo.count_by_filter({'owner_id': owner_id, 'account_id': account_id})
        
        assert result == 3
        # Should call filter multiple times
        assert mock_query.filter.call_count >= 2


def test_count_by_filter_without_owner_id_uses_filter_by(mock_expense_repo, mock_session_factory):
    """Test count_by_filter without owner_id uses filter_by."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    
    # Setup chain
    mock_query.filter_by.return_value = mock_query
    mock_query.count.return_value = 7
    
    account_id = uuid4()
    with patch.object(mock_expense_repo, '_get_filter_params', return_value={'account_id': account_id}):
        result = mock_expense_repo.count_by_filter({'account_id': account_id})
        
        assert result == 7
        mock_query.filter_by.assert_called_once()


def test_count_by_filter_exception(mock_expense_repo, mock_session_factory):
    """Test count_by_filter raises exception on database error."""
    _, mock_session = mock_session_factory
    mock_session.query.side_effect = Exception('Database error')
    
    with pytest.raises(Exception, match='Database error'):
        mock_expense_repo.count_by_filter({})
