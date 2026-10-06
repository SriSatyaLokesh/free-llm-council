"""
Secure in-memory and environment-backed provider API key management.
Supports OpenRouter, OpenAI, Anthropic, Groq, and DeepSeek keys.
"""

import os
from typing import Any, Dict, Optional

KNOWN_PROVIDERS = ("openrouter", "openai", "anthropic", "groq", "deepseek")

_keys: Dict[str, Optional[str]] = {}


def _init_from_env() -> None:
    for provider in KNOWN_PROVIDERS:
        env_var = f"{provider.upper()}_API_KEY"
        val = os.getenv(env_var)
        if val:
            _keys[provider] = val.strip()


_init_from_env()


def get_key(provider: str) -> Optional[str]:
    """Retrieve the raw secret key for a provider."""
    provider = provider.lower()
    return _keys.get(provider) or os.getenv(f"{provider.upper()}_API_KEY")


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
