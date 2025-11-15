import pytest

from src.common.exceptions.base_exception import BaseException
from src.common.exceptions.repo_exceptions import RepositoryError


def test_base_exception_with_code():
    """Test BaseException with error code."""
    exc = BaseException('Test message', 'TEST001')
    assert str(exc) == '[TEST001] Test message'


def test_base_exception_without_code():
    """Test BaseException without error code."""
    exc = BaseException('Test message')
    assert str(exc) == 'Test message'


def test_repository_exception_with_code():
    """Test RepositoryError with error code."""
    exc = RepositoryError('Database error', 'REPO001')
    assert str(exc) == '[REPO001] Database error'


def test_repository_exception_without_code():
    """Test RepositoryError without error code (uses default)."""
    exc = RepositoryError('Database error')
    assert 'Database error' in str(exc)
