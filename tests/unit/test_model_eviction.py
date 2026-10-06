"""
Unit tests for Phase 2: Dynamic Member Fault-Tolerance & Model Eviction.
"""

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, Any

from backend.council import CouncilRun


def make_mock_session(model: str, ask_side_effects=None, ask_return_value=None):
    """Create a mock CouncilSession that records ask() calls and session lifecycle."""
    session = MagicMock()
    session.model = model
    session.session_id = f"sess_{model}"
    session.create = AsyncMock(return_value=session)
    session.close = AsyncMock(return_value=None)
    session.set_permissions = AsyncMock(return_value=None)

    if ask_side_effects:
        session.ask = AsyncMock(side_effect=ask_side_effects)
    elif ask_return_value:
        session.ask = AsyncMock(return_value=ask_return_value)
    else:
        session.ask = AsyncMock(return_value={
            "text": f"Response from {model}",
            "reasoning": "",
            "toolCalls": [],
            "tokens": {"input": 100, "output": 50, "reasoning": 0, "total": 150},
            "cost": 0,
            "finish": "stop",
            "model": model,
            "error": None,
        })
    return session


@pytest.mark.asyncio
async def test_eviction_on_stage1_failure():
    """
    If a model fails in Stage 1, it must be evicted immediately and NEVER
    called again in Stage 2 (Debate), Stage 3 (Review), or Stage 4.
    """
    models = ["model-alpha", "model-beta", "model-gamma"]
    mock_sessions = {
        "model-alpha": make_mock_session("model-alpha"),
        "model-beta": make_mock_session(
            "model-beta",
            ask_return_value={
                "text": "",
                "reasoning": "",
                "toolCalls": [],
                "tokens": {},
                "cost": 0,
                "finish": "error",
                "model": "model-beta",
                "error": "Timed out after 300s",
            },
        ),
        "model-gamma": make_mock_session("model-gamma"),
    }

    run = CouncilRun(
        user_query="Should we use Postgres?",
        members=models,
        chairman="model-alpha",
        rounds=2,
    )

    with patch.object(run, "_make_session") as mock_make:
        async def fake_make(client, m, store):
            store[m] = mock_sessions[m]
            return m
        mock_make.side_effect = fake_make

        result = await run.run()

    # 1. model-beta should be evicted
    assert hasattr(run, "evicted_members"), "CouncilRun must have an evicted_members registry"
    evicted_ids = [e["model"] for e in run.evicted_members]
    assert "model-beta" in evicted_ids

    # 2. model-beta must NOT be called in debate rounds (Stage 2)
    # Stage 1 made 1 call to model-beta (which failed). It should have received EXACTLY 1 ask() call total!
    assert mock_sessions["model-beta"].ask.call_count == 1, (
        f"model-beta was called {mock_sessions['model-beta'].ask.call_count} times, expected exactly 1"
    )

    # 3. Active survivors (alpha and gamma) should have continued through debate and review
    assert mock_sessions["model-alpha"].ask.call_count >= 3  # position + 2 debate rounds + review + verdict
    assert mock_sessions["model-gamma"].ask.call_count >= 3

    # 4. Evicted members metadata must be recorded in result
    meta = result.get("metadata", {})
    assert "evicted_members" in meta
    assert any(e["model"] == "model-beta" for e in meta["evicted_members"])


@pytest.mark.asyncio
async def test_eviction_on_debate_round_failure():
    """
    If a model succeeds in Stage 1 but crashes in Debate Round 1,
    it must be evicted immediately and excluded from Debate Round 2 and Stage 3.
    """
    models = ["model-alpha", "model-beta"]

    # model-beta succeeds in Stage 1, but raises in Round 1
    call_count = 0
    async def beta_ask(prompt, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "text": "Beta Stage 1 position",
                "reasoning": "",
                "toolCalls": [],
                "tokens": {"total": 100},
                "model": "model-beta",
                "error": None,
            }
        # Round 1 fails
        return {
            "text": "",
            "reasoning": "",
            "toolCalls": [],
            "tokens": {},
            "model": "model-beta",
            "error": "HTTP 500 provider crashed",
        }

    mock_beta = make_mock_session("model-beta", ask_side_effects=beta_ask)
    mock_alpha = make_mock_session("model-alpha")

    mock_sessions = {"model-alpha": mock_alpha, "model-beta": mock_beta}

    run = CouncilRun(
        user_query="Should we migrate to TypeScript?",
        members=models,
        chairman="model-alpha",
        rounds=2,
    )

    with patch.object(run, "_make_session") as mock_make:
        async def fake_make(client, m, store):
            store[m] = mock_sessions[m]
            return m
        mock_make.side_effect = fake_make

        result = await run.run()

    # model-beta should be in evicted_members
    evicted_ids = [e["model"] for e in run.evicted_members]
    assert "model-beta" in evicted_ids

    # model-beta had 1 call (Stage 1) + 1 call (Debate Round 1).
    # It must NOT be called in Debate Round 2 (call 3) or Stage 3 Review (call 4)!
    assert mock_beta.ask.call_count == 2, (
        f"model-beta was called {mock_beta.ask.call_count} times, expected exactly 2 (Stage 1 + Round 1)"
    )


@pytest.mark.asyncio
async def test_chairman_failover_when_chairman_evicted():
    """
    If the designated chairman fails during deliberation, the council
    must promote the next surviving member to Chairman and produce a verdict.
    """
    models = ["model-alpha", "model-beta"]
    # model-beta is Chairman, but fails in Stage 1
    mock_beta = make_mock_session(
        "model-beta",
        ask_return_value={"text": "", "tokens": {}, "model": "model-beta", "error": "rate limited"}
    )
    mock_alpha = make_mock_session(
        "model-alpha",
        ask_return_value={"text": "Alpha position and verdict", "tokens": {"total": 200}, "model": "model-alpha", "error": None}
    )

    mock_sessions = {"model-alpha": mock_alpha, "model-beta": mock_beta}

    run = CouncilRun(
        user_query="How to optimize database queries?",
        members=models,
        chairman="model-beta",  # Failing chairman
        rounds=1,
    )

    with patch.object(run, "_make_session") as mock_make:
        async def fake_make(client, m, store):
            store[m] = mock_sessions[m]
            return m
        mock_make.side_effect = fake_make

        result = await run.run()

    # Chairman should have failed over to model-alpha
    verdict = result.get("verdict", {})
    assert verdict.get("model") == "model-alpha", f"Expected chairman failover to model-alpha, got {verdict.get('model')}"
    assert verdict.get("response") != "", "Verdict should have a response from failover chairman"
    assert "model-beta" in [e["model"] for e in run.evicted_members]


@pytest.mark.asyncio
async def test_eviction_emits_stream_event():
    """
    When run_stream is used, an eviction should emit a 'model_evicted' event.
    """
    models = ["model-alpha", "model-beta"]
    mock_sessions = {
        "model-alpha": make_mock_session("model-alpha"),
        "model-beta": make_mock_session(
            "model-beta",
            ask_return_value={"text": "", "tokens": {}, "model": "model-beta", "error": "network drop"}
        ),
    }

    run = CouncilRun(
        user_query="Test query",
        members=models,
        chairman="model-alpha",
        rounds=1,
    )

    queue = asyncio.Queue()
    with patch.object(run, "_make_session") as mock_make:
        async def fake_make(client, m, store):
            store[m] = mock_sessions[m]
            return m
        mock_make.side_effect = fake_make

        await run.run_stream(queue)

    events = []
    while not queue.empty():
        item = await queue.get()
        if item[0] is not None:
            events.append(item[0])

    assert "model_evicted" in events, f"Expected 'model_evicted' in emitted events: {events}"
