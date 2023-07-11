from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    # API
    PORT: int = 8000
    CONN_DB: str | None = None


    class Config:
        env_file = '.env'