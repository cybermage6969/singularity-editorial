from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from llm.base import LLMClient


@dataclass
class AgentResult:
    agent_key: str
    agent_name: str
    input_text: str
    output_text: str
    model: str
    input_tokens: int
    output_tokens: int
    elapsed_seconds: float
    edited: bool = False
    edited_text: str = ""


class BaseAgent(ABC):
    name: str = ""
    key: str = ""
    description: str = ""
    icon: str = ""

    def __init__(self, llm_client: LLMClient) -> None:
        self._llm = llm_client

    @abstractmethod
    def get_system_prompt(self) -> str:
        ...

    @abstractmethod
    def build_user_message(self, input_text: str) -> str:
        ...

    def run(self, input_text: str) -> AgentResult:
        system_prompt = self.get_system_prompt()
        user_message = self.build_user_message(input_text)

        start = time.time()
        response = self._llm.chat(
            system_prompt=system_prompt,
            user_message=user_message,
        )
        elapsed = time.time() - start

        return AgentResult(
            agent_key=self.key,
            agent_name=self.name,
            input_text=input_text,
            output_text=response.content,
            model=response.model,
            input_tokens=response.input_tokens,
            output_tokens=response.output_tokens,
            elapsed_seconds=round(elapsed, 2),
        )
