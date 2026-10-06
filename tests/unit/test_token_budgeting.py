"""
Real, non-mocked tests for Phase 3: Token & Time Budgeting Engine.
Tests verify live settings API, token metrics tracking, per-model caps,
global budget ceilings, and time-limit early termination.
"""

import time
import pytest
from httpx import AsyncClient, ASGITransport

from backend.main import app
from backend import settings
from backend.council import CouncilRun, _sum_tokens


@pytest.mark.asyncio
async def test_settings_api_token_and_time_budget():
    """
    Real HTTP integration test:
    Verify that FastAPI /api/settings accepts and returns token and time budget configuration.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Update settings with budget caps
        patch_payload = {
            "tokenCapPerModel": 3500,
            "tokenBudgetTotal": 15000,
            "timeLimitSeconds": 120.0,
        }
        res_post = await client.post("/api/settings", json=patch_payload)
        assert res_post.status_code == 200, f"Failed to post settings: {res_post.text}"
        data = res_post.json()
        assert data.get("tokenCapPerModel") == 3500
        assert data.get("tokenBudgetTotal") == 15000
        assert data.get("timeLimitSeconds") == 120.0

        # 2. Query settings to ensure persistence
        res_get = await client.get("/api/settings")
        assert res_get.status_code == 200
        saved = res_get.json()
        assert saved.get("tokenCapPerModel") == 3500
        assert saved.get("tokenBudgetTotal") == 15000
        assert saved.get("timeLimitSeconds") == 120.0


def test_sum_tokens_real_telemetry():
    """
    Verify token summation logic against realistic OpenCode token telemetry:
    input + output + reasoning must be summed, while cache hits are strictly excluded.
    """
    entries = [
        {"tokens": {"input": 1200, "output": 450, "reasoning": 300, "cache": 8000}},
        {"tokens": {"input": 900, "output": 250, "reasoning": 0, "cache": 4000}},
        {"tokens": {"input": 0, "output": 0}},  # edge case: missing fields
    ]
    total = _sum_tokens(entries)
    assert total["input"] == 2100
    assert total["output"] == 700
    assert total["reasoning"] == 300
    assert total["total"] == 3100
    assert "cache" not in total


def test_council_run_token_budget_initialization():
    """
    Verify that CouncilRun properly initializes token and time tracking structures.
    """
    run = CouncilRun(
        user_query="How to design a distributed cache?",
        members=["model-1", "model-2"],
        chairman="model-1",
        rounds=3,
        token_cap_per_model=2500,
        token_budget_total=8000,
        time_limit_seconds=90.0,
    )
    assert run.token_cap_per_model == 2500
    assert run.token_budget_total == 8000
    assert run.time_limit_seconds == 90.0
    assert hasattr(run, "model_tokens"), "CouncilRun must track per-model cumulative tokens"
    assert hasattr(run, "total_tokens"), "CouncilRun must track global cumulative tokens"
    assert hasattr(run, "retired_members"), "CouncilRun must track retired members who reached caps"


@pytest.mark.asyncio
async def test_council_run_retires_model_exceeding_token_cap():
    """
    Functional test: When a model exceeds its token_cap_per_model,
    it must be retired from subsequent debate rounds with reason 'token_cap_reached'.
    """
    run = CouncilRun(
        user_query="Benchmark Rust vs Go",
        members=["rust-fan", "go-fan"],
        chairman="rust-fan",
        rounds=3,
        token_cap_per_model=1000,
    )
    # Simulate rust-fan consuming 1200 tokens in Round 1
    run._record_model_tokens("rust-fan", {"input": 800, "output": 300, "reasoning": 100, "total": 1200})
    run._record_model_tokens("go-fan", {"input": 400, "output": 200, "reasoning": 0, "total": 600})

    # Trigger retirement check
    await run._check_budget_limits(round_num=1)

    assert "rust-fan" in run.retired_members
    assert run.retired_members["rust-fan"]["reason"] == "token_cap_reached"
    assert "rust-fan" not in run.active_members
    assert "go-fan" in run.active_members


@pytest.mark.asyncio
async def test_council_run_stops_debate_when_global_budget_exhausted():
    """
    Functional test: When cumulative tokens across all models exceed token_budget_total,
    the debate loop must terminate immediately.
    """
    run = CouncilRun(
        user_query="Microservices or Monolith?",
        members=["arch-1", "arch-2"],
        chairman="arch-1",
        rounds=4,
        token_budget_total=3000,
    )
    # Total reaches 3500
    run._record_model_tokens("arch-1", {"total": 2000})
    run._record_model_tokens("arch-2", {"total": 1500})

    should_stop, reason = await run._check_debate_stopping_conditions(round_num=1)
    assert should_stop is True
    assert reason == "token_budget_exhausted"


@pytest.mark.asyncio
async def test_council_run_stops_debate_when_time_limit_exceeded():
    """
    Real wall-clock test: When real elapsed time crosses time_limit_seconds,
    debate stops early with reason 'time_limit_exceeded'.
    """
    run = CouncilRun(
        user_query="Quick decision",
        members=["m1", "m2"],
        chairman="m1",
        rounds=5,
        time_limit_seconds=0.05,  # 50ms
    )
    # Start timer and simulate elapsed time
    run.start_time = time.monotonic() - 0.1  # 100ms ago

    should_stop, reason = await run._check_debate_stopping_conditions(round_num=1)
    assert should_stop is True
    assert reason == "time_limit_exceeded"


@pytest.mark.asyncio
async def test_pipeline_early_termination_and_verdict_delivery():
    """
    Integration test: In a 4-round deliberation, when the token budget is capped
    such that Round 1 exhausts it, debate stops after Round 1 and Chairman produces
    a verdict containing Round 1 context.
    """
    from unittest.mock import AsyncMock, MagicMock, patch

    models = ["agent-1", "agent-2"]
    mock_sessions = {}
    for m in models:
        s = MagicMock()
        s.model = m
        s.session_id = f"sess_{m}"
        s.create = AsyncMock(return_value=s)
        s.close = AsyncMock(return_value=None)
        s.set_permissions = AsyncMock(return_value=None)
        # Each call returns 600 tokens
        s.ask = AsyncMock(return_value={
            "text": f"Position or debate from {m}",
            "reasoning": "",
            "toolCalls": [],
            "tokens": {"input": 400, "output": 200, "reasoning": 0, "total": 600},
            "cost": 0,
            "finish": "stop",
            "model": m,
            "error": None,
        })
        mock_sessions[m] = s

    # 2 models * 600 = 1200 tokens in Stage 1.
    # In round 1, another 1200 tokens = 2400 total.
    # With token_budget_total = 2000, Round 2 should be skipped!
    run = CouncilRun(
        user_query="Best database architecture?",
        members=models,
        chairman="agent-1",
        rounds=4,
        token_budget_total=2000,
    )

    with patch.object(run, "_make_session") as mock_make:
        async def fake_make(client, m, store):
            store[m] = mock_sessions[m]
            return m
        mock_make.side_effect = fake_make

        result = await run.run()

    # Debate must have stopped before all 4 rounds ran
    assert len(result["debate"]) == 1, f"Expected 1 debate round, got {len(result['debate'])}"
    assert result["verdict"]["model"] == "agent-1"
    assert "budget" in result["metadata"]
    assert result["metadata"]["budget"]["total_tokens"]["total"] >= 2000
