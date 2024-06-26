"""Configuration"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment configuration settings."""

    openai_api_key: str | None = None
    anthropic_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env")
