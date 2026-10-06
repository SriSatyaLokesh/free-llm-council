"""
Intelligent capability scoring matrix for LLM Council Chairman election.

Ranks models by proven reasoning and benchmark intelligence tiers rather than
naive raw context size. Evaluates model IDs, families, context, output limits,
and tool support to designate the most qualified model as Chairman.
"""

import re
from typing import Any, Dict, List, Optional, Union

# Tier definitions with regex patterns and base scores (0 - 100 scale)
TIER_1_PATTERNS = [
    r"claude-3[.-][57]-sonnet",
    r"claude-3-opus",
    r"gpt-4o(?!-mini)",
    r"gpt-4\.5",
    r"\bo[13](?:-mini)?\b",
    r"gemini-(?:1\.5|2\.0|2\.5)-pro",
    r"deepseek-(?:r1|v3|reasoner)",
]

TIER_2_PATTERNS = [
    r"qwen(?:-?2\.5)?-(?:72b|coder-32b)",
    r"llama-3\.[123]-70b",
    r"llama-3-70b",
    r"claude-3[.-]5-haiku",
    r"gpt-4o-mini",
    r"gemini-(?:1\.5|2\.0)-flash",
    r"deepseek-coder-v2",
]

TIER_3_PATTERNS = [
    r"qwen(?:-?2\.5)?-(?:14b|32b)",
    r"mistral-(?:large|nemo)",
    r"mixtral",
    r"codestral",
    r"llama-3\.[123]-8b",
    r"llama-3-8b",
    r"gemma-2-(?:9b|27b)",
]

TIER_4_PATTERNS = [
    r"big-pickle",
    r"small-pickle",
    r"pickle",
    r"llama-3\.2-[13]b",
    r"qwen(?:-?2\.5)?-(?:0\.5b|1\.5b|3b|7b)",
    r"gemma-2-2b",
    r"phi-[34]",
]


def score_model_capability(model_or_id: Union[Dict[str, Any], str]) -> float:
    """
    Compute an intelligence score (0 to 100+) for a given model dict or model ID string.
    """
    if isinstance(model_or_id, str):
        model: Dict[str, Any] = {"id": model_or_id, "name": model_or_id}
    else:
        model = model_or_id

    model_id = (model.get("id") or "").lower()
    name = (model.get("name") or "").lower()
    search_target = f"{model_id} {name}"

    # 1. Base score from intelligence tiers
    base_score = 50.0  # default for unknown model
    matched_tier = None

    for pattern in TIER_1_PATTERNS:
        if re.search(pattern, search_target):
            base_score = 92.0
            matched_tier = 1
            break

    if matched_tier is None:
        for pattern in TIER_2_PATTERNS:
            if re.search(pattern, search_target):
                base_score = 78.0
                matched_tier = 2
                break

    if matched_tier is None:
        for pattern in TIER_3_PATTERNS:
            if re.search(pattern, search_target):
                base_score = 62.0
                matched_tier = 3
                break

    if matched_tier is None:
        for pattern in TIER_4_PATTERNS:
            if re.search(pattern, search_target):
                if "big-pickle" in search_target:
                    base_score = 45.0
                elif "small-pickle" in search_target:
                    base_score = 35.0
                else:
                    base_score = 38.0
                matched_tier = 4
                break

    # 2. Reasoning model bonus
    if any(k in search_target for k in ["reason", "r1", "o1", "o3", "think"]):
        base_score += 4.0

    # 3. Tool capability bonus
    if model.get("supportsTools"):
        base_score += 3.0

    # 4. Context & output window tie-breaking bonus (max +6 context, +3 output)
    context = model.get("context") or 0
    if context > 0:
        base_score += min(6.0, context / 32000.0)

    output = model.get("output") or 0
    if output > 0:
        base_score += min(3.0, output / 4000.0)

    return round(base_score, 2)


def select_best_chairman(models: List[Union[Dict[str, Any], str]]) -> Optional[str]:
    """
    Select the highest capability model ID from a list of model dicts or model IDs.
    """
    if not models:
        return None

    scored = []
    for m in models:
        mid = m["id"] if isinstance(m, dict) else str(m)
        score = score_model_capability(m)
        scored.append((score, mid))

    # Sort descending by score, tiebreak on model ID
    scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return scored[0][1]
