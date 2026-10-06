"""
Official Caveman compression, loaded at runtime from the installed skill.

Source of truth: https://github.com/JuliusBrussee/caveman
Install (the project's own installer, non-interactive):

    npx skills add JuliusBrussee/caveman -g -y --agent '*'

This module does not restate Caveman's rules. It reads the installed SKILL.md
and lifts the relevant sections verbatim, so upgrading the skill upstream
changes the council's behaviour with no code edit here.

Why the skill and not the proxy
-------------------------------
Caveman ships three surfaces:

* the **skill** shrinks what the model *writes*
* the **proxy** shrinks what the model *reads* (tool output, logs)
* the **middleware** wraps provider calls in *your own* code

The council talks to models through opencode sessions, so we never make the
provider call ourselves and the middleware does not apply. The proxy could
compress web research, but that means wrapping opencode itself
(`caveman opencode`), which is a separate, larger change. The skill is the
surface we can actually apply per-stage from a prompt, and the debate is
almost entirely model output.

Levels are Caveman's own: `off`, `lite`, `full`, `ultra` (plus the upstream
wenyan variants, which are omitted here because the council reasons in English).
"""

import re
from pathlib import Path
from typing import Dict, Optional

# Levels the council exposes. "off" is not an upstream level name - it is the
# skill's own off switch, and it means "no compression at all".
LEVELS = ("off", "lite", "full", "ultra", "max")

# Upstream levels that exist in the skill but do not apply to this council.
UNSUPPORTED_UPSTREAM_LEVELS = (
    "wenyan-lite", "wenyan-full", "wenyan-ultra",
)

# Where the official installer puts skills, most specific first.
SKILL_CANDIDATES = (
    Path.home() / ".agents" / "skills" / "caveman" / "SKILL.md",
    Path.home() / ".claude" / "skills" / "caveman" / "SKILL.md",
    Path.home() / ".config" / "opencode" / "skills" / "caveman" / "SKILL.md",
)

INSTALL_COMMAND = "npx skills add JuliusBrussee/caveman -g -y --agent '*'"

_cache: Dict[str, str] = {}


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------

def skill_path() -> Optional[Path]:
    for candidate in SKILL_CANDIDATES:
        if candidate.exists():
            return candidate
    return None


def is_installed() -> bool:
    return skill_path() is not None


def load_skill() -> Optional[str]:
    """
    Read the installed SKILL.md, cached against the file's mtime.

    Returns None when Caveman is not installed - the caller decides whether to
    warn or to fall back to normal prose.
    """
    path = skill_path()
    if path is None:
        return None

    try:
        mtime = str(path.stat().st_mtime)
    except OSError:
        return None

    if _cache.get("mtime") != mtime:
        try:
            _cache["body"] = path.read_text(encoding="utf-8")
            _cache["mtime"] = mtime
        except OSError:
            return None

    return _cache.get("body")


# --------------------------------------------------------------------------
# Parsing the official document
# --------------------------------------------------------------------------

def _section(body: str, heading: str) -> str:
    """Return the text under '## <heading>', up to the next '## '."""
    pattern = rf"^##\s+{re.escape(heading)}\s*$(.*?)(?=^##\s|\Z)"
    match = re.search(pattern, body, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def intensity_for(body: str, level: str) -> str:
    """
    Pull one level's row out of Caveman's own Intensity table.

    Keeping this parsed rather than hardcoded means the description of a level
    always matches the installed skill.
    """
    if level == "max":
        return "Extreme claim-and-evidence protocol. Drop all grammar/filler. Structured tokens only."
    table = _section(body, "Intensity")
    if not table:
        return ""
    for line in table.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0].strip("*").strip() == level:
            return " ".join(c for c in cells[1:] if c)
    return ""


# --------------------------------------------------------------------------
# Instruction assembly
# --------------------------------------------------------------------------

_MAX_CONTRACT = """\
CAVEMAN MAX MODE ACTIVE. MAXIMUM DENSITY CLAIM-AND-EVIDENCE PROTOCOL.
YOU ARE AN LLM COUNCIL MEMBER ARGUING WITH PEERS. HUMAN READS ONLY CHAIRMAN FINAL REPORT.

MANDATORY SYNTAX CONTRACT:
- First word must be UPDATING or DEFENDING. Do not omit or alter.
- Target: PEER: <exact_model_name_from_roster>
- Concession (optional): CONCEDE: <exact_point_if_any>
- Objection: REBUT: <exact_point_contested>
- Evidence/Tradeoff: EVIDENCE: <concrete_fact_benchmark_or_tradeoff>
- ZERO pleasantries, ZERO conversational filler, ZERO greetings, ZERO articles (a, an, the).
- CRITICAL NEGATION RULE: Never drop negation words. "not", "never", "no", "only", "except" MUST survive compression. Inverting negation corrupts argument polarity.
- ZERO TOOLS: Argue strictly from evidence already gathered in opening round.
"""

# Framing written for this council. The Caveman rules themselves are lifted
# verbatim from the installed skill above; only this wrapper and the output
# contract below are ours.
_COUNCIL_FRAMING = """\
You are a member of an LLM Council, mid-debate, talking to the other members. \
A human reads only the chairman's final report at the end - not this exchange.

CAVEMAN MODE IS ACTIVE FOR THIS MESSAGE AT LEVEL: {level}.
{level_rule}
Council output contract, which overrides any stylistic preference above:
- First three words are exactly UPDATING or DEFENDING. Do not abbreviate, \
censor or reword them. They are the parsed signal the council votes on.
- Name the peer you are rebutting, spelled exactly as given in the roster.
- Never drop a negation. "not", "never", "no", "only", "except" survive \
compression, because inverting one changes the argument rather than shortening it.
- Do not use tools. You researched in the opening round; argue from what you have.
- If a sentence would be ambiguous as a fragment, write it in full. Caveman \
stops where clarity would stop. An unparseable or self-contradicting turn costs \
the council more than the tokens it saved.

{rules}

{auto_clarity}

{boundaries}"""


def build_instruction(level: str) -> Optional[str]:
    """
    Build the Caveman instruction for a level, or None for "off".

    Returns None when the level is "off" or when the skill is not installed -
    in the latter case the council simply runs uncompressed rather than
    silently substituting rules of our own.
    """
    if level == "off":
        return None

    if level == "max":
        return _MAX_CONTRACT.strip()

    body = load_skill()
    if not body:
        return None

    level = level if level in LEVELS else "full"

    return _COUNCIL_FRAMING.format(
        level=level,
        level_rule=intensity_for(body, level),
        rules=_section(body, "Rules"),
        auto_clarity=_section(body, "Auto-Clarity"),
        boundaries=_section(body, "Boundaries"),
    ).strip()


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------

def status() -> Dict[str, object]:
    """What the UI needs to render the mode picker honestly."""
    path = skill_path()
    body = load_skill() if path else None
    return {
        "installed": body is not None,
        "path": str(path) if path else None,
        "source": "https://github.com/JuliusBrussee/caveman",
        "installCommand": INSTALL_COMMAND,
        "levels": list(LEVELS),
        "unsupportedUpstreamLevels": list(UNSUPPORTED_UPSTREAM_LEVELS),
        "levelDescriptions": {
            level: intensity_for(body, level) if body else ""
            for level in LEVELS
        },
    }
