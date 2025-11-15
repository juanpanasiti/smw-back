import pytest
from uuid import uuid4
from unittest.mock import MagicMock, patch, PropertyMock
from datetime import date, datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query

from src.infrastructure.repositories.expense_category_repository_sql import ExpenseCategoryRepositorySQL
from src.infrastructure.database.models import ExpenseCategoryModel
from src.domain.expense import ExpenseCategory


@pytest.fixture
def mock_session_factory():
    """Create a mock session factory."""
    mock_session = MagicMock()
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__enter__ = MagicMock(return_value=mock_session)
    mock_session_factory.return_value.__exit__ = MagicMock(return_value=None)
    return mock_session_factory, mock_session


@pytest.fixture
def repository(mock_session_factory):
    """Create a repository with mocked session."""
    session_factory, _ = mock_session_factory
    return ExpenseCategoryRepositorySQL(ExpenseCategoryModel, session_factory)


@pytest.fixture
def sample_entity():
    """Create a sample ExpenseCategory entity."""
    return ExpenseCategory(
        id=uuid4(),
        owner_id=uuid4(),
        name='Test Category',
        description='Test Description',
        is_income=False,
    )


@pytest.fixture
def sample_model():
    """Create a sample ExpenseCategoryModel."""
    model = ExpenseCategoryModel(
        id=uuid4(),
        owner_id=uuid4(),
        name='Test Category',
        description='Test Description',
        is_income=False,
    )
    return model


# count_by_filter tests

def test_count_by_filter_success(repository, mock_session_factory):
    """Test count_by_filter returns correct count."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock()
    mock_query.filter_by.return_value.count.return_value = 5
    mock_session.query.return_value = mock_query
    
    result = repository.count_by_filter({'owner_id': uuid4()})
    assert result == 5


def test_count_by_filter_exception(repository, mock_session_factory):
    """Test count_by_filter raises exception on database error."""
    _, mock_session = mock_session_factory
    mock_session.query.side_effect = Exception('Database error')
    
    with pytest.raises(Exception, match='Database error'):
        repository.count_by_filter({})


# create tests

def test_create_success(repository, mock_session_factory, sample_entity):
    """Test create adds entity to database."""
    _, mock_session = mock_session_factory
    mock_model = MagicMock()
    mock_model.id = sample_entity.id
    mock_model.owner_id = sample_entity.owner_id
    mock_model.name = sample_entity.name
    mock_model.description = sample_entity.description
    mock_model.is_income = sample_entity.is_income
    
    with patch.object(repository, '_parse_entity_to_model', return_value=mock_model):
        with patch.object(repository, '_parse_model_to_entity', return_value=sample_entity):
            result = repository.create(sample_entity)
            
            assert result == sample_entity
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()
            mock_session.refresh.assert_called_once()


def test_create_exception(repository, mock_session_factory, sample_entity):
    """Test create raises exception on database error."""
    _, mock_session = mock_session_factory
    mock_session.commit.side_effect = Exception('Database error')
    
    with patch.object(repository, '_parse_entity_to_model', return_value=MagicMock()):
        with pytest.raises(Exception, match='Database error'):
            repository.create(sample_entity)


# get_many_by_filter tests

def test_get_many_by_filter_simple(repository, mock_session_factory, sample_model):
    """Test get_many_by_filter without ordering."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock(spec=Query)
    mock_session.query.return_value = mock_query
    
    # Setup chain
    mock_query.filter_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.all.return_value = [sample_model]
    
    with patch.object(repository, '_get_filter_params', return_value={'owner_id': uuid4()}):
        with patch.object(repository, '_parse_model_to_entity', return_value=MagicMock()):
            result = repository.get_many_by_filter({'owner_id': uuid4()}, limit=10, offset=0)
            
            assert len(result) == 1
            mock_query.limit.assert_called_with(10)
            mock_query.offset.assert_called_with(0)


def test_get_many_by_filter_with_ordering(repository, mock_session_factory, sample_model):
    """Test get_many_by_filter with order_by parameter."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock(spec=Query)
    mock_session.query.return_value = mock_query
    
    # Setup chain
    mock_query.order_by.return_value = mock_query
    mock_query.filter_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.all.return_value = [sample_model]
    
    with patch.object(repository, '_get_filter_params', return_value={}):
        with patch.object(repository, '_parse_model_to_entity', return_value=MagicMock()):
            result = repository.get_many_by_filter({'order_by': 'id', 'order_asc': True}, limit=10, offset=0)
            
            assert len(result) == 1
            mock_query.order_by.assert_called_once()


def test_get_many_by_filter_with_desc_ordering(repository, mock_session_factory, sample_model):
    """Test get_many_by_filter with descending order."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock(spec=Query)
    mock_session.query.return_value = mock_query
    
    # Setup chain
    mock_query.order_by.return_value = mock_query
    mock_query.filter_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.all.return_value = [sample_model]
    
    with patch.object(repository, '_get_filter_params', return_value={}):
        with patch.object(repository, '_parse_model_to_entity', return_value=MagicMock()):
            result = repository.get_many_by_filter({'order_by': 'created_at', 'order_asc': False}, limit=10, offset=0)
            
            assert len(result) == 1
            mock_query.order_by.assert_called_once()


def test_get_many_by_filter_empty_search_filter(repository, mock_session_factory, sample_model):
    """Test get_many_by_filter with empty search filter."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock(spec=Query)
    mock_session.query.return_value = mock_query
    
    # Setup chain
    mock_query.limit.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.all.return_value = [sample_model]
    
    with patch.object(repository, '_get_filter_params', return_value={}):
        with patch.object(repository, '_parse_model_to_entity', return_value=MagicMock()):
            result = repository.get_many_by_filter({}, limit=10, offset=0)
            
            assert len(result) == 1
            # filter_by should not be called when search_filter is empty
            mock_query.filter_by.assert_not_called()


def test_get_many_by_filter_exception(repository, mock_session_factory):
    """Test get_many_by_filter raises exception on database error."""
    _, mock_session = mock_session_factory
    mock_session.query.side_effect = Exception('Database error')
    
    with pytest.raises(Exception, match='Database error'):
        repository.get_many_by_filter({}, limit=10, offset=0)


# get_by_filter tests

def test_get_by_filter_found(repository, mock_session_factory, sample_model):
    """Test get_by_filter returns entity when found."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock(spec=Query)
    mock_session.query.return_value = mock_query
    mock_query.filter_by.return_value = mock_query
    mock_query.first.return_value = sample_model
    
    with patch.object(repository, '_parse_model_to_entity', return_value=MagicMock()):
        result = repository.get_by_filter({'id': uuid4()})
        assert result is not None


def test_get_by_filter_not_found(repository, mock_session_factory):
    """Test get_by_filter returns None when not found."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock(spec=Query)
    mock_session.query.return_value = mock_query
    mock_query.filter_by.return_value = mock_query
    mock_query.first.return_value = None
    
    result = repository.get_by_filter({'id': uuid4()})
    assert result is None


def test_get_by_filter_exception(repository, mock_session_factory):
    """Test get_by_filter raises exception on database error."""
    _, mock_session = mock_session_factory
    mock_session.query.side_effect = Exception('Database error')
    
    with pytest.raises(Exception, match='Database error'):
        repository.get_by_filter({})


# update tests

def test_update_not_found(repository, mock_session_factory, sample_entity):
    """Test update raises ValueError when entity not found."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock(spec=Query)
    mock_session.query.return_value = mock_query
    mock_query.filter_by.return_value = mock_query
    mock_query.first.return_value = None
    
    with pytest.raises(ValueError, match=f'No record found with id {sample_entity.id}'):
        repository.update(sample_entity)


def test_update_success(repository, mock_session_factory, sample_entity):
    """Test update modifies entity in database."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock(spec=Query)
    mock_session.query.return_value = mock_query
    mock_query.filter_by.return_value = mock_query
    
    # Use actual model instance to avoid __mapper__ issues
    mock_model = ExpenseCategoryModel(
        id=sample_entity.id,
        owner_id=sample_entity.owner_id,
        name='Old Name',
        description='Old Description',
        is_income=False,
    )
    mock_query.first.return_value = mock_model
    
    with patch.object(repository, '_parse_model_to_entity', return_value=sample_entity):
        result = repository.update(sample_entity)
        assert result == sample_entity
        mock_session.commit.assert_called_once()


def test_update_integrity_error(repository, mock_session_factory, sample_entity):
    """Test update raises IntegrityError on constraint violation."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock(spec=Query)
    mock_session.query.return_value = mock_query
    mock_query.filter_by.return_value = mock_query
    
    # Use actual model instance
    mock_model = ExpenseCategoryModel(
        id=sample_entity.id,
        owner_id=sample_entity.owner_id,
        name='Old Name',
        description='Old Description',
        is_income=False,
    )
    mock_query.first.return_value = mock_model
    mock_session.commit.side_effect = IntegrityError('statement', 'params', Exception('orig'))
    
    with pytest.raises(IntegrityError):
        repository.update(sample_entity)


def test_update_generic_exception(repository, mock_session_factory, sample_entity):
    """Test update raises exception on other database errors."""
    _, mock_session = mock_session_factory
    mock_session.query.side_effect = Exception('Database error')
    
    with pytest.raises(Exception, match='Database error'):
        repository.update(sample_entity)


# delete_by_filter tests

def test_delete_by_filter_success(repository, mock_session_factory):
    """Test delete_by_filter removes records."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock(spec=Query)
    mock_session.query.return_value = mock_query
    mock_query.filter_by.return_value = mock_query
    mock_query.delete.return_value = 1  # 1 record deleted
    
    repository.delete_by_filter({'id': uuid4()})
    mock_session.commit.assert_called_once()


def test_delete_by_filter_not_found(repository, mock_session_factory):
    """Test delete_by_filter raises ValueError when no records found."""
    _, mock_session = mock_session_factory
    mock_query = MagicMock(spec=Query)
    mock_session.query.return_value = mock_query
    mock_query.filter_by.return_value = mock_query
    mock_query.delete.return_value = 0  # No records deleted
    
    with pytest.raises(ValueError, match='No records found matching filter'):
        repository.delete_by_filter({'id': uuid4()})


def test_delete_by_filter_exception(repository, mock_session_factory):
    """Test delete_by_filter raises exception on database error."""
    _, mock_session = mock_session_factory
    mock_session.query.side_effect = Exception('Database error')
    
    with pytest.raises(Exception, match='Database error'):
        repository.delete_by_filter({})


# _get_order_by_params tests

def test_get_order_by_params_defaults(repository):
    """Test _get_order_by_params uses defaults."""
    result = repository._get_order_by_params({})
    assert result is not None


def test_get_order_by_params_with_custom_field(repository):
    """Test _get_order_by_params with custom field."""
    result = repository._get_order_by_params({'order_by': 'created_at', 'order_asc': True})
    assert result is not None


def test_get_order_by_params_descending(repository):
    """Test _get_order_by_params with descending order."""
    result = repository._get_order_by_params({'order_by': 'updated_at', 'order_asc': False})
    assert result is not None


def test_get_order_by_params_invalid_field(repository):
    """Test _get_order_by_params raises ValueError for invalid field."""
    with pytest.raises(ValueError, match='Invalid order_by field'):
        repository._get_order_by_params({'order_by': 'invalid_field'})
