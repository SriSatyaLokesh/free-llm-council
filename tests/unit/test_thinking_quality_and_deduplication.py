"""Unit tests for Phase 8: Per-Model Thinking Quality & Model Deduplication."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from backend.opencode_client import CouncilSession, list_models
from backend.council import CouncilRun


def test_model_formatting_preserves_distinct_variants():
    """Verify distinct models like ling 3.1 and ling 3.0 fin are not collapsed to the same name."""
    # Simulation of format.js shortModel logic in Python to test the contract
    import re

    def short_model(model_id: str) -> str:
        name = model_id.split("/")[-1]
        name = re.sub(r"-free$", "", name)
        # Old broken regex was: re.sub(r"-\d+(\.\d+)?-.*$", "", name) -> collapsed both to 'ling'
        # Fixed regex: remove common filler words like '-contributor' or '-preview' without stripping version or flavor
        name = re.sub(r"-(preview|contributor)", "", name)
        return name

    m1 = short_model("opencode/ling-3.1-flash-free")
    m2 = short_model("opencode/ling-3.0-flash-fin-free")
    assert m1 != m2, f"Models {m1} and {m2} must not be collapsed to the same string"
    assert "3.1" in m1
    assert "3.0" in m2

    n1 = short_model("opencode/nemotron-3.5-lightning-free")
    n2 = short_model("opencode/nemotron-3-ultra-free")
    assert n1 != n2
    assert "3.5" in n1
    assert "3" in n2


@pytest.mark.asyncio
async def test_list_models_extracts_variants_and_deduplicates():
    """Verify list_models includes variants list and deduplicates identical IDs."""
    sample_data = [
        {
            "id": "space-bunny-free",
            "providerID": "opencode",
            "name": "Space Bunny Free",
            "variants": [
                {"id": "low", "settings": {"reasoningEffort": "low"}},
                {"id": "medium", "settings": {"reasoningEffort": "medium"}},
                {"id": "high", "settings": {"reasoningEffort": "high"}},
                {"id": "max", "settings": {"reasoningEffort": "max"}},
            ],
            "limit": {"context": 128000},
            "capabilities": {"tools": True},
        },
        # Duplicate entry
        {
            "id": "space-bunny-free",
            "providerID": "opencode",
            "name": "Space Bunny Free",
            "variants": [],
            "limit": {"context": 128000},
            "capabilities": {"tools": True},
        },
        {
            "id": "big-pickle",
            "providerID": "opencode",
            "name": "Big Pickle",
            "variants": [],
            "limit": {"context": 32000},
            "capabilities": {},
        },
    ]

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"data": sample_data}

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_resp
        models = await list_models()

    # Deduplicated: 2 unique models, not 3
    assert len(models) == 2
    bunny = next(m for m in models if m["id"] == "opencode/space-bunny-free")
    assert "variants" in bunny
    assert len(bunny["variants"]) == 4
    variant_ids = [v["id"] for v in bunny["variants"]]
    assert "max" in variant_ids
    assert "medium" in variant_ids


@pytest.mark.asyncio
async def test_council_session_transmits_variant_in_payload():
    """Verify CouncilSession includes variant in the model specification object."""
    mock_client = AsyncMock()
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"data": {"id": "ses_test_123"}}
    mock_client.post.return_value = mock_resp

    session = CouncilSession("opencode/space-bunny-free", mock_client, variant="max")
    await session.create()

    # Verify post payload
    call_args = mock_client.post.call_args
    assert call_args is not None
    json_body = call_args[1].get("json", {})
    assert "model" in json_body
    model_obj = json_body["model"]
    assert model_obj["id"] == "space-bunny-free"
    assert model_obj["providerID"] == "opencode"
    assert model_obj.get("variant") == "max"


@pytest.mark.asyncio
async def test_council_run_defaults_chairman_to_max_thinking():
    """Verify CouncilRun defaults the Chairman to max thinking and regular members to medium/high."""
    available_variants = {
        "opencode/space-bunny-free": ["low", "medium", "high", "max"],
        "opencode/fledge-alpha-free": ["low", "high", "max"],
        "opencode/big-pickle": [],
    }

    run = CouncilRun(
        user_query="Design a distributed cache system.",
        members=["opencode/space-bunny-free", "opencode/fledge-alpha-free", "opencode/big-pickle"],
        chairman="opencode/space-bunny-free",
        rounds=1,
    )

    resolved_thinking = run.resolve_thinking_config(available_variants)

    # Chairman must be max
    assert resolved_thinking["opencode/space-bunny-free"] == "max"
    # Member with medium/high variants defaults to medium or high
    assert resolved_thinking["opencode/fledge-alpha-free"] in ("medium", "high")
    # Member with no variants has None
    assert resolved_thinking.get("opencode/big-pickle") is None


@pytest.mark.asyncio
async def test_council_run_honors_user_thinking_overrides():
    """Verify user overrides for thinking quality are honored over defaults."""
    available_variants = {
        "opencode/space-bunny-free": ["low", "medium", "high", "max"],
    }

    user_overrides = {
        "opencode/space-bunny-free": "low",
    }

    run = CouncilRun(
        user_query="Design a distributed cache system.",
        members=["opencode/space-bunny-free"],
        chairman="opencode/space-bunny-free",
        model_thinking=user_overrides,
    )

    resolved_thinking = run.resolve_thinking_config(available_variants)
    assert resolved_thinking["opencode/space-bunny-free"] == "low"
