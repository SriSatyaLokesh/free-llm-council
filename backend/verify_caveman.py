"""
Measures what the Caveman levels actually do, on this council.

    python -m backend.verify_caveman

Part 1 - a controlled A/B. The same debate prompt is sent to the same model
twice, once uncompressed and once at each level, so the token difference is
attributable to the level and nothing else. This is the number the toggle
promises, and it is measured rather than assumed.

Part 2 - a full run with the level flipped mid-debate, to prove the mode is
read per round and that the chairman's report stays uncompressed.
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend import caveman, settings  # noqa: E402
from backend.council import CouncilRun  # noqa: E402
from backend.config import COUNCIL_AGENT  # noqa: E402
from backend.opencode_client import CouncilSession, council_permissions  # noqa: E402
import httpx  # noqa: E402

QUESTION = (
    "For a 3-person startup shipping an MVP in 8 weeks with 3 months of runway: "
    "should the backend be one Postgres instance, SQLite, or a hosted API? "
    "Commit to one, then give the single tradeoff that would flip you."
)

PEER_TEXT = """[mimo-v2.6-flash-free]
DEFENDING SQLite. Zero ops, zero network dependency, backups are a file copy.
The locking model is a non-issue at our write volume. The failure mode we
actually care about is engineer time, not query latency, and SQLite minimises it.
[big-pickle]
UPDATING toward managed Postgres. One connection pool, one schema story, and
migrations that do not require a maintenance window. Costs roughly USD 25/mo,
which against 3 months of runway is real money but survivable.
[ling-3.0-flash-fin-free]
DEFENDING the hosted API. We are not in the business of operating a database.
Ship the product, keep the option to swap the storage layer behind an interface."""


async def one_shot(model: str, prompt: str, level: str) -> dict:
    """Send one prompt in a fresh session, with the permissions its level implies."""
    instruction = caveman.build_instruction(level)
    compressed = instruction is not None

    async with httpx.AsyncClient(timeout=300) as client:
        session = CouncilSession(model, client, agent=COUNCIL_AGENT or None)
        await session.create()
        try:
            if compressed:
                await session.set_permissions(
                    council_permissions(allow_research=False)
                )
            result = await session.ask(prompt)
        finally:
            await session.close()

    tokens = result.get("tokens") or {}
    return {
        "level": level,
        "text": result.get("text", ""),
        "output": tokens.get("output", 0),
        "input": tokens.get("input", 0),
        "total": (
            tokens.get("input", 0)
            + tokens.get("output", 0)
            + tokens.get("reasoning", 0)
        ),
        "tools": [t["name"] for t in result.get("toolCalls", [])],
        "error": result.get("error"),
    }


def _median(values: list) -> float:
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2


async def part_one(model: str, repeats: int = 3) -> int:
    """
    Controlled A/B: the same debate prompt to the same model once per level,
    repeated, reporting the median and the full spread.

    A single sample is not enough. On these small free models one run can swing
    several hundred tokens on its own, and an earlier single-sample run here had
    `full` come out *longer* than the uncompressed baseline. The median with the
    range printed next to it is the honest number.
    """
    print("=" * 70)
    print("PART 1 - controlled A/B on an identical debate prompt")
    print(f"model: {model}   repeats: {repeats} per level")
    print("=" * 70)

    levels = ["off", "lite", "full", "ultra", "max"]
    samples: Dict[str, List[int]] = {}
    failures: List[str] = []
    sample_text: Dict[str, str] = {}

    for level in levels:
        instruction = caveman.build_instruction(level)
        if level != "off" and not instruction:
            print(f"[{level:5}] SKIPPED - Caveman skill not installed")
            continue

        prompt = (
            f"{instruction}\n\n---\n\n"
            "ROUND 1 of 2.\n\n"
            f"QUESTION: {QUESTION}\n"
            "YOU: opencode/space-bunny-free\n\n"
            "OPENING POSITIONS:\n"
            f"{PEER_TEXT}\n\n"
            "Contract, unchanged by compression:\n"
            "1. Rebut at least one peer by name. Name the weakest one.\n"
            "2. Concede anything you are genuinely convinced by.\n"
            "3. State whether you are UPDATING or DEFENDING your position.\n"
            "4. Raise the tradeoff the council is most likely to overlook."
        )

        outputs: List[int] = []
        tools_seen: set = set()
        for attempt in range(repeats):
            result = await one_shot(model, prompt, level)
            if result["error"]:
                print(f"[{level:5}] run {attempt + 1} ERROR {result['error']}")
                failures.append(f"{level}: {result['error']}")
                continue
            outputs.append(result["output"])
            tools_seen.update(result["tools"])
            sample_text.setdefault(level, result["text"])
            print(f"[{level:5}] run {attempt + 1}: output={result['output']} tok")

        if outputs:
            samples[level] = outputs
            if tools_seen:
                print(f"[{level:5}] tools used: {sorted(tools_seen)}")

    if "off" not in samples:
        return ["no uncompressed baseline"] + failures

    baseline = _median(samples["off"])
    print("\n" + "-" * 70)
    print(f"{'level':6} {'median':>8} {'min':>7} {'max':>7} {'vs off':>9}")
    for level, outputs in samples.items():
        median = _median(outputs)
        pct = (median - baseline) / baseline * 100
        print(f"{level:6} {median:8.0f} {min(outputs):7} {max(outputs):7} "
              f"{pct:+8.0f}%")

    # ultra is the clearest case, so it is the one worth asserting on.
    if "ultra" in samples:
        ultra = _median(samples["ultra"])
        pct = (ultra - baseline) / baseline * 100
        print(f"\nultra median is {pct:+.0f}% vs off")
        if pct >= 0:
            failures.append(
                f"ultra did not reduce output tokens ({pct:+.0f}% over {repeats} runs)"
            )
        else:
            print(f"ultra reduced output tokens by {-pct:.0f}% at the median")

    # max should achieve substantial compression
    if "max" in samples:
        max_val = _median(samples["max"])
        pct_max = (max_val - baseline) / baseline * 100
        print(f"\nmax median is {pct_max:+.0f}% vs off")
        if pct_max >= 0:
            failures.append(
                f"max did not reduce output tokens ({pct_max:+.0f}% over {repeats} runs)"
            )
        else:
            print(f"max reduced output tokens by {-pct_max:.0f}% at the median")

    # And a level that loses must be reported, not buried.
    for level in ("lite", "full"):
        if level in samples:
            pct = (_median(samples[level]) - baseline) / baseline * 100
            if pct > 0:
                print(f"NOTE: {level} came out {pct:+.0f}% vs off on this sample - "
                      f"these small models vary a lot at n={repeats}")

    head = (sample_text.get("ultra", "") or "").strip()[:40].upper()
    if sample_text.get("ultra") and not ("UPDATING" in head or "DEFENDING" in head):
        print(f"WARNING: ultra did not lead with UPDATING/DEFENDING (got {head!r})")
        failures.append("ultra broke the UPDATING/DEFENDING contract")
    elif sample_text.get("ultra"):
        print("ultra rounds led with UPDATING/DEFENDING - contract held")

    head_max = (sample_text.get("max", "") or "").strip()[:40].upper()
    if sample_text.get("max") and not ("UPDATING" in head_max or "DEFENDING" in head_max):
        print(f"WARNING: max did not lead with UPDATING/DEFENDING (got {head_max!r})")
        failures.append("max broke the UPDATING/DEFENDING contract")
    elif sample_text.get("max"):
        print("max rounds led with UPDATING/DEFENDING - contract held")

    return failures


async def part_two() -> int:
    print("\n" + "=" * 70)
    print("PART 2 - full run, flipping the level mid-debate")
    print("=" * 70)

    members = ["opencode/big-pickle", "opencode/mimo-v2.6-flash-free"]
    settings.update_settings({"debateMode": "off"})

    run = CouncilRun(QUESTION, members, "opencode/big-pickle", rounds=2)
    queue: asyncio.Queue = asyncio.Queue()

    driver = asyncio.create_task(run.run_stream(queue))

    rounds_seen = []
    flipped = False
    while True:
        kind, payload = await queue.get()
        if kind is None:
            break
        if kind == "debate_round":
            rounds_seen.append({
                "round": payload["round"],
                "level": payload.get("cavemanLevel"),
                "compressed": payload.get("compressed"),
                "output": (payload.get("tokens") or {}).get("output", 0),
            })
            print(f"  round {payload['round']}: level={payload.get('cavemanLevel')}"
                  f" output={(payload.get('tokens') or {}).get('output', 0)}")

            # Flip only once round 1 has actually been dispatched. A timer would
            # race the opening round, which can take minutes.
            if payload["round"] == 1 and not flipped:
                flipped = True
                print("  >>> flipping debate mode off -> ultra after round 1")
                settings.update_settings({"debateMode": "ultra"})
        elif kind == "verdict":
            sections = payload.get("sections") or {}
            print(f"  verdict sections: {list(sections.keys())}")
    await driver

    failures = []
    levels = [r["level"] for r in rounds_seen]
    print(f"\n  levels per round: {levels}")
    failures: List[str] = []
    if levels != ["off", "ultra"]:
        failures.append(f"mid-run flip not honoured: rounds ran at {levels}")
    else:
        print("  mid-run flip honoured: round 1 off, round 2 ultra")

    verdict = run.result.get("verdict") or {}
    sections = verdict.get("sections") or {}
    full_text = verdict.get("response") or ""
    total_words = len(full_text.split())

    print(f"  verdict total length: {total_words} words, "
          f"{(verdict.get('tokens') or {}).get('output', 0)} output tokens")
    for name in ("decision", "reasoning", "tradeoffs", "dissent", "confidence"):
        words = len(sections.get(name, "").split())
        print(f"    {name:10} {words:>4} words")

    # Judge the whole report, not the Decision section. A crisp Decision is
    # supposed to be short; the length lives in Reasoning and Tradeoffs, and an
    # earlier version of this check failed a perfectly detailed verdict for
    # having a 76-word Decision.
    failures = []
    if total_words < 400:
        failures.append(
            f"verdict looks compressed overall ({total_words} words)"
        )
    else:
        print("  verdict stayed a full report despite the compressed debate")

    for name in ("reasoning", "tradeoffs"):
        if len(sections.get(name, "").split()) < 40:
            failures.append(f"verdict section '{name}' looks thin")

    cav = (run.result.get("metadata") or {}).get("caveman") or {}
    print("\n  token report:")
    for stage in (cav.get("stages") or {}).values():
        print(f"    {stage['label']:14} mode={stage['mode']:12} "
              f"output={stage['tokens']['output']:>7} total={stage['tokens']['total']:>8}")
    print(f"    {'TOTAL':14} {'':12} {'':7}      total={cav.get('total')}")

    stray = await council_sessions()
    if stray:
        failures.append(f"{len(stray)} council sessions leaked")
    else:
        print("  no council sessions leaked")

    return failures


async def council_sessions():
    async with httpx.AsyncClient(timeout=60) as client:
        from backend import opencode_client as oc
        response = await client.get(
            f"{oc.get_server_url()}/api/session",
            params=oc._location_params(),
            headers=oc._auth_headers(),
        )
    return [s for s in (response.json().get("data") or [])
            if str(s.get("title", "")).startswith("council:")]


async def main() -> int:
    if not caveman.is_installed():
        print("Caveman is not installed. Run:")
        print(f"  {caveman.INSTALL_COMMAND}")
        return 1

    models = await __import__(
        "backend.opencode_client", fromlist=["list_models"]
    ).list_models()
    model = models[0]["id"]

    repeats = 3
    if "--quick" in sys.argv:
        repeats = 1
        print("--quick: 1 run per level, noisy\n")

    failures = await part_one(model, repeats=repeats)
    failures += await part_two()

    print("\n" + "=" * 70)
    if failures:
        print("FAILURES:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("CAVEMAN VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
