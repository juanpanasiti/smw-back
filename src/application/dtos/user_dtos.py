from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict

from src.domain.auth import Role


class PreferencesResponseDTO(BaseModel):
    id: UUID
    monthly_spending_limit: float

    model_config = ConfigDict(from_attributes=True)


class ProfileResponseDTO(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    birthdate: str | None
    preferences: PreferencesResponseDTO | None

    model_config = ConfigDict(from_attributes=True)


class UserResponseDTO(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    role: Role
    profile: ProfileResponseDTO

    model_config = ConfigDict(from_attributes=True)
