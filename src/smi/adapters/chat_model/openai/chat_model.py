from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_openai import ChatOpenAI

from audit_proto.config.settings import settings


def get_openai_chat_model(
    model_name: str,
    temp: float = 0.0,
    max_retries: int = 5,
    rate_limiter: InMemoryRateLimiter | None = None,
) -> ChatOpenAI:
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,
        rate_limiter=rate_limiter,
        max_retries=max_retries,
        model=model_name,
        temperature=temp,
    )
