# services/ai_service.py
from typing import Literal, Dict, Any
import httpx

from config.settings import settings

EngineType = Literal["ollama", "openai"]

class AIService:
    def __init__(self, engine: EngineType | None = None):
        self.engine = engine or settings.AI_DEFAULT_ENGINE

    async def ask(self, prompt: str, model: str | None = None) -> str:
        engine = self.engine

        if engine == "ollama":
            return await self._ask_ollama(prompt, model or settings.OLLAMA_MODEL)
        elif engine == "openai":
            return await self._ask_openai(prompt, model or settings.OPENAI_MODEL)
        else:
            raise ValueError(f"Unknown AI engine: {engine}")

    async def _ask_ollama(self, prompt: str, model: str) -> str:
        url = f"{settings.OLLAMA_BASE_URL}/api/chat"
        payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}

        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
            return data["message"]["content"]

    async def _ask_openai(self, prompt: str, model: str) -> str:
        # OpenAI API呼び出し（あとで実装でもOK）
        raise NotImplementedError