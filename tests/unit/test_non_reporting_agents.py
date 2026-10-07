"""
Unit tests for non-reporting agents, upfront report notices, and Phase 1 dropout eviction.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, Any

from backend.council import CouncilRun
from backend import storage


def make_mock_session(model: str, ask_return_value=None):
    session = MagicMock()
    session.model = model
    session.session_id = f"sess_{model}"
    session.create = AsyncMock(return_value=session)
    session.close = AsyncMock(return_value=None)
    session.set_permissions = AsyncMock(return_value=None)
    if ask_return_value:
        session.ask = AsyncMock(return_value=ask_return_value)
    else:
        session.ask = AsyncMock(return_value={
            "text": f"Response from {model}",
            "reasoning": "",
            "toolCalls": [],
            "tokens": {"input": 50, "output": 50, "total": 100},
            "cost": 0,
            "finish": "stop",
            "model": model,
            "error": None,
        })
    return session


@pytest.mark.asyncio
async def test_session_init_failure_evicts_non_reporting_member():
    """If a member cannot initialize session, it is registered as evicted and excluded from Stage 1 & 2."""
    models = ["model-alpha", "model-unreachable"]
    mock_alpha = make_mock_session("model-alpha")
    mock_sessions = {"model-alpha": mock_alpha}

    run = CouncilRun(
        user_query="Architecture question",
        members=models,
        chairman="model-alpha",
        rounds=1,
    )

    with patch.object(run, "_make_session") as mock_make:
        async def fake_make(client, m, store, **kwargs):
            if m == "model-unreachable":
                raise RuntimeError("Connection timed out connecting to provider daemon")
            store[m] = mock_sessions[m]
            return m
        mock_make.side_effect = fake_make

        result = await run.run()

    # model-unreachable should be in evicted_members
    evicted_ids = [e["model"] for e in run.evicted_members]
    assert "model-unreachable" in evicted_ids
    assert run.evicted_members[0]["stage"] == "session_init"

    # Only model-alpha deliberated
    assert result["metadata"]["chairman"] == "model-alpha"
    assert "model-unreachable" not in [p["model"] for p in result["positions"]]


@pytest.mark.asyncio
async def test_phase_1_dropout_quits_debate_and_excluded_from_prompts():
    """If a member times out in Phase 1, it quits before debate and is excluded from debate prompts."""
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
                "finish": "error",
                "model": "model-beta",
                "error": "Timed out after 300s",
            },
        ),
        "model-gamma": make_mock_session("model-gamma"),
    }

    run = CouncilRun(
        user_query="Which database to pick?",
        members=models,
        chairman="model-alpha",
        rounds=2,
    )

    with patch.object(run, "_make_session") as mock_make:
        async def fake_make(client, m, store, **kwargs):
            store[m] = mock_sessions[m]
            return m
        mock_make.side_effect = fake_make

        result = await run.run()

    # model-beta was evicted
    assert "model-beta" in [e["model"] for e in run.evicted_members]
    # model-beta never participated in debate rounds
    for rd in result.get("debate", []):
        models_in_round = [s["model"] for s in rd.get("statements", [])]
        assert "model-beta" not in models_in_round

    # Check debate calls to survivors: prompt should not cite model-beta as an opening position
    alpha_calls = mock_sessions["model-alpha"].ask.call_args_list
    assert len(alpha_calls) >= 3  # stage 1, round 1, round 2, review, verdict
    debate_prompt_arg = alpha_calls[1][0][0]
    assert "[model-beta]" not in debate_prompt_arg


def test_executive_and_detailed_report_formatting_non_reporting_dedup():
    """Verify that reports state non-reporting agents once on top and omit them from stages & matrix."""
    conv = {
        "id": "conv-test-dedup-1234",
        "title": "Database Deliberation",
        "created_at": "2026-10-07T12:00:00Z",
        "messages": [
            {"role": "user", "content": "Should we pick Postgres or DynamoDB?"},
            {
                "role": "assistant",
                "council": {
                    "positions": [
                        {"model": "gpt-4o", "response": "I recommend PostgreSQL for relational integrity.", "error": None},
                        {"model": "claude-3-5", "response": "", "error": "Timed out after 300s"},
                        {"model": "deepseek-r1", "response": "I favor Postgres for complex indexing.", "error": None},
                    ],
                    "debate": [
                        {
                            "round": 1,
                            "statements": [
                                {"model": "gpt-4o", "response": "Rebutting alternatives; Postgres handles ACID.", "error": None},
                                {"model": "deepseek-r1", "response": "Concurring with gpt-4o.", "error": None},
                            ],
                        }
                    ],
                    "review": [
                        {"model": "gpt-4o", "ranking": "1. Response A\n2. Response B", "error": None},
                        {"model": "deepseek-r1", "ranking": "1. Response A\n2. Response B", "error": None},
                    ],
                    "verdict": {
                        "model": "gpt-4o",
                        "response": "Final synthesized decision: use Postgres.",
                        "sections": {
                            "decision": "Use PostgreSQL with automated replicas.",
                            "reasoning": "Strong consistency and indexing outpace NoSQL for this schema.",
                            "tradeoffs": "Requires dedicated connection pooling.",
                            "dissent": "None unresolved.",
                            "confidence": "High",
                        },
                    },
                    "metadata": {
                        "members": ["gpt-4o", "deepseek-r1"],
                        "requested_members": ["gpt-4o", "claude-3-5", "deepseek-r1"],
                        "evicted_members": [
                            {"model": "claude-3-5", "stage": "positions", "reason": "Timed out after 300s"}
                        ],
                        "total_tokens": 12500,
                    },
                },
            },
        ],
    }

    # 1. Executive report
    exec_md = storage.format_conversation_executive(conv)
    assert "> **Council Attendance Notice:**" in exec_md
    assert "`claude-3-5`: Timed out after 300s" in exec_md

    # Stage 1 should ONLY have gpt-4o and deepseek-r1
    assert "### Model: `gpt-4o`" in exec_md
    assert "### Model: `deepseek-r1`" in exec_md
    assert "### Model: `claude-3-5`" not in exec_md
    assert "Timed out after 300s" not in exec_md.split("## Stage 1: Opening Positions")[1]

    # 2. Detailed report
    det_md = storage.format_conversation_detailed(conv)
    assert "> **Council Attendance Notice:**" in det_md
    assert "`claude-3-5`: Timed out after 300s" in det_md

    # Matrix table should only contain active models
    matrix_section = det_md.split("## Comparative Model Deliberation Matrix")[1].split("## Strategic Decision")[0]
    assert "| `gpt-4o` |" in matrix_section
    assert "| `deepseek-r1` |" in matrix_section
    assert "| `claude-3-5` |" not in matrix_section

    # Stage 1 transcript in detailed report
    stage1_detailed = det_md.split("### Stage 1: Opening Positions")[1].split("### Stage 2: Peer Debate")[0]
    assert "#### Model: `gpt-4o`" in stage1_detailed
    assert "#### Model: `deepseek-r1`" in stage1_detailed
    assert "#### Model: `claude-3-5`" not in stage1_detailed

    # HTML rendering
    html_rep = storage.render_report_html(conv, mode="detailed")
    assert "Council Attendance Notice" in html_rep
    assert "claude-3-5" in html_rep
