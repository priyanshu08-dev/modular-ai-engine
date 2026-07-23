from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    APP_NAME: str = "Modular AI Engine"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    LLM_PROVIDER: str = "groq"

    EMBEDDING_PROVIDER: str = "gemini"

    GROQ_API_KEY: str

    OPENAI_API_KEY: str = ""

    GEMINI_API_KEY: str = ""

    GEMINI_EMBEDDING_MODEL: str = "gemini-embedding-001"

    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    # ==========================
    # Document Settings
    # ==========================

    MAX_DOCUMENT_SIZE_MB: int = 25

    # ==========================
    # Chunking Settings
    # ==========================

    CHUNK_SIZE: int = 100
    CHUNK_OVERLAP: int = 20
    KEEP_SEPARATOR: bool = True
    IS_SEPARATOR_REGEX: bool = False
    CHUNK_SEPARATORS: list[str] = [
        "\n\n",
        "\n",
        ". ",
        "! ",
        "? ",
        "; ",
        ", ",
        " ",
        "",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.
    """
    return Settings()


settings = get_settings()