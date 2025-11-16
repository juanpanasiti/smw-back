import pytest
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from src.application.dtos import DecodedJWT, LoggedInUserDTO, RegisterUserDTO, LoginUserDTO
from src.application.dtos import Pagination, PaginatedResponse
from src.domain.auth import Role


def test_decoded_jwt_user_id_property():
    """Test DecodedJWT user_id property converts sub to UUID."""
    user_id = uuid4()
    decoded = DecodedJWT(
        sub=str(user_id),
        role=Role.FREE_USER,
        email='test@example.com',
        exp=datetime.now(timezone.utc) + timedelta(hours=1)
    )
    assert decoded.user_id == user_id
    assert isinstance(decoded.user_id, type(user_id))


def test_pagination_has_next_page_true():
    """Test Pagination has_next_page returns True when not on last page."""
    pagination = Pagination(
        current_page=2,
        total_pages=5,
        total_items=50,
        per_page=10
    )
    assert pagination.has_next_page is True


def test_pagination_has_next_page_false():
    """Test Pagination has_next_page returns False when on last page."""
    pagination = Pagination(
        current_page=5,
        total_pages=5,
        total_items=50,
        per_page=10
    )
    assert pagination.has_next_page is False


def test_pagination_has_previous_page_true():
    """Test Pagination has_previous_page returns True when not on first page."""
    pagination = Pagination(
        current_page=2,
        total_pages=5,
        total_items=50,
        per_page=10
    )
    assert pagination.has_previous_page is True


def test_pagination_has_previous_page_false():
    """Test Pagination has_previous_page returns False when on first page."""
    pagination = Pagination(
        current_page=1,
        total_pages=5,
        total_items=50,
        per_page=10
    )
    assert pagination.has_previous_page is False


def test_paginated_response_creation():
    """Test PaginatedResponse can be created with items and pagination."""
    pagination = Pagination(
        current_page=1,
        total_pages=3,
        total_items=30,
        per_page=10
    )
    response = PaginatedResponse[dict](
        items=[{'id': 1}, {'id': 2}],
        pagination=pagination
    )
    assert len(response.items) == 2
    assert response.pagination.current_page == 1
