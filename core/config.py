from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "DATABASE_URL"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()