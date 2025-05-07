from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field
# from pydantic.generics

T = TypeVar('T')


class PaginationMeta(BaseModel):
    current_page: int
    total_pages: int
    total_items: int
    per_page: int


class PaginatedResponse(BaseModel, Generic[T]):
    results: List[T] = Field(..., description='Page results')
    meta: PaginationMeta = Field(..., description='Pagination metadata')
