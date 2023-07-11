from pydantic import BaseModel, EmailStr

class LoginUser(BaseModel):
    username: str
    password: str

class RegisterUser(LoginUser):
    email: EmailStr

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'