from langchain_core.language_models import BaseChatModel
from langchain_core.rate_limiters import InMemoryRateLimiter

from smi.src.smi.adapters.chat_model.openai.chat_model import get_openai_chat_model


_DEFAULT_RATE_LIMITER = InMemoryRateLimiter()


def get_chat_model(
    provider: str = "openai",
    model_name: str = "gpt-4.1",
    temp: float = 0.0,
    max_retries: int = 5,
    rate_limiter: InMemoryRateLimiter | None = _DEFAULT_RATE_LIMITER,
) -> BaseChatModel:
    match provider:
        case "openai":
            return get_openai_chat_model(model_name, temp, max_retries, rate_limiter)

        case _:
            raise ValueError(f"Unknown provider: {provider}")
