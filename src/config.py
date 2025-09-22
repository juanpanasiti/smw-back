from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API
    PORT: int = 8000
    CONN_DB: str  # ! Required
    DEV: bool = False

    # Config
    DEBUG: bool = False

    # JWT
    JWT_SECRET_KEY: str  # ! Required
    JWT_ALGORITHM: str = 'HS256'
    JWT_EXPIRATION_TIME_MINUTES: int = 60  # 1h

    class Config:
        env_file = '.env'


settings = Settings()  # type: ignore
