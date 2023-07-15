from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API
    PORT: int = 8000
    CONN_DB: str | None = None
    DEV: bool = False

    # Config
    DEBUG: bool = False

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = 'HS256'
    JWT_EXPIRATION_TIME_MINUTES: int = 3600

    class Config:
        env_file = '.env'
