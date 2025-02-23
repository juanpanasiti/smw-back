from typing import Optional
from fastapi import HTTPException

class BaseHTTPException(HTTPException):
    description: str
    status_code: int
    exception_code: str

    def __init__(self, message: Optional[str] = '', exception_code: Optional[str] = '') -> None:
        super().__init__(
            status_code=self.status_code,
            detail={"description": message or self.description, "code": exception_code or self.exception_code}
        )

    @classmethod
    def dict(cls) -> dict:
        return {
            "description": cls.description,
        }
