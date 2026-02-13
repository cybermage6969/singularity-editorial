from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
_project_root = Path(__file__).resolve().parent.parent
load_dotenv(_project_root / ".env")


@dataclass(frozen=True)
class Settings:
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "anthropic")
    API_KEY: str = os.getenv("API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "claude-sonnet-4-5-20250929")
    BASE_URL: str = os.getenv("BASE_URL", "")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "4096"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    OUTPUT_DIR: str = str(_project_root / "output")


settings = Settings()
