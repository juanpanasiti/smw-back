from pydantic_settings import BaseSettings, SettingsConfigDict


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
    JWT_MAX_RENEWALS: int = 3  # Maximum auto-renewals before requiring refresh
    JWT_REFRESH_SECRET_KEY: str  # ! Required - Different secret for refresh tokens
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 30  # 30 days

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()  # type: ignore
