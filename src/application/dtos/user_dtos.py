from uuid import UUID

from pydantic import BaseModel, EmailStr

from src.domain.auth import Role


class PreferencesResponseDTO(BaseModel):
    id: UUID
    monthly_spending_limit: float



class ProfileResponseDTO(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    birthdate: str | None
    preferences: PreferencesResponseDTO | None



class UserResponseDTO(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    role: Role
    profile: ProfileResponseDTO
