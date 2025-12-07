from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str = "sqlite:///./expense_tracker.db"
    DEBUG: bool = False
    APP_TITLE: str = "Expense Tracker"
    APP_VERSION: str = "1.0.0"

    # You can add more settings as needed

@lru_cache()
def get_settings() -> Settings:
    return Settings()
