import pytest

from src.entrypoints.exceptions import BaseHTTPException


def test_base_http_exception_dict():
    """Test BaseHTTPException.dict() class method."""
    # Create a concrete subclass for testing
    class TestException(BaseHTTPException):
        description = "Test exception description"
        status_code = 400
        exception_code = "TEST_ERROR"
    
    result = TestException.dict()
    
    assert isinstance(result, dict)
    assert "description" in result
    assert result["description"] == "Test exception description"
