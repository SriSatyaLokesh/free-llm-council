"""Live test script executing an end-to-end deliberation across real OpenCode models."""

import httpx
import json
import time

def run():
    client = httpx.Client(timeout=180.0)

    # 1. Health verification
    health = client.get("http://localhost:8001/api/health").json()
    print("OpenCode Health:", health)

    # 2. Create conversation
    conv = client.post("http://localhost:8001/api/conversations", json={}).json()
    conv_id = conv["id"]
    print(f"Created conversation ID: {conv_id}")

    # 3. Choose max mode
    client.post("http://localhost:8001/api/settings", json={"debateMode": "max"})

    # 4. Run council deliberation
    payload = {
        "content": "Should small engineering teams adopt monorepo or polyrepo in 2026? State 1 core reason concisely.",
        "members": ["opencode/big-pickle", "opencode/space-bunny-free"],
        "rounds": 1,
        "token_cap_per_model": 250000,
        "token_budget_total": 500000,
        "time_limit_seconds": 120.0,
    }
    print("Starting council deliberation across live models...")
    start_t = time.time()
    res = client.post(f"http://localhost:8001/api/conversations/{conv_id}/message", json=payload)
    elapsed = time.time() - start_t
    print(f"Deliberation completed in {elapsed:.1f}s with HTTP {res.status_code}")

    if res.status_code != 200:
        print("Error detail:", res.text)
        return

    data = res.json()

    print("\n--- STAGE 1: OPENING POSITIONS ---")
    for pos in data.get("positions", []):
        print(f"[{pos['model']}] ({pos.get('tokens', {}).get('total', 0)} tokens):")
        print(pos.get("response", "").strip()[:180] + "...\n")

    print("--- STAGE 2: DEBATE ROUNDS (CAVEMAN MAX) ---")
    for rd in data.get("debate", []):
        print(f"Round {rd.get('round')} (Caveman Level: {rd.get('cavemanLevel')}):")
        for stmt in rd.get("statements", []):
            print(f"  [{stmt['model']}]: {stmt.get('response', '').strip()[:150]}...")

    print("\n--- STAGE 3: BLIND PEER REVIEW ---")
    for rev in data.get("review", []):
        print(f"Reviewer scored rankings: {rev.get('parsed_ranking')}")

    print("\n--- STAGE 4: CHAIRMAN VERDICT ---")
    verdict = data.get("verdict", {})
    print(f"Elected Chairman: {verdict.get('model')}")
    print(f"Total verdict tokens: {verdict.get('tokens', {}).get('total', 0)}")
    sections = verdict.get("sections", {})
    if sections:
        for k, v in sections.items():
            print(f"[{k.upper()}]: {v[:120].strip()}...")
    else:
        print("Verdict body:", verdict.get("response", "")[:300])

if __name__ == "__main__":
    run()
