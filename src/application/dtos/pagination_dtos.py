from pydantic import BaseModel, Field
from typing import Generic, TypeVar

T = TypeVar('T')


class Pagination(BaseModel):
    current_page: int = Field(..., ge=1)
    total_pages: int = Field(..., ge=1)
    total_items: int = Field(..., ge=0)
    per_page: int = Field(..., ge=1)

    @property
    def has_next_page(self) -> bool:
        return self.current_page < self.total_pages

    @property
    def has_previous_page(self) -> bool:
        return self.current_page > 1


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T] = Field(..., description='Page items')
    pagination: Pagination = Field(..., description='Pagination details')
