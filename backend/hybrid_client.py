"""
Hybrid Council transport and unified model registry.
Seamlessly combines local zero-cost OpenCode models with direct Bring-Your-Own-Key (BYOK)
cloud providers (OpenRouter, OpenAI, Anthropic, Google Gemini, Groq, DeepSeek, Mistral, xAI, etc.).
Runs completely autonomously even when OpenCode daemon is offline.
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

DIRECT_PROVIDER_MODELS: Dict[str, List[Dict[str, Any]]] = {
    "openrouter": OPENROUTER_MODELS,
    "openai": [
        {
            "id": "openai/gpt-4o",
            "providerID": "openai",
            "modelID": "gpt-4o",
            "name": "GPT-4o (Direct)",
            "family": "gpt",
            "context": 128000,
            "output": 4096,
            "supportsTools": True,
            "supportsVision": True,
            "free": False,
        },
        {
            "id": "openai/gpt-4o-mini",
            "providerID": "openai",
            "modelID": "gpt-4o-mini",
            "name": "GPT-4o Mini (Direct)",
            "family": "gpt",
            "context": 128000,
            "output": 4096,
            "supportsTools": True,
            "supportsVision": True,
            "free": False,
        },
    ],
    "anthropic": [
        {
            "id": "anthropic/claude-3-5-sonnet-20241022",
            "providerID": "anthropic",
            "modelID": "claude-3-5-sonnet-20241022",
            "name": "Claude 3.5 Sonnet (Direct)",
            "family": "claude",
            "context": 200000,
            "output": 8192,
            "supportsTools": True,
            "supportsVision": True,
            "free": False,
        },
        {
            "id": "anthropic/claude-3-5-haiku-20241022",
            "providerID": "anthropic",
            "modelID": "claude-3-5-haiku-20241022",
            "name": "Claude 3.5 Haiku (Direct)",
            "family": "claude",
            "context": 200000,
            "output": 8192,
            "supportsTools": True,
            "supportsVision": False,
            "free": False,
        },
    ],
    "google": [
        {
            "id": "google/gemini-2.0-flash",
            "providerID": "google",
            "modelID": "gemini-2.0-flash",
            "name": "Gemini 2.0 Flash (Direct)",
            "family": "gemini",
            "context": 1048576,
            "output": 8192,
            "supportsTools": True,
            "supportsVision": True,
            "free": False,
        },
        {
            "id": "google/gemini-1.5-pro",
            "providerID": "google",
            "modelID": "gemini-1.5-pro",
            "name": "Gemini 1.5 Pro (Direct)",
            "family": "gemini",
            "context": 2097152,
            "output": 8192,
            "supportsTools": True,
            "supportsVision": True,
            "free": False,
        },
    ],
    "groq": [
        {
            "id": "groq/llama-3.3-70b-versatile",
            "providerID": "groq",
            "modelID": "llama-3.3-70b-versatile",
            "name": "Llama 3.3 70B (Groq LPU)",
            "family": "llama",
            "context": 128000,
            "output": 8192,
            "supportsTools": True,
            "supportsVision": False,
            "free": False,
        },
        {
            "id": "groq/deepseek-r1-distill-llama-70b",
            "providerID": "groq",
            "modelID": "deepseek-r1-distill-llama-70b",
            "name": "DeepSeek R1 Distill 70B (Groq)",
            "family": "deepseek",
            "context": 128000,
            "output": 8192,
            "supportsTools": True,
            "supportsVision": False,
            "free": False,
        },
    ],
    "deepseek": [
        {
            "id": "deepseek/deepseek-chat",
            "providerID": "deepseek",
            "modelID": "deepseek-chat",
            "name": "DeepSeek V3 (Direct)",
            "family": "deepseek",
            "context": 64000,
            "output": 8192,
            "supportsTools": True,
            "supportsVision": False,
            "free": False,
        },
        {
            "id": "deepseek/deepseek-reasoner",
            "providerID": "deepseek",
            "modelID": "deepseek-reasoner",
            "name": "DeepSeek R1 (Direct)",
            "family": "deepseek",
            "context": 64000,
            "output": 8192,
            "supportsTools": True,
            "supportsVision": False,
            "free": False,
        },
    ],
    "mistral": [
        {
            "id": "mistral/mistral-large-latest",
            "providerID": "mistral",
            "modelID": "mistral-large-latest",
            "name": "Mistral Large 2 (Direct)",
            "family": "mistral",
            "context": 128000,
            "output": 8192,
            "supportsTools": True,
            "supportsVision": False,
            "free": False,
        },
    ],
    "xai": [
        {
            "id": "xai/grok-2",
            "providerID": "xai",
            "modelID": "grok-2",
            "name": "Grok 2 (Direct)",
            "family": "grok",
            "context": 131072,
            "output": 8192,
            "supportsTools": True,
            "supportsVision": False,
            "free": False,
        },
    ],
    "together": [
        {
            "id": "together/meta-llama/llama-3.3-70b-instruct",
            "providerID": "together",
            "modelID": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
            "name": "Llama 3.3 70B (Together)",
            "family": "llama",
            "context": 131072,
            "output": 8192,
            "supportsTools": True,
            "supportsVision": False,
            "free": False,
        },
    ],
    "cohere": [
        {
            "id": "cohere/command-r-plus",
            "providerID": "cohere",
            "modelID": "command-r-plus-08-2024",
            "name": "Command R+ (Direct)",
            "family": "cohere",
            "context": 128000,
            "output": 4096,
            "supportsTools": True,
            "supportsVision": False,
            "free": False,
        },
    ],
}

PROVIDER_ENDPOINTS: Dict[str, str] = {
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    "openai": "https://api.openai.com/v1/chat/completions",
    "deepseek": "https://api.deepseek.com/v1/chat/completions",
    "groq": "https://api.groq.com/openai/v1/chat/completions",
    "google": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
    "mistral": "https://api.mistral.ai/v1/chat/completions",
    "together": "https://api.together.xyz/v1/chat/completions",
    "xai": "https://api.x.ai/v1/chat/completions",
}


async def list_unified_models() -> List[Dict[str, Any]]:
    """
    Return all available models across local OpenCode and configured external providers.
    Does not crash if OpenCode daemon is offline.
    """
    models: List[Dict[str, Any]] = []

    # 1. Fetch free OpenCode models (gracefully ignored if daemon is offline)
    try:
        opencode_models = await opencode_client.list_models()
        models.extend(opencode_models)
    except Exception as exc:
        print(f"[hybrid] OpenCode daemon unreachable, operating in BYOK mode: {exc}")

    # 2. Add keyed models for each configured provider
    for provider, p_models in DIRECT_PROVIDER_MODELS.items():
        if provider_keys.get_key(provider):
            models.extend(p_models)

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

        matching_provider = next(
            (p for p in provider_keys.KNOWN_PROVIDERS if model.startswith(f"{p}/")),
            None,
        )
        self.is_opencode = matching_provider is None
        self.provider = "opencode" if self.is_opencode else matching_provider
        self.raw_model = (
            model.replace(f"{matching_provider}/", "", 1)
            if matching_provider
            else model
        )
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

        # External HTTP Provider handling (OpenRouter / OpenAI-compatible / Anthropic)
        self.messages.append({"role": "user", "content": prompt})
        provider_name = self.provider
        api_key = provider_keys.get_key(provider_name)
        if not api_key:
            return {
                "text": "",
                "reasoning": "",
                "toolCalls": [],
                "tokens": {},
                "cost": 0,
                "finish": "error",
                "model": self.model,
                "error": f"{provider_name.capitalize()} API key not configured",
            }

        try:
            if provider_name == "anthropic":
                url = "https://api.anthropic.com/v1/messages"
                headers = {
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                }
                payload = {
                    "model": self.raw_model,
                    "messages": [
                        {"role": m["role"], "content": m["content"]}
                        for m in self.messages
                    ],
                    "max_tokens": 4096,
                }
            else:
                url = PROVIDER_ENDPOINTS.get(
                    provider_name, "https://openrouter.ai/api/v1/chat/completions"
                )
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                }
                if provider_name == "openrouter":
                    headers["HTTP-Referer"] = "https://github.com/SriSatyaLokesh/free-llm-council"
                    headers["X-Title"] = "Free LLM Council"

                payload = {
                    "model": self.raw_model,
                    "messages": self.messages,
                }
                if self.variant:
                    payload["reasoning_effort"] = self.variant

            res = await self.client.post(
                url,
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
            if provider_name == "anthropic":
                content_blocks = data.get("content", [])
                text = "".join(
                    b.get("text", "") for b in content_blocks if b.get("type") == "text"
                )
                reasoning = ""
                usage = data.get("usage", {})
                tokens = {
                    "input": usage.get("input_tokens", 0),
                    "output": usage.get("output_tokens", 0),
                    "reasoning": 0,
                    "total": usage.get("input_tokens", 0) + usage.get("output_tokens", 0),
                }
            else:
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
