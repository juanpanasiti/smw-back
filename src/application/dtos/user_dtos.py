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


class UpdatePreferencesDTO(BaseModel):
    monthly_spending_limit: float | None = None


class UpdateProfileDTO(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    birthdate: str | None = None
    preferences: UpdatePreferencesDTO | None = None


class UpdateUserDTO(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    profile: UpdateProfileDTO | None = None
