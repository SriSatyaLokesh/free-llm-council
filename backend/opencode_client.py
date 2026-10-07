"""
Client for the local opencode server.

This module replaces the old OpenRouter client. The council does not talk to
any model provider directly - it asks the *local opencode server* to run models
that are already configured inside opencode. No third-party API keys required.

Why sessions instead of a simple completion call?
-------------------------------------------------
`POST /api/experimental/generate` is rejected by the free tier with
"OpenCode's free tier can only be used from within OpenCode". The session
endpoints go through the normal agent loop, which is what makes them work -
and as a bonus it gives every council member the full toolbelt (webfetch,
websearch, read, grep, glob).

Verified call sequence:
    POST /api/session                              {model, agent, permissions}
    POST /api/session/{id}/prompt                  {text}   -> returns immediately
    POST /api/experimental/session/{id}/wait       {}      -> blocks until idle
    GET  /api/session/{id}/message?type=assistant&order=asc
    DELETE /api/session/{id}
"""

import asyncio
import base64
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx

from .config import (
    OPENCODE_SERVER_PASSWORD,
    OPENCODE_SERVER_URL,
    OPENCODE_WORKSPACE,
    PER_MODEL_TIMEOUT,
)

# Actions the council members are allowed to use. Everything else is denied.
# These mirror the `council` agent defined in opencode.json - belt and braces.
#
# Note on action names: opencode has no separate "write"/"patch" action. All
# filesystem mutation goes through `edit`. `task` is denied so a member cannot
# spawn a subagent that would escape this sandbox.
DEFAULT_ALLOWED_ACTIONS = ("webfetch", "websearch", "read", "grep", "glob", "list")
DEFAULT_DENIED_ACTIONS = (
    "edit", "bash", "task", "lsp", "external_directory", "todowrite", "question",
)

# Additional research tools cut off for a compressed round, once the opening
# research is already in the transcript.
#
# "execute" matters: with only webfetch/websearch denied, models route around it
# and fetch pages through `execute` instead, so denying it is what actually
# stops the spending.
#
# DO NOT add "shell" here. It is not a real permission action, and a ruleset
# containing it makes opencode fail the entire session with outcome "failed" -
# even for a prompt that uses no tools at all. Verified by bisection against
# opencode 2.0.18.
RESEARCH_ACTIONS = ("webfetch", "websearch", "execute", "run", "sh")


class OpencodeUnavailable(RuntimeError):
    """Raised when the local opencode server cannot be reached."""


# --------------------------------------------------------------------------
# Server discovery
# --------------------------------------------------------------------------

def _service_config_candidates() -> List[Path]:
    """Possible locations of opencode's service.json."""
    candidates = [
        Path.home() / ".config" / "opencode" / "service.json",
    ]
    appdata = os.environ.get("APPDATA")
    if appdata:
        candidates.append(Path(appdata) / "opencode" / "service.json")
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        candidates.append(Path(xdg) / "opencode" / "service.json")
    return candidates


def get_server_password() -> str:
    """
    Resolve the opencode server password.

    Order: OPENCODE_SERVER_PASSWORD env var, then ~/.config/opencode/service.json
    """
    env_val = os.environ.get("OPENCODE_SERVER_PASSWORD") or OPENCODE_SERVER_PASSWORD
    if env_val:
        return env_val

    for path in _service_config_candidates():
        try:
            if path.exists():
                data = json.loads(path.read_text(encoding="utf-8"))
                password = data.get("password")
                if password:
                    return password
        except Exception:
            continue

    raise OpencodeUnavailable(
        "Could not find the opencode server password. Run `opencode service start` "
        "to create one, or set OPENCODE_SERVER_PASSWORD."
    )


def get_server_url() -> str:
    """
    Resolve the opencode server base URL.

    Order: OPENCODE_SERVER_URL env var, `opencode service status`,
    port from service.json, then the default 4096 port.
    """
    env_val = os.environ.get("OPENCODE_SERVER_URL") or OPENCODE_SERVER_URL
    if env_val:
        return env_val.rstrip("/")

    executable = shutil.which("opencode") or shutil.which("opencode.cmd")
    if executable:
        try:
            proc = subprocess.run(
                [executable, "service", "status"],
                capture_output=True,
                text=True,
                timeout=15,
            )
            output = (proc.stdout or "").strip()
            match = re.search(r"https?://[^\s\"']+", output)
            if match:
                return match.group(0).rstrip("/")
        except Exception:
            pass

    for path in _service_config_candidates():
        try:
            if path.exists():
                data = json.loads(path.read_text(encoding="utf-8"))
                port = data.get("port")
                if port:
                    return f"http://127.0.0.1:{port}"
        except Exception:
            continue

    return "http://127.0.0.1:4096"


def is_opencode_responding(url: Optional[str] = None) -> bool:
    """Check if the OpenCode server is currently responding."""
    target_url = (url or get_server_url()).rstrip("/")
    try:
        with httpx.Client(timeout=1.5) as client:
            resp = client.get(f"{target_url}/api/model")
            # 200 = healthy; 401 = up and demanding auth; both prove the server is listening
            return resp.status_code in (200, 401)
    except Exception:
        return False


def ensure_opencode_running(timeout: float = 12.0) -> bool:
    """
    Ensure the OpenCode service is running. If not running, automatically start it.

    Returns True if OpenCode is confirmed running and responding, False otherwise.
    """
    target_url = get_server_url()
    if is_opencode_responding(target_url):
        return True

    executable = shutil.which("opencode") or shutil.which("opencode.cmd")
    if not executable:
        return False

    import time
    try:
        # Step 1: Attempt standard `opencode service start`
        subprocess.run(
            [executable, "service", "start"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception:
        pass

    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(0.5)
        new_url = get_server_url()
        if is_opencode_responding(new_url):
            return True

    # Step 2: Fallback to running background server if service daemon didn't start
    try:
        kwargs: Dict[str, Any] = {}
        if os.name == "nt":
            kwargs["creationflags"] = 0x08000000 | 0x00000200  # CREATE_NO_WINDOW | DETACHED_PROCESS
        else:
            kwargs["start_new_session"] = True

        subprocess.Popen(
            [executable, "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            **kwargs,
        )

        fallback_deadline = time.time() + 5.0
        while time.time() < fallback_deadline:
            time.sleep(0.5)
            new_url = get_server_url()
            if is_opencode_responding(new_url):
                return True
    except Exception:
        pass

    return is_opencode_responding()



def _auth_headers() -> Dict[str, str]:
    password = get_server_password()
    token = base64.b64encode(f"opencode:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def _location_params() -> Dict[str, str]:
    """Every opencode call is scoped to the council's workspace directory."""
    return {"location[directory]": OPENCODE_WORKSPACE}


async def diagnose_connection(url: Optional[str] = None) -> Dict[str, Any]:
    """
    Actively inspect the connection to the OpenCode server and return a detailed diagnosis.

    Returns a dict with:
      - status: 'connected' | 'port_conflict' | 'unauthorized' | 'unreachable' | 'error'
      - message: human-readable explanation and actionable remediation
      - url: server URL tested
      - models_count: number of available models if connected
    """
    target_url = (url or get_server_url()).rstrip("/")
    port_match = re.search(r":(\d+)", target_url)
    target_port = int(port_match.group(1)) if port_match else 4096

    try:
        password = get_server_password()
        token = base64.b64encode(f"opencode:{password}".encode()).decode()
        headers = {"Authorization": f"Basic {token}"}
    except OpencodeUnavailable as exc:
        return {
            "status": "missing_credentials",
            "message": str(exc),
            "url": target_url,
            "port": target_port,
        }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                f"{target_url}/api/model",
                params=_location_params(),
                headers=headers,
            )

            if resp.status_code == 200:
                payload = resp.json()
                models = payload.get("data", []) if isinstance(payload, dict) else []
                return {
                    "status": "connected",
                    "url": target_url,
                    "port": target_port,
                    "models_count": len(models),
                    "message": f"Connected to OpenCode at {target_url} ({len(models)} models available)",
                }

            if resp.status_code == 401:
                server_hdr = resp.headers.get("server", "").lower()
                body_text = resp.text.lower()
                if "kilo" in server_hdr or "kilo" in body_text:
                    return {
                        "status": "port_conflict",
                        "url": target_url,
                        "port": target_port,
                        "message": (
                            f"Port conflict on {target_url}: port is occupied by Kilo, not OpenCode. "
                            f"Run OpenCode on another port (e.g. `opencode serve --port 4097`) "
                            f"and set OPENCODE_SERVER_URL=http://127.0.0.1:4097."
                        ),
                    }
                if "opencode" not in body_text and "opencode" not in str(resp.headers).lower():
                    return {
                        "status": "port_conflict",
                        "url": target_url,
                        "port": target_port,
                        "message": (
                            f"Port conflict on {target_url}: server rejected credentials and does not "
                            f"appear to be OpenCode. Another local service may be using this port."
                        ),
                    }
                return {
                    "status": "unauthorized",
                    "url": target_url,
                    "port": target_port,
                    "message": f"OpenCode server at {target_url} rejected credentials. Run `opencode service restart` or check service.json.",
                }

            if resp.status_code == 404:
                return {
                    "status": "port_conflict",
                    "url": target_url,
                    "port": target_port,
                    "message": f"Server at {target_url} returned 404 for /api/model. It may be a different local service. Expected OpenCode daemon.",
                }

            return {
                "status": "degraded",
                "url": target_url,
                "port": target_port,
                "message": f"Server returned unexpected status HTTP {resp.status_code}",
            }

    except httpx.ConnectError:
        return {
            "status": "unreachable",
            "url": target_url,
            "port": target_port,
            "message": f"No server listening at {target_url}. Run `opencode service start` or `opencode serve --port 4096`.",
        }
    except Exception as exc:
        return {
            "status": "error",
            "url": target_url,
            "port": target_port,
            "message": f"Error connecting to OpenCode at {target_url}: {exc}",
        }



# --------------------------------------------------------------------------
# Model roster
# --------------------------------------------------------------------------

async def list_models() -> List[Dict[str, Any]]:
    """
    Fetch the models available inside opencode.

    This is the council roster - whatever opencode has configured, with no
    hardcoded list to maintain.
    """
    url = f"{get_server_url()}/api/model"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                url,
                params=_location_params(),
                headers=_auth_headers(),
            )
    except httpx.ConnectError:
        # Auto-heal: start opencode service if not yet running and retry
        if ensure_opencode_running(timeout=8.0):
            url = f"{get_server_url()}/api/model"
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    url,
                    params=_location_params(),
                    headers=_auth_headers(),
                )
        else:
            raise OpencodeUnavailable(
                f"No opencode server found at {get_server_url()}. Check that opencode is installed."
            )

    if response.status_code == 401:
        raise OpencodeUnavailable(
            "opencode server rejected our credentials. Try `opencode service restart`."
        )
    if response.status_code == 404:
        raise OpencodeUnavailable(
            f"No opencode server found at {get_server_url()}. Run `opencode service start`."
        )
    response.raise_for_status()

    payload = response.json()

    models = []
    seen_ids = set()
    for entry in payload.get("data", []):
        model_id = entry.get("id") or entry.get("modelID")
        provider_id = entry.get("providerID")
        if not model_id or not provider_id:
            continue

        full_id = f"{provider_id}/{model_id}"
        if full_id in seen_ids:
            continue
        seen_ids.add(full_id)

        capabilities = entry.get("capabilities") or {}
        limits = entry.get("limit") or {}
        cost = entry.get("cost") or [{}]
        variants = entry.get("variants") or []

        models.append({
            "id": full_id,
            "providerID": provider_id,
            "modelID": model_id,
            "name": entry.get("name") or model_id,
            "family": entry.get("family"),
            "context": limits.get("context"),
            "output": limits.get("output"),
            "supportsTools": bool(capabilities.get("tools")),
            "supportsVision": "image" in (capabilities.get("input") or []),
            "variants": variants,
            "free": not any(
                (cost[0].get(k) or 0) for k in ("input", "output")
            ) if cost else False,
        })

    models.sort(key=lambda m: m["id"])
    return models


async def default_chairman(models: Optional[List[Dict[str, Any]]] = None) -> Optional[str]:
    """Pick the chairman automatically using the intelligent capability matrix."""
    if models is None:
        models = await list_models()
    if not models:
        return None
    from .capability_matrix import select_best_chairman
    return select_best_chairman(models)


# --------------------------------------------------------------------------
# Permissions
# --------------------------------------------------------------------------

def council_permissions(
    allow_research: bool = True,
) -> List[Dict[str, str]]:
    """
    Build the permission ruleset for council members.

    Allow the research and read tools, explicitly deny everything that could
    modify the workspace. The council must never be able to write to the user's
    files.

    With `allow_research=False` the web tools are denied too. That is used for
    compressed debate rounds, where the members already researched in the
    opening round and re-searching only burns tokens.
    """
    allowed = DEFAULT_ALLOWED_ACTIONS
    if not allow_research:
        allowed = tuple(a for a in DEFAULT_ALLOWED_ACTIONS if a not in RESEARCH_ACTIONS)

    rules = [{"action": action, "resource": "*", "effect": "allow"} for action in allowed]
    rules += [{"action": action, "resource": "*", "effect": "deny"} for action in DEFAULT_DENIED_ACTIONS]

    if not allow_research:
        rules += [
            {"action": action, "resource": "*", "effect": "deny"}
            for action in RESEARCH_ACTIONS
        ]

    return rules


# --------------------------------------------------------------------------
# Session
# --------------------------------------------------------------------------

def _parse_assistant_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """Flatten an opencode assistant message into text / reasoning / tool calls."""
    text_parts: List[str] = []
    reasoning_parts: List[str] = []
    tool_calls: List[Dict[str, Any]] = []

    for block in message.get("content") or []:
        kind = block.get("type")

        if kind == "text":
            text_parts.append(block.get("text") or "")
        elif kind == "reasoning":
            reasoning_parts.append(block.get("text") or "")
        elif kind == "tool":
            state = block.get("state") or {}
            tool_input = state.get("input")
            output_parts = []
            for part in state.get("content") or []:
                if isinstance(part, dict) and part.get("text"):
                    output_parts.append(part["text"])
            tool_calls.append({
                "name": block.get("name"),
                "status": state.get("status"),
                "input": tool_input,
                "url": (tool_input or {}).get("url")
                if isinstance(tool_input, dict) else None,
                "output": "\n".join(output_parts),
                "error": state.get("error"),
            })

    model_info = message.get("model") or {}
    return {
        "text": "\n\n".join(part for part in text_parts if part.strip()),
        "reasoning": "\n\n".join(part for part in reasoning_parts if part.strip()),
        "toolCalls": tool_calls,
        "finish": message.get("finish"),
        "cost": message.get("cost", 0),
        "tokens": message.get("tokens") or {},
        "model": model_info.get("id"),
    }


class CouncilSession:
    """
    One opencode session driven by one council member.

    The session is reused across debate rounds so the model keeps its own
    reasoning history instead of re-paying context cost every round.
    """

    def __init__(
        self,
        model: str,
        client: httpx.AsyncClient,
        agent: Optional[str] = None,
        variant: Optional[str] = None,
    ):
        self.model = model
        self.agent = agent
        self.variant = variant
        self._client = client
        self._base = get_server_url()
        self._headers = _auth_headers()
        self.session_id: Optional[str] = None
        self._message_cursor = 0
        self._denied_tools: List[str] = []

    def _url(self, path: str) -> str:
        return f"{self._base}{path}"

    def _params(self) -> Dict[str, str]:
        return _location_params()

    # -- lifecycle ---------------------------------------------------------

    async def create(self) -> "CouncilSession":
        """Create the underlying opencode session."""
        provider_id, model_id = self.model.split("/", 1)

        model_payload: Dict[str, Any] = {"providerID": provider_id, "id": model_id}
        if self.variant:
            model_payload["variant"] = self.variant

        body: Dict[str, Any] = {
            "title": f"council: {self.model}",
            "model": model_payload,
            "permissions": council_permissions(),
            # The location must be passed in the BODY. The
            # ?location[directory]= query parameter is accepted but ignored
            # for session creation, which silently leaves the session scoped
            # to whatever directory the server was started in - meaning the
            # council could not read the project it is being consulted about.
            "location": {"directory": OPENCODE_WORKSPACE},
        }
        if self.agent:
            body["agent"] = self.agent

        response = await self._client.post(
            self._url("/api/session"),
            json=body,
            params=self._params(),
            headers=self._headers,
        )

        if response.status_code == 404:
            raise RuntimeError(f"Model not available in opencode: {self.model}")
        if response.status_code == 401:
            raise RuntimeError("opencode server rejected the council's credentials")
        response.raise_for_status()

        self.session_id = response.json()["data"]["id"]
        return self

    async def close(self) -> None:
        """Delete the opencode session so it does not clutter the user's list."""
        if not self.session_id:
            return
        try:
            await self._client.delete(
                self._url(f"/api/session/{self.session_id}"),
                params=self._params(),
                headers=self._headers,
            )
        except Exception:
            pass
        finally:
            self.session_id = None

    async def __aenter__(self) -> "CouncilSession":
        return await self.create()

    async def __aexit__(self, *exc) -> None:
        await self.close()

    # -- permissions -------------------------------------------------------

    async def set_permissions(self, rules: List[Dict[str, str]]) -> None:
        """
        Replace this session's permission ruleset mid-run.

        Used to tighten the sandbox between stages - e.g. cutting off web
        research once the opening round is done, so the debate costs output
        tokens only instead of re-running searches every round.

        An unknown action name makes opencode fail the whole session, so
        callers should pass names that came from the real schema.
        """
        if not self.session_id:
            return
        await self._client.patch(
            self._url(f"/api/session/{self.session_id}"),
            json={"permissions": rules},
            params=self._params(),
            headers=self._headers,
        )

    # -- asking ------------------------------------------------------------

    async def ask(self, prompt: str, timeout: Optional[float] = None) -> Dict[str, Any]:
        """
        Send a prompt and wait for the agent loop to finish.

        Returns {text, reasoning, toolCalls, finish, cost, tokens, model}.
        """
        if not self.session_id:
            raise RuntimeError("Session not created - call create() first")

        timeout = timeout or PER_MODEL_TIMEOUT

        prompt_response = await self._client.post(
            self._url(f"/api/session/{self.session_id}/prompt"),
            json={"text": prompt},
            params=self._params(),
            headers=self._headers,
        )
        prompt_response.raise_for_status()

        watchdog = asyncio.create_task(self._deny_pending_permissions())
        try:
            await asyncio.wait_for(
                self._client.post(
                    self._url(f"/api/experimental/session/{self.session_id}/wait"),
                    json={},
                    params=self._params(),
                    headers=self._headers,
                ),
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            await self._interrupt()
            return {
                "text": "",
                "reasoning": "",
                "toolCalls": [],
                "finish": "timeout",
                "cost": 0,
                "tokens": {},
                "model": self.model,
                "error": f"Timed out after {int(timeout)}s",
            }
        finally:
            watchdog.cancel()

        return await self._collect_new_messages()

    async def _session_outcome(self) -> Dict[str, Any]:
        """
        Read the session's own outcome flag.

        opencode reports a failed agent loop as outcome "failed" with zero
        tokens and no assistant messages at all. Without this check a failed
        call is indistinguishable from a model that chose to say nothing.
        """
        try:
            response = await self._client.get(
                self._url(f"/api/session/{self.session_id}"),
                params=self._params(),
                headers=self._headers,
            )
            if response.status_code == 200:
                return response.json().get("data") or {}
        except Exception:
            pass
        return {}

    async def _interrupt(self) -> None:
        """Stop a runaway agent loop so the session does not keep burning tokens."""
        if not self.session_id:
            return
        try:
            await self._client.post(
                self._url(f"/api/session/{self.session_id}/interrupt"),
                json={},
                params=self._params(),
                headers=self._headers,
            )
        except Exception:
            pass

    async def _collect_new_messages(self) -> Dict[str, Any]:
        """Read the assistant messages produced since the last prompt."""
        response = await self._client.get(
            self._url(f"/api/session/{self.session_id}/message"),
            params={**self._params(), "type": "assistant", "order": "asc"},
            headers=self._headers,
        )
        response.raise_for_status()

        messages = response.json().get("data") or []
        new_messages = messages[self._message_cursor:]
        self._message_cursor = len(messages)

        texts, reasoning, tool_calls = [], [], []
        t_input = t_output = t_reasoning = 0
        cost = 0.0
        finish = "stop"
        last_context = 0

        for message in new_messages:
            parsed = _parse_assistant_message(message)
            if parsed["text"]:
                texts.append(parsed["text"])
            if parsed["reasoning"]:
                reasoning.append(parsed["reasoning"])
            tool_calls.extend(parsed["toolCalls"])

            # Accumulate across every message this prompt produced. A run that
            # used tools emits several assistant messages, and each one is a
            # real billed call - keeping only the last would understate the cost
            # of exactly the uncompressed runs we are comparing against.
            tokens = parsed["tokens"] or {}
            t_input += tokens.get("input", 0) or 0
            t_output += tokens.get("output", 0) or 0
            t_reasoning += tokens.get("reasoning", 0) or 0
            last_context = tokens.get("input", 0) or last_context
            cost += parsed["cost"] or 0.0

            if parsed["finish"] and parsed["finish"] != "stop":
                finish = parsed["finish"]

        text = "\n\n".join(texts)

        # A failed agent loop produces no messages and no tokens. Report it
        # rather than returning an empty answer that looks like a real one.
        error = None
        if not text:
            outcome = (await self._session_outcome()).get("outcome")
            if outcome and outcome != "success":
                error = (
                    f"opencode reported this session as '{outcome}'. "
                    f"The model may have been rate limited, or the agent "
                    f"'{self.agent or 'default'}' may not be usable."
                )
            elif not tool_calls:
                error = f"{self.model} returned no response."

        return {
            "text": text,
            "reasoning": "\n\n".join(reasoning),
            "toolCalls": tool_calls,
            "finish": finish,
            "cost": cost,
            "tokens": {
                "input": t_input,
                "output": t_output,
                "reasoning": t_reasoning,
                "total": t_input + t_output + t_reasoning,
                "contextAtEnd": last_context,
                "messages": len(new_messages),
            },
            "model": self.model,
            "error": error,
        }

    # -- safety ------------------------------------------------------------

    async def _deny_pending_permissions(self) -> None:
        """
        Watchdog: auto-reject any permission request raised for this session.

        Our ruleset already denies writes, but if opencode asks about an action
        name we did not anticipate, a human is not watching. Rejecting keeps a
        council run from hanging forever on an unanswered prompt.
        """
        try:
            while True:
                await asyncio.sleep(1.0)
                if not self.session_id:
                    return

                response = await self._client.get(
                    self._url("/api/permission/request"),
                    params=self._params(),
                    headers=self._headers,
                )
                if response.status_code != 200:
                    continue

                payload = response.json()
                requests = payload.get("data", payload) if isinstance(payload, dict) else payload

                for request in requests or []:
                    if request.get("sessionID") != self.session_id:
                        continue
                    request_id = request.get("id")
                    action = request.get("action")
                    if action:
                        self._denied_tools.append(action)
                    try:
                        await self._client.post(
                            self._url(
                                f"/api/session/{self.session_id}"
                                f"/permission/{request_id}/reply"
                            ),
                            json={"reply": "reject"},
                            params=self._params(),
                            headers=self._headers,
                        )
                    except Exception:
                        pass
        except asyncio.CancelledError:
            raise
        except Exception:
            return


# --------------------------------------------------------------------------
# Fan-out helpers
# --------------------------------------------------------------------------

async def opencode_request(
    method: str,
    path: str,
    json_body: Optional[Dict[str, Any]] = None,
    timeout: float = 30.0,
) -> Any:
    """
    Low-level authenticated call against the opencode server.

    Every opencode endpoint wraps its payload in {"data": ...}; that envelope is
    unwrapped here so callers get the useful value directly.
    """
    url = f"{get_server_url()}{path}"
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.request(
            method,
            url,
            json=json_body,
            params=_location_params(),
            headers=_auth_headers(),
        )
        response.raise_for_status()
        if response.status_code == 204 or not response.content:
            return None
        payload = response.json()
        if isinstance(payload, dict) and "data" in payload:
            return payload["data"]
        return payload


async def ask_many(
    models: List[str],
    prompt: str,
    agent: Optional[str] = None,
    sessions: Optional[Dict[str, CouncilSession]] = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Run one prompt across many models in parallel.

    If `sessions` is given, those existing sessions are reused (so the model
    keeps its own history). Otherwise a fresh session is created and closed.

    A model that fails is simply absent from the returned dict - it never fails
    the whole run.
    """
    owned: List[CouncilSession] = []
    active: Dict[str, CouncilSession] = dict(sessions or {})

    async with httpx.AsyncClient(timeout=PER_MODEL_TIMEOUT) as client:
        if sessions is None:
            # No sessions supplied: create throwaway ones for this single prompt.
            for model in models:
                if model not in active:
                    session = CouncilSession(model, client, agent=agent)
                    active[model] = session
                    owned.append(session)

        # Create any not-yet-started sessions first, in parallel.
        to_create = [s for s in active.values() if not s.session_id]
        if to_create:
            await asyncio.gather(*(s.create() for s in to_create), return_exceptions=True)

        async def run(model: str) -> Optional[Dict[str, Any]]:
            session = active.get(model)
            if not session or not session.session_id:
                return None
            try:
                return await session.ask(prompt)
            except Exception as exc:
                print(f"[council] model {model} failed: {exc}")
                return {
                    "text": "", "reasoning": "", "toolCalls": [], "error": str(exc),
                    "finish": "error", "cost": 0, "tokens": {}, "model": model,
                }

        try:
            results = await asyncio.gather(*(run(m) for m in models))
        finally:
            await asyncio.gather(*(s.close() for s in owned), return_exceptions=True)

    return {
        model: result
        for model, result in zip(models, results)
        if result is not None
    }
