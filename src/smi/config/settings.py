"""Application settings loaded from environment variables and .env files."""

import os

from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()


class Settings:
    """Container for runtime configuration used across the service."""

    ROOT_LOG_LEVEL = os.getenv("ROOT_LOG_LEVEL", "INFO")
    RAG_SERVICE_LOG_LEVEL = os.getenv("RAG_SERVICE_LOG_LEVEL", "DEBUG")

    EXAMPLE_API_KEY: SecretStr = SecretStr(os.environ.get("EXAMPLE_API_KEY", ""))


settings = Settings()
