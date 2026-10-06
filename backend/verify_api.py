"""
End-to-end test of the HTTP API, including the SSE streaming path.

Creates a conversation, sends a message with a small council, and prints every
streamed event. Leaves the conversation on disk so the UI can be opened onto it.

    python -m backend.verify_api
"""

import asyncio
import json
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend import opencode_client as oc  # noqa: E402

API = "http://localhost:8001"
QUESTION = (
    "Our startup has 3 engineers and 8 months of runway. Should we build with "
    "Postgres or SQLite for the MVP? Be decisive, and name the one tradeoff that "
    "would make you change your mind."
)


def post(path, body):
    req = urllib.request.Request(
        f"{API}{path}",
        data=json.dumps(body).encode(),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    return json.load(urllib.request.urlopen(req, timeout=60))


async def council_sessions():
    """Council sessions currently left in the user's opencode session list."""
    import httpx

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.get(
            f"{oc.get_server_url()}/api/session",
            params=oc._location_params(),
            headers=oc._auth_headers(),
        )
    return [
        s for s in (response.json().get("data") or [])
        if str(s.get("title", "")).startswith("council:")
    ]


def main() -> int:
    t0 = time.time()
    stray_before = asyncio.run(council_sessions())

    print("creating conversation...")
    conv = post("/api/conversations", {})
    cid = conv["id"]
    print(f"  {cid}")

    body = {
        "content": QUESTION,
        "members": ["opencode/big-pickle", "opencode/mimo-v2.6-flash-free"],
        "chairman": "opencode/big-pickle",
        "rounds": 1,
    }

    req = urllib.request.Request(
        f"{API}/api/conversations/{cid}/message/stream",
        data=json.dumps(body).encode(),
        method="POST",
        headers={"Content-Type": "application/json"},
    )

    print(f"streaming from {req.full_url}\n" + "-" * 62)
    seen = []
    with urllib.request.urlopen(req, timeout=1800) as resp:
        buf = ""
        for raw in resp:
            buf += raw.decode("utf-8", "replace")
            while "\n\n" in buf:
                frame, buf = buf.split("\n\n", 1)
                for line in frame.split("\n"):
                    if not line.startswith("data:"):
                        continue
                    event = json.loads(line[5:].strip())
                    kind = event.get("type")
                    seen.append(kind)
                    print(f"[{time.time() - t0:6.1f}s] {kind}")

                    if kind == "roster":
                        print(f"            members={event['data']['members']}")
                    elif kind == "positions_complete":
                        for p in event["data"]:
                            tools = [c["name"] for c in p.get("toolCalls") or []]
                            print(f"            {p['model']}: tools={tools} err={p.get('error')}")
                    elif kind == "debate_round_complete":
                        for s in event["data"]["statements"]:
                            print(f"            R{event['data']['round']} {s['model']}: "
                                  f"{len(s.get('response') or '')} chars")
                    elif kind == "review_complete":
                        for r in event["data"]:
                            print(f"            {r['model']}: parsed={r['parsed_ranking']}")
                    elif kind == "aggregate_complete":
                        print(f"            {event['data']}")
                    elif kind == "verdict_complete":
                        sections = event["data"].get("sections") or {}
                        print(f"            model={event['data']['model']}")
                        print(f"            sections={list(sections.keys())}")
                        print(f"            decision={str(sections.get('decision'))[:110]!r}")
                    elif kind == "error":
                        print(f"            !! {event.get('message')}")

    print("-" * 62)
    required = [
        "roster", "positions_complete", "debate_round_complete",
        "review_complete", "aggregate_complete", "verdict_complete", "complete",
    ]
    missing = [r for r in required if r not in seen]

    stray_after = asyncio.run(council_sessions())
    leaked = len(stray_after) - len(stray_before)

    print(f"conversation id   : {cid}")
    print(f"elapsed           : {time.time() - t0:.0f}s")
    print(f"session leak      : {leaked} (must be 0)")

    if missing:
        print(f"MISSING EVENTS    : {missing}")
        return 1
    if leaked > 0:
        print("LEAKED SESSIONS   :")
        for s in stray_after:
            print(f"    {s['id']}  {s.get('title')}")
        return 1

    print("ALL STREAM EVENTS RECEIVED, NO SESSIONS LEAKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
