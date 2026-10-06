"""
Hybrid Council transport and unified model registry.
Seamlessly combines local zero-cost OpenCode models with custom keyed providers (OpenRouter, etc.).
"""

from typing import Any, Dict, List, Optional
import httpx

from . import opencode_client, provider_keys
from .opencode_client import CouncilSession

OPENROUTER_MODELS: List[Dict[str, Any]] = [
    {
        "id": "openrouter/anthropic/claude-3.5-sonnet",
        "providerID": "openrouter",
        "modelID": "anthropic/claude-3.5-sonnet",
        "name": "Claude 3.5 Sonnet (OpenRouter)",
        "family": "claude",
        "context": 200000,
        "output": 8192,
        "supportsTools": True,
        "supportsVision": True,
        "free": False,
    },
    {
        "id": "openrouter/openai/gpt-4o",
        "providerID": "openrouter",
        "modelID": "openai/gpt-4o",
        "name": "GPT-4o (OpenRouter)",
        "family": "gpt",
        "context": 128000,
        "output": 4096,
        "supportsTools": True,
        "supportsVision": True,
        "free": False,
    },
    {
        "id": "openrouter/deepseek/deepseek-r1",
        "providerID": "openrouter",
        "modelID": "deepseek/deepseek-r1",
        "name": "DeepSeek R1 (OpenRouter)",
        "family": "deepseek",
        "context": 64000,
        "output": 8192,
        "supportsTools": True,
        "supportsVision": False,
        "free": False,
    },
    {
        "id": "openrouter/meta-llama/llama-3.3-70b-instruct",
        "providerID": "openrouter",
        "modelID": "meta-llama/llama-3.3-70b-instruct",
        "name": "Llama 3.3 70B Instruct (OpenRouter)",
        "family": "llama",
        "context": 131072,
        "output": 8192,
        "supportsTools": True,
        "supportsVision": False,
        "free": False,
    },
]


async def list_unified_models() -> List[Dict[str, Any]]:
    """
    Return all available models across local OpenCode and configured external providers.
    """
    models: List[Dict[str, Any]] = []

    # 1. Fetch free OpenCode models
    try:
        opencode_models = await opencode_client.list_models()
        models.extend(opencode_models)
    except Exception as exc:
        print(f"[hybrid] could not list opencode models: {exc}")

    # 2. Add OpenRouter models if key is present
    if provider_keys.get_key("openrouter"):
        models.extend(OPENROUTER_MODELS)

    models.sort(key=lambda m: m["id"])
    return models


class HybridCouncilSession:
    """
    Unified session wrapper routing to either local OpenCode daemon
    or direct external HTTP provider API depending on model ID prefix.
    """

    def __init__(
        self,
        model: str,
        client: httpx.AsyncClient,
        agent: Optional[str] = None,
        variant: Optional[str] = None,
    ):
        self.model = model
        self.client = client
        self.agent = agent
        self.variant = variant
        self.is_opencode = not model.startswith("openrouter/")
        self.provider = "opencode" if self.is_opencode else "openrouter"
        self.raw_model = model.replace("openrouter/", "", 1) if not self.is_opencode else model
        self.session_id: Optional[str] = None
        self.messages: List[Dict[str, str]] = []

        if self.is_opencode:
            self._session: Optional[CouncilSession] = CouncilSession(
                model, client, agent=agent, variant=variant
            )
        else:
            self._session = None

    async def create(self) -> "HybridCouncilSession":
        if self.is_opencode and self._session:
            await self._session.create()
            self.session_id = self._session.session_id
        else:
            self.session_id = f"ext_{self.model}"
            self.messages = []
        return self

    async def set_permissions(self, rules: List[Dict[str, str]]) -> None:
        if self.is_opencode and self._session:
            await self._session.set_permissions(rules)

    async def ask(
        self,
        prompt: str,
        timeout: float = 120.0,
    ) -> Dict[str, Any]:
        if self.is_opencode and self._session:
            return await self._session.ask(prompt, timeout=timeout)

        # External HTTP Provider handling (OpenRouter / OpenAI compatible)
        self.messages.append({"role": "user", "content": prompt})
        api_key = provider_keys.get_key("openrouter")
        if not api_key:
            return {
                "text": "",
                "reasoning": "",
                "toolCalls": [],
                "tokens": {},
                "cost": 0,
                "finish": "error",
                "model": self.model,
                "error": "OpenRouter API key not configured",
            }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/opencode/llm-council",
            "X-Title": "LLM Council",
        }
        payload = {
            "model": self.raw_model,
            "messages": self.messages,
        }
        if self.variant:
            payload["reasoning_effort"] = self.variant

        try:
            res = await self.client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=timeout,
            )
            if res.status_code == 401:
                return {
                    "text": "",
                    "reasoning": "",
                    "toolCalls": [],
                    "tokens": {},
                    "cost": 0,
                    "finish": "error",
                    "model": self.model,
                    "error": "401 Unauthorized: Invalid API Key or Insufficient Credits",
                }
            if res.status_code == 429:
                return {
                    "text": "",
                    "reasoning": "",
                    "toolCalls": [],
                    "tokens": {},
                    "cost": 0,
                    "finish": "error",
                    "model": self.model,
                    "error": "429 Too Many Requests: Rate Limit Reached",
                }
            res.raise_for_status()

            data = res.json()
            choice = data["choices"][0]["message"]
            text = choice.get("content") or ""
            reasoning = choice.get("reasoning_details") or choice.get("reasoning") or ""
            usage = data.get("usage") or {}
            tokens = {
                "input": usage.get("prompt_tokens", 0),
                "output": usage.get("completion_tokens", 0),
                "reasoning": 0,
                "total": usage.get("total_tokens", 0),
            }

            self.messages.append({"role": "assistant", "content": text})
            return {
                "text": text,
                "reasoning": reasoning,
                "toolCalls": [],
                "tokens": tokens,
                "cost": 0,
                "finish": "stop",
                "model": self.model,
                "error": None,
            }
        except Exception as exc:
            return {
                "text": "",
                "reasoning": "",
                "toolCalls": [],
                "tokens": {},
                "cost": 0,
                "finish": "error",
                "model": self.model,
                "error": str(exc),
            }

    async def close(self) -> None:
        if self.is_opencode and self._session:
            await self._session.close()
        self.messages.clear()
