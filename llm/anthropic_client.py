from __future__ import annotations

from collections.abc import Iterator

import anthropic

from llm.base import ChatStream, LLMClient, LLMResponse


class AnthropicChatStream(ChatStream):
    def __init__(
        self,
        client: anthropic.Anthropic,
        model: str,
        system_prompt: str,
        user_message: str,
        max_tokens: int,
        temperature: float,
    ) -> None:
        self.response: LLMResponse | None = None
        self._client = client
        self._model = model
        self._system_prompt = system_prompt
        self._user_message = user_message
        self._max_tokens = max_tokens
        self._temperature = temperature

    def __iter__(self) -> Iterator[str]:
        with self._client.messages.stream(
            model=self._model,
            max_tokens=self._max_tokens,
            temperature=self._temperature,
            system=self._system_prompt,
            messages=[{"role": "user", "content": self._user_message}],
        ) as stream:
            for text in stream.text_stream:
                yield text
            msg = stream.get_final_message()
            self.response = LLMResponse(
                content=msg.content[0].text,
                model=msg.model,
                input_tokens=msg.usage.input_tokens,
                output_tokens=msg.usage.output_tokens,
            )


class AnthropicClient(LLMClient):
    def __init__(self, api_key: str, model: str, base_url: str = "") -> None:
        kwargs: dict = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        self._client = anthropic.Anthropic(**kwargs)
        self._model = model

    def chat(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> LLMResponse:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        return LLMResponse(
            content=response.content[0].text,
            model=response.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )

    def chat_stream(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> AnthropicChatStream:
        return AnthropicChatStream(
            client=self._client,
            model=self._model,
            system_prompt=system_prompt,
            user_message=user_message,
            max_tokens=max_tokens,
            temperature=temperature,
        )
