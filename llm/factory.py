from __future__ import annotations

from config.settings import settings
from llm.base import LLMClient


def create_llm_client() -> LLMClient:
    """Create an LLM client based on the configured provider."""
    provider = settings.LLM_PROVIDER.lower()

    if provider == "anthropic":
        from llm.anthropic_client import AnthropicClient

        return AnthropicClient(
            api_key=settings.API_KEY,
            model=settings.MODEL_NAME,
            base_url=settings.BASE_URL,
        )
    elif provider == "openai_compat":
        from llm.openai_compat_client import OpenAICompatClient

        return OpenAICompatClient(
            api_key=settings.API_KEY,
            model=settings.MODEL_NAME,
            base_url=settings.BASE_URL,
        )
    else:
        raise ValueError(f"不支持的 LLM 提供商: {provider}")
