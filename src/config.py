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

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()  # type: ignore
