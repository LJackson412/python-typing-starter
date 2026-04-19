"""Application settings loaded from environment variables and .env files."""

import os

from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()


class Settings:
    """Container for runtime configuration used across the service."""

    ROOT_LOG_LEVEL: str = os.getenv("ROOT_LOG_LEVEL", "INFO")
    SMI_LOG_LEVEL: str = os.getenv("SMI_LOG_LEVEL", "DEBUG")

    OPENAI_API_KEY: SecretStr = SecretStr(os.environ.get("OPENAI_API_KEY", ""))
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4.1")
    LLM_MAX_CONCURRENCY: int = int(os.getenv("LLM_MAX_CONCURRENCY", "10"))


settings = Settings()
