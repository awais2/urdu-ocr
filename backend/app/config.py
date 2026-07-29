"""Application settings loaded from environment / .env file."""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str
    gemini_model: str = "gemini-2.5-flash"

    database_path: str = "data/urdu_ocr.db"

    cors_origins: str = "http://localhost:5173"
    max_upload_size_mb: int = 15

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
