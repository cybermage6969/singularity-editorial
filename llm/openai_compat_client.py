from __future__ import annotations

from llm.base import LLMClient, LLMResponse


class OpenAICompatClient(LLMClient):
    """Placeholder for future OpenAI-compatible API support."""

    def __init__(self, api_key: str, model: str, base_url: str = "") -> None:
        self._model = model
        raise NotImplementedError(
            "OpenAI 兼容客户端尚未实现。请使用 LLM_PROVIDER=anthropic。"
        )

    def chat(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> LLMResponse:
        raise NotImplementedError
