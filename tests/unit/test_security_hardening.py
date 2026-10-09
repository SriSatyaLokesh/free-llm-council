"""Security hardening regression tests for path traversal, stored XSS, and subprocess sandboxing."""

import os
import pytest
from unittest.mock import patch, MagicMock
from httpx import ASGITransport, AsyncClient

from backend import storage
from backend.main import app


def test_validate_safe_id_accepts_valid_ids():
    """Verify that safe identifiers (alphanumeric, hyphens, underscores) are accepted."""
    assert storage.validate_safe_id("conv-1234-abcd_EFGH") == "conv-1234-abcd_EFGH"
    assert storage.validate_safe_id("550e8400-e29b-41d4-a716-446655440000") == "550e8400-e29b-41d4-a716-446655440000"
    assert storage.validate_safe_id("project_alpha") == "project_alpha"


def test_validate_safe_id_rejects_traversal_and_forbidden_chars():
    """Verify that relative traversal sequences and special characters are rejected."""
    bad_ids = [
        "../projects",
        "..\\projects",
        "../../etc/passwd",
        "/absolute/path",
        "conv;rm -rf",
        "conv<script>",
        "conv*id",
        "",
        " ",
        "conv id",
    ]
    for bad in bad_ids:
        with pytest.raises(ValueError, match="Invalid"):
            storage.validate_safe_id(bad)


def test_get_conversation_path_prevents_traversal():
    """Verify get_conversation_path rejects any path attempting to escape DATA_DIR."""
    with pytest.raises(ValueError):
        storage.get_conversation_path("../projects")

    with pytest.raises(ValueError):
        storage.get_conversation_path("../../config")

    # Valid ID resolves properly inside DATA_DIR
    valid_path = storage.get_conversation_path("valid-conv-123")
    assert valid_path.endswith(os.path.join("data", "conversations", "valid-conv-123.json")) or \
           valid_path.endswith(os.path.normpath("data/conversations/valid-conv-123.json"))


def test_delete_conversation_rejects_traversal_gracefully(tmp_path):
    """Verify delete_conversation with traversal returns False without throwing or deleting files."""
    # Create a dummy canary file that should never be deleted
    canary = tmp_path / "canary.json"
    canary.write_text('{"canary": true}', encoding="utf-8")

    assert storage.delete_conversation("../canary") is False
    assert storage.delete_conversation("../../canary") is False
    assert canary.exists()


def test_render_report_html_escapes_xss_in_title_and_metadata():
    """Verify render_report_html escapes HTML in conversation titles, metadata, and markdown body."""
    conv = {
        "id": "conv-test-xss",
        "created_at": "2026-10-09T07:00:00Z",
        "title": "</title><script id='xss'>alert('title')</script>",
        "messages": [
            {
                "role": "user",
                "content": "What is security? <img src=x onerror=alert('msg')>",
            },
            {
                "role": "assistant",
                "council": {
                    "positions": [],
                    "debate": [],
                    "review": [],
                    "verdict": {
                        "model": "model<script>alert('model')</script>",
                        "sections": {
                            "confidence": "high<script>alert('conf')</script>",
                        },
                    },
                    "metadata": {
                        "total_tokens": 1234,
                    },
                },
            },
        ],
    }

    html_out = storage.render_report_html(conv)

    # Raw script or img onerror tags must never appear unescaped in HTML
    assert "<script id='xss'>" not in html_out
    assert "<script>" not in html_out
    assert "<img src=x onerror" not in html_out

    # Must be entity-encoded
    assert "&lt;/title&gt;&lt;script id=&#x27;xss&#x27;&gt;alert(&#x27;title&#x27;)&lt;/script&gt;" in html_out or \
           "&lt;script" in html_out


@pytest.mark.asyncio
async def test_api_conversation_endpoints_reject_path_traversal():
    """Verify FastAPI conversation endpoints safely handle path traversal sequences with 404/400."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # GET with traversal ID
        res_get = await ac.get("/api/conversations/..%2Fprojects")
        assert res_get.status_code in (400, 404)

        # DELETE with traversal ID
        res_del = await ac.delete("/api/conversations/..%2Fprojects")
        assert res_del.status_code in (400, 404)


def test_generate_report_pdf_includes_sandboxing_flags():
    """Verify generate_report_pdf includes --disable-javascript and --disable-local-file-access."""
    conv = {
        "id": "conv-test-flags",
        "title": "Test Deliberation",
        "messages": [],
    }

    with patch("backend.storage.find_headless_browser", return_value="dummy-chrome"), \
         patch("subprocess.run") as mock_run:
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_run.return_value = mock_proc

        storage.generate_report_pdf(conv)

        assert mock_run.called
        cmd_args = mock_run.call_args[0][0]
        assert "--disable-javascript" in cmd_args
        assert "--disable-local-file-access" in cmd_args
        assert "--headless=new" in cmd_args
