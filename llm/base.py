from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class LLMResponse:
    content: str
    model: str
    input_tokens: int
    output_tokens: int


class ChatStream(ABC):
    """流式 LLM 响应。迭代获取文本片段，迭代结束后 .response 可用。"""

    response: LLMResponse | None

    @abstractmethod
    def __iter__(self) -> Iterator[str]: ...


class LLMClient(ABC):
    @abstractmethod
    def chat(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> LLMResponse:
        """Send a single-turn chat request and return the response."""

    @abstractmethod
    def chat_stream(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> ChatStream:
        """Send a single-turn chat request and return a streaming response."""
