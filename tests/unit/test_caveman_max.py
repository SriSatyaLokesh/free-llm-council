"""
Real, non-mocked tests for Phase 5: Caveman Max Mode & Debate Compression.
Tests verify instruction generation, structured contract formatting,
negation preservation directives, and live settings API acceptance.
"""

import pytest
from httpx import AsyncClient, ASGITransport

from backend.main import app
from backend import caveman, settings


def test_caveman_levels_includes_max():
    """
    Ensure 'max' is recognized as a first-class debate compression level.
    """
    assert "max" in caveman.LEVELS, f"Expected 'max' in caveman.LEVELS: {caveman.LEVELS}"
    assert "max" in settings.DEBATE_MODES, f"Expected 'max' in settings.DEBATE_MODES: {settings.DEBATE_MODES}"


def test_build_instruction_max_structure_and_contract():
    """
    Verify that build_instruction('max') emits the ultra-dense claim-and-evidence contract.
    Must contain:
    - UPDATING / DEFENDING requirement
    - Structured fields: PEER:, REBUT:, EVIDENCE:
    - Strict negation protection rule (not, never, no, only, except)
    - Removal of pleasantries, articles, and filler
    """
    instruction = caveman.build_instruction("max")
    assert instruction is not None, "build_instruction('max') returned None"

    upper_inst = instruction.upper()
    assert "MAX" in upper_inst
    assert "UPDATING" in upper_inst and "DEFENDING" in upper_inst
    assert "PEER:" in upper_inst
    assert "REBUT:" in upper_inst
    assert "EVIDENCE:" in upper_inst

    # Negation preservation directive
    lower_inst = instruction.lower()
    for word in ("not", "never", "no", "only", "except"):
        assert word in lower_inst, f"Negation guard missing word: {word!r}"


def test_settings_module_accepts_max_mode():
    """
    Verify backend.settings accepts and returns 'max' debate mode.
    """
    settings.update_settings({"debateMode": "max"})
    assert settings.get_debate_mode() == "max"
    # Reset back to full for test hygiene
    settings.update_settings({"debateMode": "full"})


@pytest.mark.asyncio
async def test_settings_api_accepts_max_mode():
    """
    HTTP integration test: FastAPI POST /api/settings accepts debateMode='max'.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/api/settings", json={"debateMode": "max"})
        assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
        data = res.json()
        assert data.get("debateMode") == "max"

        # Verify persistence via GET
        res_get = await client.get("/api/settings")
        assert res_get.status_code == 200
        assert res_get.json().get("debateMode") == "max"

        # Clean up
        await client.post("/api/settings", json={"debateMode": "full"})


def test_prompts_integrate_max_contract():
    """
    Verify that debate_prompt embeds the Caveman max instruction cleanly.
    """
    from backend import prompts

    inst = caveman.build_instruction("max")
    prompt = prompts.debate_prompt(
        user_query="Which framework to pick?",
        your_model="agent-alpha",
        positions_text="[agent-alpha]\nUse FastHTML",
        prior_rounds_text="",
        round_number=1,
        total_rounds=2,
        caveman_instruction=inst,
    )
    assert "CAVEMAN MAX MODE ACTIVE" in prompt
    assert "PEER:" in prompt
    assert "REBUT:" in prompt
    assert "EVIDENCE:" in prompt
    assert "UPDATING" in prompt and "DEFENDING" in prompt


def test_chairman_prompt_contains_expansion_directive_for_max():
    """
    Verify that verdict_prompt alerts the chairman to expand compressed debate notes.
    """
    from backend import prompts

    prompt = prompts.verdict_prompt(
        user_query="Database choice?",
        positions_text="pos",
        debate_text="deb",
        review_text="rev",
        aggregate_text="agg",
        chairman_model="chief",
        debate_was_compressed=True,
        compression_modes="max",
    )
    assert "compressed mode (max)" in prompt
    assert "Expand: restore the full reasoning" in prompt


@pytest.mark.asyncio
async def test_council_run_records_max_caveman_mode():
    """
    Functional test: When debateMode is 'max', CouncilRun marks
    round_entry['cavemanLevel'] as 'max' and round_entry['compressed'] as True.
    """
    from unittest.mock import AsyncMock, MagicMock, patch
    from backend.council import CouncilRun

    settings.update_settings({"debateMode": "max"})
    try:
        models = ["agent-1", "agent-2"]
        mock_sessions = {}
        for m in models:
            s = MagicMock()
            s.model = m
            s.session_id = f"sess_{m}"
            s.create = AsyncMock(return_value=s)
            s.close = AsyncMock(return_value=None)
            s.set_permissions = AsyncMock(return_value=None)
            s.ask = AsyncMock(return_value={
                "text": "DEFENDING agent-1. PEER: agent-2. REBUT: point. EVIDENCE: fact.",
                "reasoning": "",
                "toolCalls": [],
                "tokens": {"input": 100, "output": 25, "reasoning": 0, "total": 125},
                "cost": 0,
                "finish": "stop",
                "model": m,
                "error": None,
            })
            mock_sessions[m] = s

        run = CouncilRun(
            user_query="FastHTML vs React?",
            members=models,
            chairman="agent-1",
            rounds=1,
        )

        with patch.object(run, "_make_session") as mock_make:
            async def fake_make(client, m, store):
                store[m] = mock_sessions[m]
                return m
            mock_make.side_effect = fake_make

            result = await run.run()

        assert len(result["debate"]) == 1
        round_1 = result["debate"][0]
        assert round_1["cavemanLevel"] == "max"
        assert round_1["compressed"] is True
        assert result["metadata"]["caveman"]["stages"]["debate"]["mode"] == "max"
    finally:
        settings.update_settings({"debateMode": "full"})
