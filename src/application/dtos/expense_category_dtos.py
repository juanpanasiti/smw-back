from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateExpenseCategoryDTO(BaseModel):
    owner_id: UUID
    name: str
    description: str = ''
    is_income: bool

    model_config = ConfigDict(from_attributes=True)


class UpdateExpenseCategoryDTO(BaseModel):
    name: str | None = None
    description: str | None = None
    is_income: bool | None = None

    model_config = ConfigDict(from_attributes=True)


class ExpenseCategoryResponseDTO(BaseModel):
    id: UUID
    owner_id: UUID
    name: str
    description: str
    is_income: bool

    model_config = ConfigDict(from_attributes=True)
