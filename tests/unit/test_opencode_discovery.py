"""
Unit tests for OpenCode discovery, port resilience, and health diagnostics.
"""

import json
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import httpx

from backend import opencode_client as oc
from backend.main import app
from httpx import AsyncClient, ASGITransport


def test_get_server_url_env_override(monkeypatch):
    """OPENCODE_SERVER_URL env var should override all detection."""
    monkeypatch.setenv("OPENCODE_SERVER_URL", "http://localhost:9999/")
    monkeypatch.setattr(oc, "OPENCODE_SERVER_URL", "http://localhost:9999/")
    assert oc.get_server_url() == "http://localhost:9999"


def test_get_server_url_parses_dynamic_port(monkeypatch):
    """Dynamic port from 'opencode service status' should be extracted cleanly."""
    monkeypatch.delenv("OPENCODE_SERVER_URL", raising=False)
    monkeypatch.setattr(oc, "OPENCODE_SERVER_URL", None)

    mock_run = MagicMock()
    mock_run.return_value.stdout = "OpenCode service is running at http://127.0.0.1:49374\n"

    with patch("shutil.which", return_value="opencode"), patch("subprocess.run", mock_run):
        url = oc.get_server_url()
        assert url == "http://127.0.0.1:49374"


def test_get_server_password_resolution(tmp_path, monkeypatch):
    """Password should be resolved from service.json candidate directories."""
    monkeypatch.delenv("OPENCODE_SERVER_PASSWORD", raising=False)
    monkeypatch.setattr(oc, "OPENCODE_SERVER_PASSWORD", None)

    fake_config = tmp_path / "service.json"
    fake_config.write_text(json.dumps({"password": "test-secret-token"}), encoding="utf-8")

    with patch.object(oc, "_service_config_candidates", return_value=[fake_config]):
        pwd = oc.get_server_password()
        assert pwd == "test-secret-token"


def test_get_server_password_missing_raises_actionable_error(monkeypatch):
    """When no service.json exists, an informative OpencodeUnavailable error is raised."""
    monkeypatch.delenv("OPENCODE_SERVER_PASSWORD", raising=False)
    monkeypatch.setattr(oc, "OPENCODE_SERVER_PASSWORD", None)

    with patch.object(oc, "_service_config_candidates", return_value=[Path("/nonexistent/service.json")]):
        with pytest.raises(oc.OpencodeUnavailable) as exc_info:
            oc.get_server_password()
        assert "opencode service start" in str(exc_info.value)


@pytest.mark.asyncio
async def test_diagnose_connection_detects_port_conflict():
    """
    If a port is open but occupied by another process (e.g. Kilo on 4096),
    diagnose_connection() should report 'port_conflict' with the conflicting details.
    """
    # This function check_connection_health() / diagnose_connection() is new
    assert hasattr(oc, "diagnose_connection"), "oc must provide diagnose_connection()"

    mock_transport = ASGITransport(app=MagicMock())  # dummy
    # Simulating a non-opencode response (e.g. Kilo returning 401 without opencode token header)
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_resp.text = "Unauthorized - Kilo Daemon"
        mock_resp.headers = {"server": "kilo"}
        mock_get.return_value = mock_resp

        diagnosis = await oc.diagnose_connection("http://127.0.0.1:4096")
        assert diagnosis["status"] in ("port_conflict", "unauthorized_foreign")
        assert "4096" in diagnosis["message"]


@pytest.mark.asyncio
async def test_health_endpoint_returns_diagnostics():
    """
    FastAPI /api/health endpoint should report OpenCode connection and diagnostics.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/health")
        assert response.status_code in (200, 503)
        data = response.json()
        assert "status" in data
        assert "opencode" in data


def test_ensure_opencode_running_when_already_responding():
    """If opencode is already responding, ensure_opencode_running returns True immediately."""
    with patch.object(oc, "is_opencode_responding", return_value=True):
        assert oc.ensure_opencode_running(timeout=1.0) is True


def test_ensure_opencode_running_triggers_service_start():
    """If opencode is not responding, ensure_opencode_running runs opencode service start."""
    with patch.object(oc, "is_opencode_responding", side_effect=[False, True]), \
         patch("shutil.which", return_value="opencode"), \
         patch("subprocess.run") as mock_run:
        result = oc.ensure_opencode_running(timeout=2.0)
        assert result is True
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "service" in args and "start" in args

