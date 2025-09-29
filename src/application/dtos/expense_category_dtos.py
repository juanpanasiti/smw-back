from uuid import UUID

from pydantic import BaseModel


class CreateExpenseCategoryDTO(BaseModel):
    owner_id: UUID
    name: str
    description: str = ''
    is_income: bool



class UpdateExpenseCategoryDTO(BaseModel):
    name: str | None = None
    description: str | None = None
    is_income: bool | None = None



class ExpenseCategoryResponseDTO(BaseModel):
    id: UUID
    owner_id: UUID
    name: str
    description: str
    is_income: bool
