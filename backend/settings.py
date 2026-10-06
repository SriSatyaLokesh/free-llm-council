"""
Live, mutable council settings.

These are deliberately process-global rather than per-request so the user can
change them *while a run is in progress*. `CouncilRun` reads them immediately
before building each round's prompt, so flipping the toggle mid-debate takes
effect from the next round onwards.

Assigning a single value in a module-level dict is atomic under the GIL, and
`asyncio` runs handlers on one thread, so no lock is needed.
"""

from typing import Any, Dict, List, Optional

from .caveman import LEVELS
from .config import DEBATE_MODE

# Caveman's own levels, plus "off" which means no compression at all.
DEBATE_MODES = tuple(LEVELS)

DEFAULT_DEBATE_MODE = DEBATE_MODE if DEBATE_MODE in DEBATE_MODES else "full"

# Where caveman compression applies. Positions and the verdict are always
# written out in full.
DEBATE_MODE_SCOPE = (
    "debate rounds and the blind peer review",
)

_settings: Dict[str, Any] = {
    "debateMode": DEFAULT_DEBATE_MODE,
    "tokenCapPerModel": None,
    "tokenBudgetTotal": None,
    "timeLimitSeconds": None,
}

# Which mode each stage of the current run used, so the UI can show what the
# toggle actually changed. Keyed by nothing in particular - single run.
_run_modes: Dict[str, str] = {}


def get_settings() -> Dict[str, Any]:
    return dict(_settings)


def get_debate_mode() -> str:
    mode = _settings.get("debateMode")
    return mode if mode in DEBATE_MODES else DEFAULT_DEBATE_MODE


def get_token_cap_per_model() -> Any:
    return _settings.get("tokenCapPerModel")


def get_token_budget_total() -> Any:
    return _settings.get("tokenBudgetTotal")


def get_time_limit_seconds() -> Any:
    return _settings.get("timeLimitSeconds")


def update_settings(patch: Dict[str, Any]) -> Dict[str, Any]:
    """Apply a partial update. Unknown keys and bad values are ignored."""
    if "debateMode" in patch:
        mode = patch["debateMode"]
        if mode in DEBATE_MODES:
            _settings["debateMode"] = mode
    if "tokenCapPerModel" in patch:
        val = patch["tokenCapPerModel"]
        _settings["tokenCapPerModel"] = int(val) if val is not None else None
    if "tokenBudgetTotal" in patch:
        val = patch["tokenBudgetTotal"]
        _settings["tokenBudgetTotal"] = int(val) if val is not None else None
    if "timeLimitSeconds" in patch:
        val = patch["timeLimitSeconds"]
        _settings["timeLimitSeconds"] = float(val) if val is not None else None
    return get_settings()



def record_stage_mode(stage: str, mode: str) -> None:
    """Note which mode a stage ran in."""
    _run_modes[stage] = mode


def get_run_modes() -> Dict[str, str]:
    return dict(_run_modes)


def reset_run_modes() -> None:
    _run_modes.clear()


def reconcile_council_preset(
    preset: Dict[str, Any],
    available_models: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Reconciles a saved council preset against currently available OpenCode models.

    - Preserves members that are still available.
    - If a model is missing, attempts to find an updated version of the same family.
    - Ensures minimum quorum (at least 2 members).
    - Reconciles Chairman: if saved chairman is gone, updates to new replacement or best available.
    - Reconciles thinking variants: keeps valid variant if supported by model, else falls back to default.
    """
    avail_ids = [m["id"] for m in available_models]
    id_to_model = {m["id"]: m for m in available_models}

    reconciled = dict(preset)
    saved_members = preset.get("members") or []
    new_members = []
    replacement_map = {}

    for m in saved_members:
        if m in avail_ids:
            new_members.append(m)
        else:
            # Look for an upgraded version or family match
            # e.g., 'ling-3.0-flash-fin-free' -> search for 'ling' in avail_ids
            base_key = m.split("/")[-1].split("-")[0]
            candidate = next(
                (aid for aid in avail_ids if base_key in aid and aid not in new_members),
                None,
            )
            if candidate:
                new_members.append(candidate)
                replacement_map[m] = candidate

    # Ensure at least 2 members if available
    if len(new_members) < 2 and len(avail_ids) >= 2:
        for aid in avail_ids:
            if aid not in new_members:
                new_members.append(aid)
            if len(new_members) >= 2:
                break

    reconciled["members"] = new_members

    # Reconcile Chairman
    saved_chair = preset.get("chairman")
    if saved_chair:
        if saved_chair in new_members:
            reconciled["chairman"] = saved_chair
        elif saved_chair in replacement_map:
            reconciled["chairman"] = replacement_map[saved_chair]
        elif new_members:
            reconciled["chairman"] = new_members[0]
        else:
            reconciled["chairman"] = None

    # Reconcile modelThinking
    saved_thinking = preset.get("modelThinking") or {}
    new_thinking = {}
    for m, variant in saved_thinking.items():
        target_m = replacement_map.get(m, m)
        if target_m in id_to_model:
            model_info = id_to_model[target_m]
            variants = [
                v["id"] if isinstance(v, dict) else str(v)
                for v in model_info.get("variants", [])
            ]
            if variant in variants:
                new_thinking[target_m] = variant
            elif variants:
                new_thinking[target_m] = (
                    variants[-1] if target_m == reconciled.get("chairman") else variants[0]
                )
    reconciled["modelThinking"] = new_thinking

    return reconciled
