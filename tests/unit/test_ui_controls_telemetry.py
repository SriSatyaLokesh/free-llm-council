"""Unit and integration tests for Phase 7: UI Controls, Eviction Badges & Budget Telemetry."""

import pytest
import asyncio
import json
from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend import settings, provider_keys, storage


@pytest.mark.asyncio
async def test_health_api_contract_matches_frontend():
    """Verify /api/health provides all fields required by the frontend Sidebar health badge."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/health")
        assert response.status_code in (200, 503)
        data = response.json()
        assert "status" in data
        assert "opencode" in data
        opencode = data["opencode"]
        assert "status" in opencode
        assert "port" in opencode
        assert "url" in opencode
        assert "message" in opencode


@pytest.mark.asyncio
async def test_settings_api_supports_budget_controls():
    """Verify /api/settings handles both retrieval and updates for debate mode and budget limits."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Get settings
        get_res = await ac.get("/api/settings")
        assert get_res.status_code == 200
        get_data = get_res.json()
        assert "debateMode" in get_data
        assert "caveman" in get_data
        assert "max" in get_data["caveman"]["levels"]

        # Update settings with budget caps and max debateMode
        post_res = await ac.post(
            "/api/settings",
            json={
                "debateMode": "max",
                "tokenCapPerModel": 12500,
                "tokenBudgetTotal": 45000,
                "timeLimitSeconds": 180.0,
            },
        )
        assert post_res.status_code == 200
        post_data = post_res.json()
        assert post_data["debateMode"] == "max"
        assert post_data["tokenCapPerModel"] == 12500
        assert post_data["tokenBudgetTotal"] == 45000
        assert post_data["timeLimitSeconds"] == 180.0

        # Verify internal state matches
        assert settings.get_debate_mode() == "max"
        assert settings.get_token_cap_per_model() == 12500
        assert settings.get_token_budget_total() == 45000
        assert settings.get_time_limit_seconds() == 180.0


@pytest.mark.asyncio
async def test_provider_keys_api_integration():
    """Verify /api/providers/keys endpoints support modal interactions: list, update, and remove."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Update an API key
        update_res = await ac.post(
            "/api/providers/keys",
            json={"provider": "openrouter", "key": "sk-or-v1-9876543210abcdef"},
        )
        assert update_res.status_code == 200
        update_data = update_res.json()
        assert "openrouter" in update_data
        assert update_data["openrouter"]["configured"] is True
        assert update_data["openrouter"]["preview"].endswith("cdef")

        # 2. Get keys status
        keys_res = await ac.get("/api/providers/keys")
        assert keys_res.status_code == 200
        keys_data = keys_res.json()
        assert "openrouter" in keys_data
        assert keys_data["openrouter"]["configured"] is True
        assert keys_data["openrouter"]["preview"] == update_data["openrouter"]["preview"]

        # 3. Clear the key
        clear_res = await ac.post(
            "/api/providers/keys",
            json={"provider": "openrouter", "key": ""},
        )
        assert clear_res.status_code == 200
        clear_data = clear_res.json()
        assert clear_data["openrouter"]["configured"] is False
        assert clear_data["openrouter"]["preview"] == ""


@pytest.mark.asyncio
async def test_council_session_budget_and_eviction_telemetry():
    """Verify CouncilRun captures evicted_models, retired_models, and emits early conclusion events."""
    from backend.council import CouncilRun

    run = CouncilRun(
        user_query="How to optimize React rendering performance?",
        members=["mock-model-a", "mock-model-b"],
        chairman="mock-model-a",
        rounds=2,
        token_cap_per_model=1000,
        token_budget_total=2500,
        time_limit_seconds=10.0,
    )

    # Validate initialization of budget and eviction telemetry
    assert run.token_cap_per_model == 1000
    assert run.token_budget_total == 2500
    assert run.time_limit_seconds == 10.0
    assert run.evicted_members == []
    assert run.retired_members == {}

    # Emulate eviction and retirement event emission
    emitted = []

    async def mock_emit(kind, payload):
        emitted.append((kind, payload))

    await run._evict("mock-model-b", stage="positions", round_num=None, reason="Timeout", emit=mock_emit)
    assert len(run.evicted_members) == 1
    assert run.evicted_members[0]["model"] == "mock-model-b"
    assert ("model_evicted", {"model": "mock-model-b", "stage": "positions", "round": None, "reason": "Timeout"}) in emitted

    # Record tokens exceeding token_cap_per_model and check budget limits
    run.active_members = ["mock-model-a"]
    run._record_model_tokens("mock-model-a", {"total": 1500})
    retired = await run._check_budget_limits(round_num=1, emit=mock_emit)
    assert len(retired) == 1
    assert "mock-model-a" in run.retired_members
    assert any(k == "model_retired" for k, _ in emitted)

    # Check stopping condition triggers debate_concluded_early event
    should_stop, reason = await run._check_debate_stopping_conditions(1, emit=mock_emit)
    assert should_stop is True
    assert any(k == "debate_concluded_early" for k, _ in emitted)
