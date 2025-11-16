import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from src.infrastructure.database.database_connection import DatabaseConnection


@pytest.fixture
def db_connection() -> DatabaseConnection:
    """Create a database connection instance for testing."""
    return DatabaseConnection("sqlite:///:memory:")


def test_database_connection_init():
    """Test DatabaseConnection initialization."""
    str_conn = "sqlite:///:memory:"
    db = DatabaseConnection(str_conn)
    
    assert db.str_conn == str_conn
    assert db._engine is None
    assert db._SessionLocal is None


def test_database_connection_engine_property(db_connection: DatabaseConnection):
    """Test engine property creates engine on first access."""
    assert db_connection._engine is None
    
    engine = db_connection.engine
    
    assert engine is not None
    assert isinstance(engine, Engine)
    assert db_connection._engine is engine
    
    # Verify it returns the same instance on second access
    engine2 = db_connection.engine
    assert engine2 is engine


def test_database_connection_session_local_property(db_connection: DatabaseConnection):
    """Test SessionLocal property creates sessionmaker on first access."""
    assert db_connection._SessionLocal is None
    
    session_local = db_connection.SessionLocal
    
    assert session_local is not None
    assert isinstance(session_local, sessionmaker)
    assert db_connection._SessionLocal is session_local
    
    # Verify it returns the same instance on second access
    session_local2 = db_connection.SessionLocal
    assert session_local2 is session_local


def test_execute_query_success(db_connection: DatabaseConnection):
    """Test execute_query executes successfully and returns results."""
    result = db_connection.execute_query('SELECT 1 as value')
    
    assert result is not None
    assert len(result) > 0
    assert result[0][0] == 1


def test_execute_query_exception():
    """Test execute_query returns None on exception."""
    db_connection = DatabaseConnection("sqlite:///:memory:")
    
    # Mock the _SessionLocal attribute directly
    mock_session = MagicMock()
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__enter__ = MagicMock(return_value=mock_session)
    mock_session_factory.return_value.__exit__ = MagicMock(return_value=None)
    mock_session.execute.side_effect = Exception('Database error')
    
    db_connection._SessionLocal = mock_session_factory
    
    result = db_connection.execute_query('SELECT * FROM invalid_table')
    
    assert result is None


def test_execute_query_with_valid_query(db_connection: DatabaseConnection):
    """Test execute_query with a valid query returns correct results."""
    result = db_connection.execute_query('SELECT 42 as answer, "test" as text')
    
    assert result is not None
    assert len(result) == 1
    assert result[0][0] == 42
    assert result[0][1] == "test"


def test_test_connection_success(db_connection: DatabaseConnection):
    """Test test_connection returns True on successful connection."""
    result = db_connection.test_connection()
    
    assert result is True


def test_test_connection_failure():
    """Test test_connection returns False on connection failure."""
    # Use an invalid connection string
    db_connection = DatabaseConnection("invalid://connection/string")
    
    result = db_connection.test_connection()
    
    assert result is False


def test_test_connection_exception():
    """Test test_connection returns False when exception is raised."""
    db_connection = DatabaseConnection("sqlite:///:memory:")
    
    # Mock the _engine attribute directly
    mock_engine = MagicMock()
    mock_engine.connect.side_effect = Exception('Connection error')
    db_connection._engine = mock_engine
    
    result = db_connection.test_connection()
    
    assert result is False
