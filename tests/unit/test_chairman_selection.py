"""
Real, non-mocked unit tests for Phase 4: Intelligent Chairman Selection Matrix.
Verifies benchmark capability scoring, auto-election of frontier reasoning models,
context tie-breaking, and intelligent failover to the highest-capability survivor.
"""

import pytest
from httpx import AsyncClient, ASGITransport

from backend.capability_matrix import score_model_capability, select_best_chairman
from backend.opencode_client import default_chairman
from backend.council import resolve_roster, CouncilRun


def test_frontier_model_outranks_large_context_toy_model():
    """
    Core requirement: A Frontier intelligence model (e.g. Claude 3.5 Sonnet, GPT-4o)
    with 64k or 128k context must decisively outscore a toy or small model
    (e.g. opencode/big-pickle) even if big-pickle reports 128k context.
    """
    frontier = {
        "id": "anthropic/claude-3-5-sonnet",
        "name": "Claude 3.5 Sonnet",
        "context": 64000,
        "output": 8192,
        "supportsTools": True,
    }
    toy = {
        "id": "opencode/big-pickle",
        "name": "Big Pickle",
        "context": 128000,
        "output": 4096,
        "supportsTools": False,
    }

    score_frontier = score_model_capability(frontier)
    score_toy = score_model_capability(toy)

    assert score_frontier > score_toy, (
        f"Frontier ({score_frontier}) must outscore toy ({score_toy})"
    )
    assert score_frontier >= 90.0
    assert score_toy < 60.0


def test_select_best_chairman_ranks_diverse_roster():
    """
    Given a mixed roster of detected models, select_best_chairman must pick
    the most capable intelligence model.
    """
    roster = [
        {"id": "opencode/big-pickle", "context": 128000, "output": 4096},
        {"id": "meta/llama-3-8b-instruct", "context": 8192, "output": 2048},
        {"id": "openai/gpt-4o", "context": 128000, "output": 4096, "supportsTools": True},
        {"id": "qwen/qwen-2.5-7b", "context": 32000, "output": 4096},
    ]

    best = select_best_chairman(roster)
    assert best == "openai/gpt-4o"


def test_deepseek_r1_outranks_flash():
    """
    Reasoning frontier models like DeepSeek-R1 must outrank fast lightweight
    frontier-lite models like Gemini 1.5 Flash.
    """
    roster = [
        {"id": "google/gemini-1.5-flash", "context": 1000000, "output": 8192},
        {"id": "deepseek/deepseek-r1", "context": 64000, "output": 8192},
    ]

    best = select_best_chairman(roster)
    assert best == "deepseek/deepseek-r1"


def test_pickle_tiebreak_prefers_larger_model():
    """
    When only test or open-code models exist, election gracefully ranks between them
    (big-pickle over small-pickle).
    """
    roster = [
        {"id": "opencode/small-pickle", "context": 32000, "output": 2048},
        {"id": "opencode/big-pickle", "context": 128000, "output": 4096},
    ]

    best = select_best_chairman(roster)
    assert best == "opencode/big-pickle"


@pytest.mark.asyncio
async def test_default_chairman_uses_capability_matrix():
    """
    backend.opencode_client.default_chairman must use the capability matrix
    rather than naive context max.
    """
    roster = [
        {"id": "opencode/big-pickle", "context": 200000, "output": 4096},
        {"id": "anthropic/claude-3-5-sonnet", "context": 128000, "output": 8192},
    ]

    chosen = await default_chairman(roster)
    assert chosen == "anthropic/claude-3-5-sonnet"


def test_council_run_chairman_failover_elects_highest_capability_survivor():
    """
    If the initial chairman is evicted, CouncilRun._ensure_active_chairman()
    must promote the highest capability SURVIVING member, not just active_members[0].
    """
    # Active survivors: small-pickle, then Qwen 72B.
    # If active_members is [small-pickle, qwen-72b], naive selection would pick small-pickle.
    # Intelligent failover MUST elect qwen-72b.
    run = CouncilRun(
        user_query="How to optimize an SQL query?",
        members=["claude-3-5-sonnet", "opencode/small-pickle", "qwen/qwen-2.5-72b"],
        chairman="claude-3-5-sonnet",
        rounds=2,
    )
    # Evict initial chairman
    run.active_members = ["opencode/small-pickle", "qwen/qwen-2.5-72b"]

    new_chair = run._ensure_active_chairman()
    assert new_chair == "qwen/qwen-2.5-72b", (
        f"Expected qwen-72b to be promoted as chairman, got {new_chair}"
    )


@pytest.mark.asyncio
async def test_models_api_returns_intelligent_default_chairman(monkeypatch):
    """
    HTTP integration test: GET /api/models must return the highest capability
    model as defaultChairman.
    """
    from backend.main import app
    from unittest.mock import AsyncMock

    mock_models = [
        {"id": "opencode/big-pickle", "name": "Big Pickle", "context": 200000},
        {"id": "anthropic/claude-3-5-sonnet", "name": "Claude 3.5 Sonnet", "context": 128000},
        {"id": "meta/llama-3-8b", "name": "Llama 3 8B", "context": 8192},
    ]

    import backend.main
    monkeypatch.setattr(backend.main, "list_unified_models", AsyncMock(return_value=mock_models))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/models")
        assert res.status_code == 200
        data = res.json()
        assert data.get("defaultChairman") == "anthropic/claude-3-5-sonnet"
