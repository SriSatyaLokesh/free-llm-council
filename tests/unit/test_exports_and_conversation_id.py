"""Tests for conversation ID exposure, markdown report export, and zip bundle packaging."""

import io
import json
import zipfile
import pytest
from backend import storage
from backend.main import app
from httpx import ASGITransport, AsyncClient


def test_format_conversation_markdown_structure():
    """Verify markdown generator produces structured sections."""
    sample_conv = {
        "id": "conv-test-1234",
        "created_at": "2026-10-06T12:00:00Z",
        "title": "Database Architecture Debate",
        "messages": [
            {
                "role": "user",
                "content": "Postgres vs CockroachDB for multi-region?",
            },
            {
                "role": "assistant",
                "council": {
                    "positions": [
                        {
                            "model": "model-a",
                            "response": "CockroachDB is purpose-built for multi-region active-active.",
                            "error": None,
                        },
                        {
                            "model": "model-b",
                            "response": "Postgres with read replicas is simpler if writes are centralized.",
                            "error": None,
                        },
                    ],
                    "debate": [
                        {
                            "round": 1,
                            "responses": [
                                {
                                    "model": "model-a",
                                    "response": "Centralized writes create cross-region latency spikes.",
                                }
                            ],
                        }
                    ],
                    "review": [
                        {
                            "model": "model-b",
                            "response": "Scored model-a: strong accuracy and grounded reasoning.",
                        }
                    ],
                    "verdict": {
                        "model": "model-chair",
                        "sections": {
                            "decision": "Use CockroachDB if strict active-active multi-region writes are required.",
                            "reasoning": "Postgres write replication latency across oceanic regions degrades p99.",
                            "tradeoffs": "Operational complexity and higher base infrastructure costs.",
                            "confidence": "High (4/5)",
                        },
                    },
                    "metadata": {
                        "members": ["model-a", "model-b"],
                        "chairman": "model-chair",
                        "caveman": "full",
                        "total_tokens": 4200,
                    },
                },
            },
        ],
    }

    md = storage.format_conversation_markdown(sample_conv)
    assert "# Database Architecture Debate" in md
    assert "conv-test-1234" in md
    assert "## Executive Verdict (Chairman Synthesis)" in md
    assert "### Decision" in md
    assert "CockroachDB is purpose-built" in md
    assert "## Stage 1: Opening Positions" in md
    assert "## Stage 2: Peer Debate" in md
    assert "## Stage 3: Blind Peer Review" in md
    assert "## Session Telemetry & Metadata" in md
    assert "4,200" in md

    # Detailed report verification
    detailed_md = storage.format_conversation_detailed(sample_conv)
    assert "Council Deliberation Deep-Dive & Comparative Matrix" in detailed_md
    assert "COUNCIL MULTI-AGENT DELIBERATION FLOW" in detailed_md
    assert "Comparative Model Deliberation Matrix" in detailed_md
    assert "| `model-a` |" in detailed_md
    assert "| `model-b` |" in detailed_md
    assert "Strategic Trade-Off & Risk Mitigation Matrix" in detailed_md
    assert "Presiding Chairman" in detailed_md


def test_export_conversation_zip_archive():
    """Verify in-memory zip archive packages executive-report.md, detailed-report.md, report.md, conversation.json, and summary.txt."""
    sample_conv = {
        "id": "conv-test-5678",
        "created_at": "2026-10-06T12:00:00Z",
        "title": "Cache Eviction Evaluation",
        "messages": [
            {
                "role": "user",
                "content": "W-TinyLFU vs 2Q cache?",
            },
            {
                "role": "assistant",
                "council": {
                    "verdict": {
                        "model": "chair-model",
                        "sections": {
                            "decision": "Adopt W-TinyLFU via Caffeine/Ristretto.",
                            "confidence": "Very High",
                        },
                    }
                },
            },
        ],
    }

    zip_bytes = storage.export_conversation_zip(sample_conv)
    assert isinstance(zip_bytes, bytes)
    assert len(zip_bytes) > 0

    with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zf:
        names = zf.namelist()
        assert "conversation.json" in names
        assert "report.md" in names
        assert "executive-report.md" in names
        assert "detailed-report.md" in names
        assert "summary.txt" in names

        # Validate JSON content
        raw = zf.read("conversation.json").decode("utf-8")
        parsed = json.loads(raw)
        assert parsed["id"] == "conv-test-5678"

        # Validate Markdown report content
        report_text = zf.read("report.md").decode("utf-8")
        assert "# Cache Eviction Evaluation" in report_text
        assert "Adopt W-TinyLFU" in report_text

        detailed_text = zf.read("detailed-report.md").decode("utf-8")
        assert "Council Deliberation Deep-Dive & Comparative Matrix" in detailed_text
        assert "Adopt W-TinyLFU" in detailed_text

        # Validate summary text
        summary_text = zf.read("summary.txt").decode("utf-8")
        assert "LLM COUNCIL DELIBERATION SUMMARY" in summary_text
        assert "conv-test-5678" in summary_text
        assert "Adopt W-TinyLFU" in summary_text


@pytest.mark.asyncio
async def test_export_endpoints_http():
    """Verify HTTP GET endpoints for report and zip downloads."""
    # Use existing or create a temporary conversation
    conv = storage.create_conversation("test-export-http-conv")
    storage.add_user_message("test-export-http-conv", "Test Query")
    storage.add_assistant_message(
        "test-export-http-conv",
        {
            "positions": [{"model": "m1", "response": "Pos 1"}],
            "verdict": {
                "model": "chair",
                "sections": {"decision": "Final decision"},
            },
        },
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Test markdown report export (default / executive)
        resp_md = await client.get("/api/conversations/test-export-http-conv/export/report")
        assert resp_md.status_code == 200
        assert "text/markdown" in resp_md.headers["content-type"]
        assert "Test Query" in resp_md.text
        assert "Final decision" in resp_md.text

        # 2. Test detailed markdown report export
        resp_detail = await client.get("/api/conversations/test-export-http-conv/export/report?format=detailed")
        assert resp_detail.status_code == 200
        assert "text/markdown" in resp_detail.headers["content-type"]
        assert "Council Deliberation Deep-Dive" in resp_detail.text
        assert "COUNCIL MULTI-AGENT DELIBERATION FLOW" in resp_detail.text
        assert "Comparative Model Deliberation Matrix" in resp_detail.text

        # 3. Test pre-rendered reports JSON endpoint
        resp_reports = await client.get("/api/conversations/test-export-http-conv/reports")
        assert resp_reports.status_code == 200
        data = resp_reports.json()
        assert "executive_report" in data
        assert "detailed_report" in data
        assert "Final decision" in data["executive_report"]
        assert "Comparative Model Deliberation Matrix" in data["detailed_report"]

        # 4. Test ZIP export
        resp_zip = await client.get("/api/conversations/test-export-http-conv/export/zip")
        assert resp_zip.status_code == 200
        assert "application/zip" in resp_zip.headers["content-type"]
        with zipfile.ZipFile(io.BytesIO(resp_zip.content), "r") as zf:
            assert "report.md" in zf.namelist()
            assert "executive-report.md" in zf.namelist()
            assert "detailed-report.md" in zf.namelist()
            assert "conversation.json" in zf.namelist()
            assert "summary.txt" in zf.namelist()

        # 5. Test 404 on non-existent conversation
        resp_404 = await client.get("/api/conversations/non-existent-id/export/zip")
        assert resp_404.status_code == 404

    # Cleanup
    storage.delete_conversation("test-export-http-conv")
