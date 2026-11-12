"""
Application configuration loader for JARVIS backend.
Loads environment variables from `.env` using Pydantic Settings.
"""
from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

LLMProviderType = Literal["ollama", "openai", "anthropic", "gemini"]


class Settings(BaseSettings):
    """Typed runtime settings loaded from environment variables and `.env`."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM Provider Configuration
    LLM_PROVIDER: LLMProviderType = "ollama"
    LLM_MODEL: str = "llama3.2"
    LLM_TEMPERATURE: float = Field(default=0.7, ge=0.0, le=2.0)
    LLM_MAX_TOKENS: int = Field(default=2048, ge=1)
    LLM_TIMEOUT_SECONDS: float = Field(default=60.0, gt=0.0)

    # Ollama (Local)
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    # Cloud LLM API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    # Search Engine
    SEARCH_PROVIDER: str = "duckduckgo"
    TAVILY_API_KEY: Optional[str] = None

    # Storage & Paths
    DATA_DIR: Path = Path("data")
    SQLITE_DB_PATH: Path = Path("data/jarvis.db")

    # Terminal Safety
    REQUIRE_COMMAND_APPROVAL: bool = True

    # Voice Settings
    VOICE_ENABLED: bool = False
    STT_MODEL_SIZE: str = "base.en"
    TTS_ENGINE: str = "edge-tts"
    TTS_VOICE: str = "en-US-ChristopherNeural"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings instance (call `.cache_clear()` in tests)."""
    return Settings()
