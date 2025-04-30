from pydantic import BaseModel


class ProfileReqV1(BaseModel):
    user_id: int
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class ProfileResV1(BaseModel):
    first_name: str
    last_name: str
    spent_alert: float
    monthly_payment_alert: float

    class Config:
        from_attributes = True
