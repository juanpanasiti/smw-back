from pydantic import BaseModel


class PaginationParamsV1(BaseModel):
    offset: int = 0
    limit: int = 10
