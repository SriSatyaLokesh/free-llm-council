"""
Secure in-memory and environment-backed provider API key management.
Supports OpenRouter, OpenAI, Anthropic, Groq, and DeepSeek keys.
"""

import os
from typing import Any, Dict, Optional

KNOWN_PROVIDERS = (
    "openrouter",
    "openai",
    "anthropic",
    "google",
    "groq",
    "deepseek",
    "mistral",
    "xai",
    "together",
    "cohere",
)

PROVIDER_ENV_ALIASES = {
    "google": ("GOOGLE_API_KEY", "GEMINI_API_KEY"),
    "xai": ("XAI_API_KEY", "GROK_API_KEY"),
    "cohere": ("COHERE_API_KEY", "CO_API_KEY"),
}

_keys: Dict[str, Optional[str]] = {}


def _get_env_key(provider: str) -> Optional[str]:
    """Retrieve key from environment variables including known aliases."""
    aliases = PROVIDER_ENV_ALIASES.get(provider, (f"{provider.upper()}_API_KEY",))
    for var in aliases:
        val = os.getenv(var)
        if val and val.strip():
            return val.strip()
    return None


def _init_from_env() -> None:
    for provider in KNOWN_PROVIDERS:
        val = _get_env_key(provider)
        if val:
            _keys[provider] = val


_init_from_env()


def get_key(provider: str) -> Optional[str]:
    """Retrieve the raw secret key for a provider."""
    provider = provider.lower()
    return _keys.get(provider) or _get_env_key(provider)


def set_key(provider: str, key: Optional[str]) -> None:
    """Store or clear a key for a provider."""
    provider = provider.lower()
    if key and key.strip():
        _keys[provider] = key.strip()
    else:
        _keys.pop(provider, None)


def delete_key(provider: str) -> None:
    """Delete a key for a provider."""
    provider = provider.lower()
    _keys.pop(provider, None)


def redact_key(key: Optional[str]) -> str:
    """Redact a secret key so it can be safely displayed in the UI."""
    if not key:
        return ""
    if len(key) <= 8:
        return "***"
    return f"{key[:5]}...{key[-4:]}"


def get_key_statuses() -> Dict[str, Dict[str, Any]]:
    """Return configured status and redacted preview for all known providers."""
    result = {}
    for provider in KNOWN_PROVIDERS:
        raw = get_key(provider)
        result[provider] = {
            "configured": bool(raw),
            "preview": redact_key(raw) if raw else "",
        }
    return result
