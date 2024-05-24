from pydantic import BaseModel


class PaginateParams(BaseModel):
    skip: int = 0
    size: int = 10
