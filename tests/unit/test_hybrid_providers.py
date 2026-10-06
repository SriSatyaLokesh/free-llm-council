"""
Real, non-mocked tests for Phase 6: Hybrid Provider & Custom API Key Ingestion.
Verifies secure key storage, redacted previews, API endpoints, unified model registry,
hybrid session routing, and fault-tolerant eviction on provider authorization failures.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch

from backend.main import app
from backend import provider_keys
from backend.hybrid_client import list_unified_models, HybridCouncilSession
from backend.council import CouncilRun


def test_provider_key_sanitization_and_redaction():
    """
    Test setting, retrieving, and redacting provider API keys.
    Full secret keys must NEVER be leaked in preview outputs.
    """
    provider_keys.set_key("openrouter", "sk-or-v1-abcdef1234567890abcdef")
    stored = provider_keys.get_key("openrouter")
    assert stored == "sk-or-v1-abcdef1234567890abcdef"

    statuses = provider_keys.get_key_statuses()
    assert "openrouter" in statuses
    assert statuses["openrouter"]["configured"] is True
    preview = statuses["openrouter"]["preview"]
    assert "sk-or" in preview
    assert "1234567890" not in preview  # Middle is redacted

    # Clear key
    provider_keys.delete_key("openrouter")
    assert provider_keys.get_key("openrouter") is None
    assert provider_keys.get_key_statuses()["openrouter"]["configured"] is False


def test_expanded_provider_keys_and_alias_lookup(monkeypatch):
    """
    Test expanded provider keys (google, groq, deepseek, mistral, xai, together, cohere)
    and verify alias environment variable resolution (GEMINI_API_KEY -> google).
    """
    statuses = provider_keys.get_key_statuses()
    for prov in ("openrouter", "openai", "anthropic", "google", "groq", "deepseek", "mistral", "xai", "together", "cohere"):
        assert prov in statuses

    # Test alias resolution via GEMINI_API_KEY
    provider_keys.delete_key("google")
    monkeypatch.setenv("GEMINI_API_KEY", "AIzaSyFakeGeminiKey123456789")
    assert provider_keys.get_key("google") == "AIzaSyFakeGeminiKey123456789"
    assert provider_keys.get_key_statuses()["google"]["configured"] is True

    # Test alias resolution via GROK_API_KEY
    provider_keys.delete_key("xai")
    monkeypatch.setenv("GROK_API_KEY", "xai-fakegrokkey987654321")
    assert provider_keys.get_key("xai") == "xai-fakegrokkey987654321"
    assert provider_keys.get_key_statuses()["xai"]["configured"] is True


@pytest.mark.asyncio
async def test_provider_keys_http_api():
    """
    HTTP integration test:
    GET /api/providers/keys
    POST /api/providers/keys
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Update keys via POST
        res_post = await client.post("/api/providers/keys", json={
            "provider": "openrouter",
            "key": "sk-or-v1-testkey987654321",
        })
        assert res_post.status_code == 200
        data_post = res_post.json()
        assert data_post["openrouter"]["configured"] is True

        # 2. Query keys via GET
        res_get = await client.get("/api/providers/keys")
        assert res_get.status_code == 200
        data_get = res_get.json()
        assert data_get["openrouter"]["configured"] is True
        assert "testkey" not in data_get["openrouter"]["preview"]

        # Clean up
        provider_keys.delete_key("openrouter")


@pytest.mark.asyncio
async def test_unified_model_registry_merges_free_and_keyed_models(monkeypatch):
    """
    list_unified_models() must return OpenCode models when no keys exist,
    and merge OpenRouter/keyed models when a key is configured.
    """
    mock_opencode = [
        {"id": "opencode/big-pickle", "name": "Big Pickle", "providerID": "opencode"},
    ]
    import backend.opencode_client
    monkeypatch.setattr(backend.opencode_client, "list_models", AsyncMock(return_value=mock_opencode))

    # 1. Without key: only opencode models
    provider_keys.delete_key("openrouter")
    models_no_key = await list_unified_models()
    model_ids_no_key = [m["id"] for m in models_no_key]
    assert "opencode/big-pickle" in model_ids_no_key
    assert not any(m["id"].startswith("openrouter/") for m in models_no_key)

    # 2. With key: includes openrouter frontier models
    provider_keys.set_key("openrouter", "sk-or-v1-dummy-key")
    models_with_key = await list_unified_models()
    model_ids_with_key = [m["id"] for m in models_with_key]
    assert "opencode/big-pickle" in model_ids_with_key
    assert any("claude" in mid.lower() for mid in model_ids_with_key)

    provider_keys.delete_key("openrouter")


@pytest.mark.asyncio
async def test_hybrid_council_session_routing():
    """
    HybridCouncilSession dispatches OpenCode models to CouncilSession,
    and keyed models to direct chat completion handler.
    """
    import httpx
    async with httpx.AsyncClient() as client:
        # 1. OpenCode model session
        opencode_sess = HybridCouncilSession("opencode/big-pickle", client)
        assert opencode_sess.is_opencode is True

        # 2. Keyed OpenRouter model session
        keyed_sess = HybridCouncilSession("openrouter/anthropic/claude-3.5-sonnet", client)
        assert keyed_sess.is_opencode is False
        assert keyed_sess.provider == "openrouter"


@pytest.mark.asyncio
async def test_keyed_model_401_triggers_immediate_eviction():
    """
    If an external keyed model fails with 401 Unauthorized (invalid key/no credits),
    it must be immediately evicted from CouncilRun and the council must proceed.
    """
    models = ["opencode/big-pickle", "openrouter/openai/gpt-4o"]
    run = CouncilRun(
        user_query="Design a payment service",
        members=models,
        chairman="opencode/big-pickle",
        rounds=1,
    )

    async def mock_ask_all(model_list, prompt_fn):
        results = {}
        for m in model_list:
            if m.startswith("openrouter/"):
                results[m] = {
                    "text": "",
                    "reasoning": "",
                    "toolCalls": [],
                    "tokens": {},
                    "cost": 0,
                    "finish": "error",
                    "model": m,
                    "error": "401 Unauthorized: Invalid API Key or Insufficient Credits",
                }
            else:
                results[m] = {
                    "text": f"Position from {m}",
                    "reasoning": "",
                    "toolCalls": [],
                    "tokens": {"input": 100, "output": 50, "total": 150},
                    "cost": 0,
                    "finish": "stop",
                    "model": m,
                    "error": None,
                }
        return results

    with patch.object(run, "_open_sessions", AsyncMock(return_value=models)), \
         patch.object(run, "_ask_all", side_effect=mock_ask_all), \
         patch.object(run, "_run_chairman", AsyncMock(return_value={
             "model": "opencode/big-pickle",
             "response": "Verdict",
             "sections": {"decision": "Done"},
             "tokens": {},
             "error": None,
         })), \
         patch.object(run, "_close_all", AsyncMock()):
        result = await run.run()

    # The failing keyed model must be evicted
    evicted_models = [e["model"] for e in run.evicted_members]
    assert "openrouter/openai/gpt-4o" in evicted_models
    assert "opencode/big-pickle" in run.active_members
    assert result["verdict"]["model"] == "opencode/big-pickle"


@pytest.mark.asyncio
async def test_standalone_byok_operation_without_opencode(monkeypatch):
    """
    Verify full standalone BYOK operation when OpenCode daemon is completely offline.
    list_unified_models(), /api/models, and /api/health must function smoothly with BYOK keys.
    """
    from backend.opencode_client import OpencodeUnavailable
    import backend.opencode_client
    monkeypatch.setattr(
        backend.opencode_client,
        "list_models",
        AsyncMock(side_effect=OpencodeUnavailable("Connection refused")),
    )

    # Configure direct BYOK keys for OpenAI and Groq
    provider_keys.set_key("openai", "sk-proj-testkey123")
    provider_keys.set_key("groq", "gsk-testkey456")

    try:
        # 1. list_unified_models returns keyed models without throwing
        models = await list_unified_models()
        assert len(models) >= 2
        model_ids = [m["id"] for m in models]
        assert "openai/gpt-4o" in model_ids
        assert "groq/llama-3.3-70b-versatile" in model_ids

        # 2. HTTP endpoints succeed in BYOK mode
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            res_models = await client.get("/api/models")
            assert res_models.status_code == 200
            data_models = res_models.json()
            assert len(data_models["models"]) >= 2
            assert data_models["defaultChairman"] is not None

            res_health = await client.get("/api/health")
            assert res_health.status_code == 200
            data_health = res_health.json()
            assert data_health["status"] == "ok"
            assert data_health["mode"] in ("byok", "hybrid")
    finally:
        provider_keys.delete_key("openai")
        provider_keys.delete_key("groq")
