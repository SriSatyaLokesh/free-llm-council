"""Unit and integration tests for Phase 11: Human-in-the-Loop Mid-Debate Steering & Resource Injection."""

import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend import council, prompts, storage


def test_active_run_registry_and_steering_injection():
    """Verify active run registration and steering injection on CouncilRun."""
    conv_id = "test-steering-conv-1"
    run = council.CouncilRun(
        user_query="Should we use Postgres or ClickHouse?",
        members=["model-a", "model-b"],
        chairman="model-a",
        rounds=2,
    )

    # Initially empty guidance
    assert hasattr(run, "injected_guidance")
    assert len(run.injected_guidance) == 0

    # Inject steering
    guidance = run.inject_steering(
        message="Focus strictly on analytics workload with 10M rows/day.",
        resources=["https://clickhouse.com/docs", "https://postgresql.org"],
    )
    assert guidance["message"] == "Focus strictly on analytics workload with 10M rows/day."
    assert len(guidance["resources"]) == 2
    assert len(run.injected_guidance) == 1

    # Active run registration
    council.register_active_run(conv_id, run)
    assert council.get_active_run(conv_id) is run

    council.unregister_active_run(conv_id)
    assert council.get_active_run(conv_id) is None


def test_prompts_integrate_human_guidance():
    """Verify debate and verdict prompts include human guidance and directives."""
    guidance_list = [
        {
            "message": "Do not recommend MongoDB. Consider ACID transactions paramount.",
            "resources": ["https://jepsen.io/analyses"],
        }
    ]

    # Debate prompt test
    debate_text = prompts.debate_prompt(
        user_query="Which database to choose?",
        your_model="model-a",
        positions_text="Pos A",
        prior_rounds_text="Round 1 text",
        round_number=2,
        total_rounds=2,
        human_guidance=guidance_list,
    )
    assert "HUMAN OPERATOR GUIDANCE & STEERING" in debate_text
    assert "Do not recommend MongoDB" in debate_text
    assert "https://jepsen.io/analyses" in debate_text
    assert "MANDATORY DIRECTIVE" in debate_text

    # Verdict prompt test
    verdict_text = prompts.verdict_prompt(
        user_query="Which database to choose?",
        positions_text="Pos A",
        debate_text="Debate text",
        review_text="Review text",
        aggregate_text="Aggregate text",
        chairman_model="model-a",
        human_guidance=guidance_list,
    )
    assert "HUMAN OPERATOR GUIDANCE & STEERING" in verdict_text
    assert "Do not recommend MongoDB" in verdict_text
    assert "Explicitly highlight how the final verdict aligns with or addresses the operator's input" in verdict_text


@pytest.mark.asyncio
async def test_steer_http_api_endpoints():
    """Verify HTTP POST /api/conversations/{id}/steer behavior."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        conv_id = "test-steer-http-conv"
        storage.create_conversation(conv_id)

        try:
            # 1. No active run -> 400 Bad Request
            res_no_run = await client.post(
                f"/api/conversations/{conv_id}/steer",
                json={"message": "Pause and pivot!"},
            )
            assert res_no_run.status_code == 400
            assert "No active council run" in res_no_run.json()["detail"]

            # 2. Register mock active run
            run = council.CouncilRun(
                user_query="Test query",
                members=["model-a"],
                chairman="model-a",
            )
            council.register_active_run(conv_id, run)

            # 3. Empty message -> 400 Bad Request
            res_empty = await client.post(
                f"/api/conversations/{conv_id}/steer",
                json={"message": "   "},
            )
            assert res_empty.status_code == 400

            # 4. Valid steering injection
            res_steer = await client.post(
                f"/api/conversations/{conv_id}/steer",
                json={
                    "message": "Focus on horizontal partitioning.",
                    "resources": ["https://vitess.io"],
                },
            )
            assert res_steer.status_code == 200
            data = res_steer.json()
            assert data["status"] == "ok"
            assert data["steering"]["message"] == "Focus on horizontal partitioning."
            assert data["steering"]["resources"] == ["https://vitess.io"]
            assert len(run.injected_guidance) == 1

        finally:
            council.unregister_active_run(conv_id)
            storage.delete_conversation(conv_id)


@pytest.mark.asyncio
async def test_council_run_incorporates_steering_in_debate_and_verdict():
    """Verify that steering injected into a CouncilRun appears in debate prompt, queue events, and verdict metadata."""
    from unittest.mock import AsyncMock, MagicMock, patch

    asked_prompts = []

    def make_mock(model: str):
        session = MagicMock()
        session.model = model
        session.session_id = f"sess_{model}"
        session.create = AsyncMock(return_value=session)
        session.close = AsyncMock(return_value=None)
        session.set_permissions = AsyncMock(return_value=None)

        async def ask_fake(prompt: str):
            asked_prompts.append((model, prompt))
            if "FINAL RANKING:" in prompt or "anonymized" in prompt:
                return {
                    "text": "FINAL RANKING:\n1. Response A\n2. Response B",
                    "reasoning": "",
                    "toolCalls": [],
                    "tokens": {"total": 50},
                    "cost": 0,
                    "finish": "stop",
                    "model": model,
                    "error": None,
                }
            elif "## Decision" in prompt or "Chairman" in prompt:
                return {
                    "text": "## Decision\nDecided\n## Reasoning\nReasoned\n## Tradeoffs\nTraded\n## Dissent\nNone\n## Confidence\nHigh",
                    "reasoning": "",
                    "toolCalls": [],
                    "tokens": {"total": 50},
                    "cost": 0,
                    "finish": "stop",
                    "model": model,
                    "error": None,
                }
            return {
                "text": f"Arg from {model}",
                "reasoning": "",
                "toolCalls": [],
                "tokens": {"total": 50},
                "cost": 0,
                "finish": "stop",
                "model": model,
                "error": None,
            }

        session.ask = AsyncMock(side_effect=ask_fake)
        return session

    mock_sessions = {
        "m1": make_mock("m1"),
        "m2": make_mock("m2"),
    }

    queue = asyncio.Queue()
    run = council.CouncilRun(
        user_query="Which distributed cache to use?",
        members=["m1", "m2"],
        chairman="m1",
        rounds=2,
    )

    # Inject steering before / during run
    run.inject_steering(
        message="Strictly prioritize Redis cluster over Hazelcast.",
        resources=["https://redis.io"],
    )

    with patch("backend.hybrid_client.HybridCouncilSession", side_effect=lambda m, *a, **kw: mock_sessions[m]):
        result = await run.run_stream(queue)

    # 1. Verify queue received human_guidance_injected
    events = []
    while not queue.empty():
        kind, payload = queue.get_nowait()
        if kind:
            events.append(kind)
    assert "human_guidance_injected" in events

    # 2. Verify debate and verdict prompts contained the guidance
    debate_prompts = [p for m, p in asked_prompts if "ROUND" in p or "DEBATE" in p]
    assert any("Strictly prioritize Redis cluster over Hazelcast." in p for p in debate_prompts)

    verdict_prompts = [p for m, p in asked_prompts if "You are the Chairman" in p]
    assert any("Strictly prioritize Redis cluster over Hazelcast." in p for p in verdict_prompts)
    assert any("https://redis.io" in p for p in verdict_prompts)

    # 3. Verify metadata recorded injected_guidance
    assert "injected_guidance" in result["metadata"]
    assert len(result["metadata"]["injected_guidance"]) == 1
    assert result["metadata"]["injected_guidance"][0]["message"] == "Strictly prioritize Redis cluster over Hazelcast."
