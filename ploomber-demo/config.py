"""Configuration settings for the application, set in the .env file."""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the application"""

    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env")
