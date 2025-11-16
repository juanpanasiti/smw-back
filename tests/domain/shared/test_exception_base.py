import pytest
from src.domain.shared.exception_base import ExceptionBase


def test_exception_base_initialization() -> None:
    """Test that ExceptionBase can be initialized with a message."""
    exception = ExceptionBase('Test error message')
    assert exception.message == 'Test error message'
    assert exception.code == 'GENERIC_EXCEPTION'


def test_exception_base_str_representation() -> None:
    """Test that ExceptionBase string representation includes code and message."""
    exception = ExceptionBase('Something went wrong')
    assert str(exception) == 'GENERIC_EXCEPTION: Something went wrong'


def test_exception_base_can_be_raised() -> None:
    """Test that ExceptionBase can be raised like a normal exception."""
    with pytest.raises(ExceptionBase) as exc_info:
        raise ExceptionBase('Test exception')
    
    assert exc_info.value.message == 'Test exception'
    assert str(exc_info.value) == 'GENERIC_EXCEPTION: Test exception'


def test_exception_base_inheritance() -> None:
    """Test that ExceptionBase is a proper Exception."""
    exception = ExceptionBase('Test')
    assert isinstance(exception, Exception)
