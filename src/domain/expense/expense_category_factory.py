from uuid import UUID

from ..shared import EntityFactoryBase


class ExpenseCategoryFactory(EntityFactoryBase):
    @classmethod
    def create(cls, **kwargs):
        from .expense_category import ExpenseCategory
        id: UUID | None = kwargs.get('id')
        owner_id: UUID | None = kwargs.get('owner_id')
        name: str | None = kwargs.get('name')
        description: str | None = kwargs.get('description')
        is_income: bool | None = kwargs.get('is_income')

        if id is None or not isinstance(id, UUID):
            raise ValueError(f'id must be a UUID, got {type(id)}')
        if name is None or not isinstance(name, str) or not name.strip():
            raise ValueError('name must be a non-empty string')
        if owner_id is None or not isinstance(owner_id, UUID):
            raise ValueError(f'owner_id must be a UUID, got {type(owner_id)}')
        if description is None or (not isinstance(description, str)):
            raise ValueError(f'description must be a string, got {type(description)}')
        if is_income is None or not isinstance(is_income, bool):
            raise ValueError(f'is_income must be a boolean, got {type(is_income)}')

        return ExpenseCategory(
            id=id,
            name=name.strip(),
            owner_id=owner_id,
            description=description.strip(),
            is_income=is_income,
        )
