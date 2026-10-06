"""
Four-stage LLM Council orchestration.

  Stage 1  Positions   - every member answers independently
  Stage 2  Debate      - N rounds of named cross-examination
  Stage 3  Review      - anonymous scoring, to counter self-favouritism
  Stage 4  Verdict     - the chairman decides, with tradeoffs and dissent

Each member keeps ONE opencode session for the whole run, so by the time it
reaches the debate it still remembers its own position and its own previous
turns. That is what makes the exchange feel like a debate rather than a
sequence of independent prompts.
"""

import asyncio
import re
import time
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

import httpx


from . import caveman as caveman_mod
from . import prompts, settings
from .config import (
    CHAIRMAN_MODEL,
    COUNCIL_AGENT,
    COUNCIL_MODELS,
    DEBATE_ROUNDS,
    PER_MODEL_TIMEOUT,
)
from .opencode_client import (
    CouncilSession,
    OpencodeUnavailable,
    council_permissions,
    default_chairman,
    list_models,
)

# Maximum characters of a member's text carried into the next stage's prompt.
# Guards against a runaway generation blowing out another model's context.
MAX_QUOTE_CHARS = 12000

# Same guard for a compressed round. Caveman already shortens the text; this
# stops one verbose member dominating the next round's prompt.
MAX_QUOTE_CHARS_COMPRESSED = 4000


# --------------------------------------------------------------------------
# Roster resolution
# --------------------------------------------------------------------------

async def resolve_roster(
    members: Optional[List[str]] = None,
    chairman: Optional[str] = None,
) -> Tuple[List[str], str]:
    """
    Work out who sits on the council and who chairs it.

    Defaults to every model opencode has, with the largest-context model as
    chairman.
    """
    from .hybrid_client import list_unified_models
    available = await list_unified_models()
    available_ids = [m["id"] for m in available]

    if members:
        selected = [m for m in members if m in available_ids]
        # Keep the caller's ordering, drop anything opencode no longer offers.
    elif COUNCIL_MODELS:
        selected = [m for m in COUNCIL_MODELS if m in available_ids]
    else:
        selected = list(available_ids)

    if not selected:
        raise OpencodeUnavailable(
            "No council members available. Check that opencode is running and "
            "has at least one model configured."
        )

    chair = chairman or CHAIRMAN_MODEL
    if not chair or chair not in available_ids:
        # Prefer the highest capability member from the selected council
        from .capability_matrix import select_best_chairman
        selected_models_meta = [m for m in available if m["id"] in selected]
        chair = select_best_chairman(selected_models_meta) or selected[0]

    return selected, chair


# --------------------------------------------------------------------------
# Formatting helpers
# --------------------------------------------------------------------------

def _clip(text: str, limit: int = MAX_QUOTE_CHARS) -> str:
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit] + "\n\n[...truncated...]"


def _label(index: int) -> str:
    """0 -> 'A', 1 -> 'B', ... 'Z', then 'AA'."""
    letters = ""
    index += 1
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def _sum_tokens(entries: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Total the token counts opencode reported for a set of entries.

    opencode returns {input, output, reasoning, cache} and no `total`, so the
    total is computed here. Cache reads are excluded: they are cheaper than
    fresh input and would flatter the compressed stages, which is the opposite
    of what this number is for.
    """
    input_ = output = reasoning = 0
    for entry in entries:
        tokens = entry.get("tokens") or {}
        input_ += tokens.get("input", 0) or 0
        output += tokens.get("output", 0) or 0
        reasoning += tokens.get("reasoning", 0) or 0
    return {
        "input": input_,
        "output": output,
        "reasoning": reasoning,
        "total": input_ + output + reasoning,
    }


def _positions_block(positions: List[Dict[str, Any]], limit: int = MAX_QUOTE_CHARS) -> str:
    return "\n\n".join(
        f"[{p['model']}]\n{_clip(p['response'], limit)}"
        for p in positions
        if p.get("response")
    )


def _debate_block(rounds: List[Dict[str, Any]], limit: int = MAX_QUOTE_CHARS) -> str:
    if not rounds:
        return "(no debate rounds ran)"
    out = []
    for round_data in rounds:
        out.append(f"--- ROUND {round_data['round']} ---")
        for statement in round_data["statements"]:
            if statement.get("response"):
                out.append(f"[{statement['model']}]\n{_clip(statement['response'], limit)}")
    return "\n\n".join(out)


def _review_block(reviews: List[Dict[str, Any]]) -> str:
    return "\n\n".join(
        f"[{r['model']}]\n{_clip(r['ranking'], 6000)}"
        for r in reviews
        if r.get("ranking")
    ) or "(no peer reviews returned)"


def _aggregate_block(aggregate: List[Dict[str, Any]]) -> str:
    if not aggregate:
        return "(no scores parsed)"
    return "\n".join(
        f"  {i + 1}. {a['model']:<40} avg rank {a['average_rank']} "
        f"({a['rankings_count']} review(s))"
        for i, a in enumerate(aggregate)
    )


# --------------------------------------------------------------------------
# Ranking parsing (carried over from the original implementation)
# --------------------------------------------------------------------------

def parse_ranking_from_text(ranking_text: str) -> List[str]:
    """Extract the ordered labels from a 'FINAL RANKING:' block."""
    ranking_text = ranking_text or ""

    if "FINAL RANKING:" in ranking_text:
        section = ranking_text.split("FINAL RANKING:")[-1]
        numbered = re.findall(r"\d+\.\s*Response [A-Z]+", section)
        if numbered:
            return [re.search(r"Response [A-Z]+", m).group() for m in numbered]
        return re.findall(r"Response [A-Z]+", section)

    return re.findall(r"Response [A-Z]+", ranking_text)


def calculate_aggregate_rankings(
    reviews: List[Dict[str, Any]],
    label_to_model: Dict[str, str],
) -> List[Dict[str, Any]]:
    """Average each model's rank position across every peer review."""
    positions: Dict[str, List[int]] = defaultdict(list)

    for review in reviews:
        for rank, label in enumerate(review.get("parsed_ranking") or [], start=1):
            model = label_to_model.get(label)
            if model:
                positions[model].append(rank)

    aggregate = [
        {
            "model": model,
            "average_rank": round(sum(ranks) / len(ranks), 2),
            "rankings_count": len(ranks),
        }
        for model, ranks in positions.items()
        if ranks
    ]
    aggregate.sort(key=lambda a: a["average_rank"])
    return aggregate


# --------------------------------------------------------------------------
# Active Run Registry
# --------------------------------------------------------------------------

_active_runs: Dict[str, "CouncilRun"] = {}


def register_active_run(conversation_id: str, run: "CouncilRun") -> None:
    """Register an ongoing CouncilRun by conversation ID."""
    _active_runs[conversation_id] = run


def unregister_active_run(conversation_id: str) -> None:
    """Unregister an ongoing CouncilRun by conversation ID."""
    _active_runs.pop(conversation_id, None)


def get_active_run(conversation_id: str) -> Optional["CouncilRun"]:
    """Retrieve the active CouncilRun for a conversation ID, if any."""
    return _active_runs.get(conversation_id)


# --------------------------------------------------------------------------
# The run
# --------------------------------------------------------------------------

class CouncilRun:
    """One council deliberation, owning every session it creates."""

    def __init__(
        self,
        user_query: str,
        members: List[str],
        chairman: str,
        rounds: Optional[int] = None,
        token_cap_per_model: Optional[int] = None,
        token_budget_total: Optional[int] = None,
        time_limit_seconds: Optional[float] = None,
        model_thinking: Optional[Dict[str, str]] = None,
    ):
        self.user_query = user_query
        self.members = members
        self.chairman = chairman
        self.rounds = DEBATE_ROUNDS if rounds is None else max(0, int(rounds))
        self.token_cap_per_model = (
            token_cap_per_model
            if token_cap_per_model is not None
            else settings.get_token_cap_per_model()
        )
        self.token_budget_total = (
            token_budget_total
            if token_budget_total is not None
            else settings.get_token_budget_total()
        )
        self.time_limit_seconds = (
            time_limit_seconds
            if time_limit_seconds is not None
            else settings.get_time_limit_seconds()
        )
        self.model_thinking: Dict[str, str] = dict(model_thinking or {})
        self.resolved_thinking: Dict[str, Optional[str]] = {}

        self.sessions: Dict[str, CouncilSession] = {}
        self.chair_session: Optional[CouncilSession] = None
        self.active_members: List[str] = list(members)
        self.evicted_members: List[Dict[str, Any]] = []

        # Token & Time tracking
        self.start_time: float = time.monotonic()
        self.model_tokens: Dict[str, Dict[str, int]] = {
            m: {"input": 0, "output": 0, "reasoning": 0, "total": 0} for m in members
        }
        self.total_tokens: Dict[str, int] = {
            "input": 0, "output": 0, "reasoning": 0, "total": 0
        }
        self.retired_members: Dict[str, Dict[str, Any]] = {}

        # Human-in-the-loop steering & guidance
        self.injected_guidance: List[Dict[str, Any]] = []
        self._guidance_queue: List[Dict[str, Any]] = []
        self._stream_queue: Optional[asyncio.Queue] = None

        # Populated by run(), so the caller can persist the result afterwards.
        self.result: Optional[Dict[str, Any]] = None

    def inject_steering(
        self, message: str, resources: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Inject human operator guidance and resources into the ongoing deliberation."""
        entry = {
            "message": message.strip(),
            "resources": [r.strip() for r in (resources or []) if r.strip()],
            "timestamp": time.time(),
        }
        self.injected_guidance.append(entry)
        self._guidance_queue.append(entry)
        if self._stream_queue is not None:
            try:
                self._stream_queue.put_nowait(("human_guidance_injected", entry))
            except Exception:
                pass
        return entry

    def resolve_thinking_config(
        self, available_variants: Optional[Dict[str, List[Any]]] = None
    ) -> Dict[str, Optional[str]]:
        """
        Determine thinking quality / reasoning effort per model:
        - Honored if explicitly provided by the user in self.model_thinking.
        - Otherwise, Chairman defaults to 'max' (or highest available variant).
        - Regular members default to 'medium' (or 'high' / first available).
        - Returns None for models without variants.
        """
        if available_variants is None:
            available_variants = {}

        resolved: Dict[str, Optional[str]] = {}
        for m in self.members:
            if m in self.model_thinking:
                resolved[m] = self.model_thinking[m]
                continue

            variants_raw = available_variants.get(m, [])
            variant_ids = [
                v["id"] if isinstance(v, dict) else str(v)
                for v in variants_raw
            ]

            if not variant_ids:
                resolved[m] = None
                continue

            if m == self.chairman:
                if "max" in variant_ids:
                    resolved[m] = "max"
                elif "xhigh" in variant_ids:
                    resolved[m] = "xhigh"
                elif "high" in variant_ids:
                    resolved[m] = "high"
                else:
                    resolved[m] = variant_ids[-1]
            else:
                if "medium" in variant_ids:
                    resolved[m] = "medium"
                elif "high" in variant_ids:
                    resolved[m] = "high"
                elif "low" in variant_ids:
                    resolved[m] = "low"
                else:
                    resolved[m] = variant_ids[0]

        self.resolved_thinking = resolved
        return resolved

    def _record_model_tokens(self, model: str, token_data: Dict[str, Any]) -> None:
        """Accumulate token telemetry for a model and update global council totals."""
        if not token_data:
            return

        if model not in self.model_tokens:
            self.model_tokens[model] = {"input": 0, "output": 0, "reasoning": 0, "total": 0}

        inp = token_data.get("input", 0) or 0
        out = token_data.get("output", 0) or 0
        reasoning = token_data.get("reasoning", 0) or 0
        total = token_data.get("total")
        if total is None:
            total = inp + out + reasoning

        self.model_tokens[model]["input"] += inp
        self.model_tokens[model]["output"] += out
        self.model_tokens[model]["reasoning"] += reasoning
        self.model_tokens[model]["total"] += total

        self.total_tokens["input"] += inp
        self.total_tokens["output"] += out
        self.total_tokens["reasoning"] += reasoning
        self.total_tokens["total"] += total

    async def _check_budget_limits(
        self, round_num: Optional[int] = None, emit=None
    ) -> List[str]:
        """
        Check if any active model has exceeded token_cap_per_model.
        If exceeded, retire the model from future debate rounds.
        """
        if not self.token_cap_per_model:
            return []

        retired_now = []
        for model in list(self.active_members):
            cum_total = self.model_tokens.get(model, {}).get("total", 0)
            if cum_total >= self.token_cap_per_model:
                self.active_members.remove(model)
                record = {
                    "model": model,
                    "stage": "budget",
                    "round": round_num,
                    "reason": "token_cap_reached",
                    "tokens": cum_total,
                }
                self.retired_members[model] = record
                retired_now.append(model)
                print(
                    f"[council] RETIRED {model} at round {round_num}: "
                    f"used {cum_total} tokens (cap: {self.token_cap_per_model})"
                )

                # Close session to free resources
                session = self.sessions.pop(model, None)
                if session:
                    try:
                        await session.close()
                    except Exception:
                        pass

                if emit:
                    await emit("model_retired", record)

        if retired_now:
            self._ensure_active_chairman()

        return retired_now

    async def _check_debate_stopping_conditions(
        self, round_num: int, emit=None
    ) -> Tuple[bool, Optional[str]]:
        """
        Determine if the debate loop should terminate early due to:
        1. Total token budget exhausted
        2. Wall-clock time limit reached
        3. Fewer than 2 active members remaining
        """
        if self.token_budget_total and self.total_tokens.get("total", 0) >= self.token_budget_total:
            reason = "token_budget_exhausted"
            if emit:
                await emit("debate_concluded_early", {"round": round_num, "reason": reason})
            return True, reason

        if self.time_limit_seconds:
            elapsed = time.monotonic() - self.start_time
            if elapsed >= self.time_limit_seconds:
                reason = "time_limit_exceeded"
                if emit:
                    await emit("debate_concluded_early", {"round": round_num, "reason": reason})
                return True, reason

        if len(self.active_members) < 2:
            reason = "insufficient_active_members"
            if emit:
                await emit("debate_concluded_early", {"round": round_num, "reason": reason})
            return True, reason

        return False, None

    async def _evict(
        self,
        model: str,
        stage: str,
        round_num: Optional[int] = None,
        reason: str = "Unknown error",
        emit=None,
    ) -> None:
        """Evict a failing or depleted model immediately and ensure it is never called again."""
        if model in self.active_members:
            self.active_members.remove(model)

        record = {
            "model": model,
            "stage": stage,
            "round": round_num,
            "reason": reason,
        }
        self.evicted_members.append(record)
        print(f"[council] EVICTED {model} during {stage} (round {round_num}): {reason}")

        # Close session immediately to free resources
        session = self.sessions.pop(model, None)
        if session:
            try:
                await session.close()
            except Exception:
                pass

        if emit:
            await emit("model_evicted", record)

    def _ensure_active_chairman(self) -> str:
        """If current chairman is evicted or inactive, fail over to the next highest-capability survivor."""
        if self.chairman in self.active_members:
            return self.chairman
        if self.active_members:
            prev = self.chairman
            from .capability_matrix import select_best_chairman
            self.chairman = select_best_chairman(self.active_members) or self.active_members[0]
            print(f"[council] Chairman failover: {prev} -> {self.chairman}")
            return self.chairman
        return self.chairman


    # -- session lifecycle -------------------------------------------------

    async def _open_sessions(self, client: httpx.AsyncClient) -> List[str]:
        """Create one session per member with resolved thinking quality. Returns the members that came up."""
        from .hybrid_client import list_unified_models
        try:
            unified = await list_unified_models()
            avail_variants = {m["id"]: m.get("variants", []) for m in unified}
        except Exception:
            avail_variants = {}

        self.resolve_thinking_config(avail_variants)

        created = []

        async def _call_make(m: str):
            v = self.resolved_thinking.get(m)
            try:
                return await self._make_session(
                    client,
                    m,
                    self.sessions,
                    variant=v,
                )
            except TypeError as exc:
                if "variant" in str(exc):
                    return await self._make_session(client, m, self.sessions)
                raise

        results = await asyncio.gather(
            *(_call_make(model) for model in self.members),
            return_exceptions=True,
        )
        for model, result in zip(self.members, results):
            if isinstance(result, Exception):
                print(f"[council] could not open session for {model}: {result}")
            else:
                created.append(result)
        return created

    async def _make_session(
        self,
        client: httpx.AsyncClient,
        model: str,
        store: Dict[str, Any],
        variant: Optional[str] = None,
    ) -> str:
        from .hybrid_client import HybridCouncilSession
        session = HybridCouncilSession(
            model, client, agent=COUNCIL_AGENT or None, variant=variant
        )
        await session.create()
        store[model] = session
        return model

    async def _close_all(self) -> None:
        everything = list(self.sessions.values())
        if self.chair_session:
            everything.append(self.chair_session)
        await asyncio.gather(
            *(s.close() for s in everything), return_exceptions=True
        )
        self.sessions.clear()
        self.chair_session = None

    # -- asking ------------------------------------------------------------

    async def _ask_all(
        self,
        models: List[str],
        build_prompt,
    ) -> Dict[str, Dict[str, Any]]:
        """Run one prompt across the live sessions in parallel."""

        async def run(model: str) -> Tuple[str, Optional[Dict[str, Any]]]:
            session = self.sessions.get(model)
            if not session:
                return model, None
            try:
                return model, await session.ask(build_prompt(model))
            except Exception as exc:
                print(f"[council] {model} failed: {exc}")
                return model, {
                    "text": "", "reasoning": "", "toolCalls": [],
                    "error": str(exc), "finish": "error",
                    "cost": 0, "tokens": {}, "model": model,
                }

        results = await asyncio.gather(*(run(m) for m in models))
        return {model: result for model, result in results if result is not None}

    @staticmethod
    def _as_entry(model: str, result: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "model": model,
            "response": result.get("text", ""),
            "reasoning": result.get("reasoning", ""),
            "toolCalls": result.get("toolCalls", []),
            "tokens": result.get("tokens", {}),
            "cost": result.get("cost", 0),
            "finish": result.get("finish"),
            "error": result.get("error"),
        }

    # -- the pipeline ------------------------------------------------------

    async def run(self) -> Dict[str, Any]:
        """
        Execute all four stages and return the full result.

        On any failure that is not model-specific, all sessions are still
        cleaned up before the error propagates.
        """
        self.result = await self.run_stream(None)
        return self.result

    async def run_stream(
        self,
        queue: Optional[asyncio.Queue] = None,
    ) -> Dict[str, Any]:
        """
        Execute all four stages, optionally emitting progress as it goes.

        `queue` receives ("positions"|"debate_round"|"review"|"aggregate"|
        "verdict", payload) tuples so a streaming HTTP handler can forward them
        to the browser as they finish, and always ends with a (None, None)
        sentinel - including when the run raises, so a consumer reading the
        queue can never block forever.
        """
        self._stream_queue = queue

        async def emit(kind: str, payload: Any) -> None:
            if queue is not None:
                await queue.put((kind, payload))
                # Yield so the consumer is actually scheduled before the next
                # stage starts. Without this the pipeline runs ahead of its
                # reader - an HTTP handler cannot apply a mid-run setting change
                # between two rounds, because the loop never gets the chance.
                await asyncio.sleep(0)

        for g in self.injected_guidance:
            await emit("human_guidance_injected", g)

        try:
            async with httpx.AsyncClient(timeout=PER_MODEL_TIMEOUT) as client:
                try:
                    live = await self._open_sessions(client)
                    if not live:
                        return self._empty_result(
                            "Could not open any council sessions. Is opencode running?"
                        )
                    await emit("roster", {"members": live, "chairman": self.chairman})
                    result = await self._pipeline(client, live, emit)
                finally:
                    # Must happen INSIDE the `async with`. Closing a session
                    # needs the client, and a client that has already left its
                    # context manager rejects every request - so doing this in
                    # an outer finally leaks every council session into the
                    # user's opencode session list.
                    await self._close_all()

            self.result = result
            return result
        finally:
            if queue is not None:
                await queue.put((None, None))

    async def _pipeline(
        self,
        client: httpx.AsyncClient,
        live: List[str],
        emit=None,
    ) -> Dict[str, Any]:
        if emit is None:
            async def emit(kind: str, payload: Any) -> None:
                return

        # -- Stage 1: positions ------------------------------------------
        self.active_members = list(live)
        positions = self._as_entries(
            self.active_members,
            await self._ask_all(
                self.active_members, lambda m: prompts.position_prompt(self.user_query, m)
            ),
        )

        # Evict any models that failed or returned blank in Stage 1
        for p in list(positions):
            self._record_model_tokens(p["model"], p.get("tokens") or {})
            error = p.get("error")
            resp = (p.get("response") or "").strip()
            tool_calls = p.get("toolCalls") or []
            if error or (not resp and not tool_calls):
                await self._evict(
                    p["model"],
                    stage="positions",
                    round_num=None,
                    reason=error or "Model returned empty position",
                    emit=emit,
                )

        await self._check_budget_limits(round_num=None, emit=emit)
        await emit("positions", positions)

        # If nobody produced a position there is nothing to debate or review.
        # Bail out rather than running three more stages on empty text.
        evicted_ids = {e["model"] for e in self.evicted_members}
        valid_positions = [
            p for p in positions
            if p.get("response") and p["model"] not in evicted_ids
        ]
        if not valid_positions:
            reasons = [e["reason"] for e in self.evicted_members]
            detail = reasons[0] if reasons else "no model returned any text"
            return self._empty_result(
                f"Every council member failed to produce a position ({detail})."
            )

        self._ensure_active_chairman()

        # -- Stage 2: debate ---------------------------------------------
        # The compression mode is read fresh at the top of every round, so
        # flipping the toggle while a run is in progress takes effect from the
        # next round rather than the next run.
        debate_rounds: List[Dict[str, Any]] = []
        modes_used: List[str] = []
        settings.reset_run_modes()

        for round_number in range(1, self.rounds + 1):
            should_stop, reason = await self._check_debate_stopping_conditions(
                round_number, emit=emit
            )
            if should_stop:
                print(f"[council] Stopping debate early at round {round_number}: {reason}")
                break

            level = settings.get_debate_mode()
            instruction = caveman_mod.build_instruction(level)
            compressed = instruction is not None
            limit = MAX_QUOTE_CHARS_COMPRESSED if compressed else MAX_QUOTE_CHARS

            modes_used.append(level)
            settings.record_stage_mode(f"debate:{round_number}", level)
            print(f"[council] round {round_number}: caveman level={level}")

            # A compressed round argues from the research already done, so cut
            # the web tools off. This is a real saving, not a prompt request:
            # otherwise models re-run searches every round.
            if compressed:
                await self._tighten(self.active_members, allow_research=False)

            positions_text = _positions_block(positions, limit)
            prior = _debate_block(debate_rounds, limit)

            current_round_members = list(self.active_members)
            results = await self._ask_all(
                current_round_members,
                lambda m, rn=round_number, pt=positions_text, pr=prior, ins=instruction, g=list(self.injected_guidance): (
                    prompts.debate_prompt(
                        self.user_query, m, pt, pr, rn, self.rounds,
                        caveman_instruction=ins,
                        human_guidance=g,
                    )
                ),
            )

            statements = self._as_entries(current_round_members, results)
            # Evict models that failed or returned blank in this debate round
            for stmt in list(statements):
                self._record_model_tokens(stmt["model"], stmt.get("tokens") or {})
                error = stmt.get("error")
                resp = (stmt.get("response") or "").strip()
                if error or not resp:
                    await self._evict(
                        stmt["model"],
                        stage="debate",
                        round_num=round_number,
                        reason=error or "Model returned empty debate statement",
                        emit=emit,
                    )

            await self._check_budget_limits(round_num=round_number, emit=emit)

            round_entry = {
                "round": round_number,
                "cavemanLevel": level,
                "compressed": compressed,
                "statements": statements,
                "tokens": _sum_tokens(statements),
            }
            debate_rounds.append(round_entry)
            await emit("debate_round", round_entry)

            self._ensure_active_chairman()

            # Restore research for a following uncompressed round.
            if compressed and round_number < self.rounds:
                next_level = settings.get_debate_mode()
                if caveman_mod.build_instruction(next_level) is None:
                    await self._tighten(self.active_members, allow_research=True)

        # -- Stage 3: blind review ---------------------------------------
        reviews: List[Dict[str, Any]] = []
        aggregate: List[Dict[str, Any]] = []
        label_to_model = {
            f"Response {_label(i)}": position["model"]
            for i, position in enumerate(positions)
            if position.get("response")
        }

        if len(self.active_members) >= 2 and len(label_to_model) >= 2:
            review_level = settings.get_debate_mode()
            review_instruction = caveman_mod.build_instruction(review_level)
            modes_used.append(review_level)
            settings.record_stage_mode("review", review_level)
            print(f"[council] review: caveman level={review_level}")

            review_limit = (
                MAX_QUOTE_CHARS_COMPRESSED if review_instruction else MAX_QUOTE_CHARS
            )
            anonymous_block = "\n\n".join(
                f"{label}:\n{_clip(position['response'], review_limit)}"
                for label, position in zip(label_to_model.keys(), positions)
                if position.get("response")
            )

            current_review_members = list(self.active_members)
            review_results = await self._ask_all(
                current_review_members,
                lambda m: prompts.review_prompt(
                    self.user_query, anonymous_block, label_to_model,
                    caveman_instruction=review_instruction,
                ),
            )

            for model, result in review_results.items():
                tokens = result.get("tokens", {})
                self._record_model_tokens(model, tokens)
                error = result.get("error")
                text = result.get("text", "")
                if error:
                    await self._evict(model, "review", None, error, emit)
                reviews.append({
                    "model": model,
                    "ranking": text,
                    "parsed_ranking": parse_ranking_from_text(text),
                    "toolCalls": result.get("toolCalls", []),
                    "tokens": tokens,
                    "error": result.get("error"),
                })
            review_entry = {
                "reviews": reviews,
                "cavemanLevel": review_level,
                "tokens": _sum_tokens(reviews),
            }
            await emit("review", review_entry)

            aggregate = calculate_aggregate_rankings(reviews, label_to_model)
            await emit("aggregate", aggregate)
        else:
            print(f"[council] Skipping peer review: active members={len(self.active_members)}")

        # -- Stage 4: chairman verdict ----------------------------------
        compressed_modes = [m for m in modes_used if m != "off"]
        self._ensure_active_chairman()

        verdict_entry = await self._run_chairman(
            client, positions, debate_rounds, reviews, aggregate, label_to_model,
            debate_was_compressed=bool(compressed_modes),
            compression_modes=", ".join(dict.fromkeys(compressed_modes)),
            human_guidance=list(self.injected_guidance),
        )
        self._record_model_tokens(verdict_entry.get("model"), verdict_entry.get("tokens") or {})
        await emit("verdict", verdict_entry)

        return {
            "positions": positions,
            "debate": debate_rounds,
            "review": reviews,
            "aggregate": aggregate,
            "verdict": verdict_entry,
            "metadata": {
                "label_to_model": label_to_model,
                "aggregate_rankings": aggregate,
                "rounds": self.rounds,
                "members": live,
                "active_members": self.active_members,
                "evicted_members": self.evicted_members,
                "retired_members": self.retired_members,
                "requested_members": self.members,
                "chairman": verdict_entry.get("model"),
                "injected_guidance": list(self.injected_guidance),
                "budget": {
                    "token_cap_per_model": self.token_cap_per_model,
                    "token_budget_total": self.token_budget_total,
                    "time_limit_seconds": self.time_limit_seconds,
                    "model_tokens": self.model_tokens,
                    "total_tokens": self.total_tokens,
                    "elapsed_seconds": round(time.monotonic() - self.start_time, 2),
                },
                "caveman": self._compression_report(
                    positions, debate_rounds, reviews, verdict_entry, modes_used
                ),
            },
        }


    # -- compression bookkeeping -------------------------------------------

    async def _tighten(self, models: List[str], allow_research: bool) -> None:
        """Re-scope every member's permissions, ignoring individual failures."""
        rules = council_permissions(allow_research=allow_research)

        async def apply(model: str) -> None:
            session = self.sessions.get(model)
            if session and session.session_id:
                try:
                    await session.set_permissions(rules)
                except Exception as exc:
                    print(f"[council] permission update failed for {model}: {exc}")

        await asyncio.gather(*(apply(m) for m in models), return_exceptions=True)

    @staticmethod
    def _compression_report(
        positions: List[Dict[str, Any]],
        debate_rounds: List[Dict[str, Any]],
        reviews: List[Dict[str, Any]],
        verdict: Dict[str, Any],
        modes_used: List[str],
    ) -> Dict[str, Any]:
        """
        Token totals per stage, so the toggle's effect is visible rather than
        promised. These are the provider-reported numbers opencode returns.
        """
        stages = {
            "positions": {
                "label": "Positions",
                "mode": "full",
                "tokens": _sum_tokens(positions),
            },
            "debate": {
                "label": "Debate",
                "mode": ", ".join(dict.fromkeys(modes_used)) or "off",
                "tokens": _sum_tokens(
                    [s for r in debate_rounds for s in r.get("statements", [])]
                ),
            },
            "review": {
                "label": "Blind review",
                "mode": modes_used[-1] if modes_used else "off",
                "tokens": _sum_tokens(reviews),
            },
            "verdict": {
                "label": "Verdict",
                "mode": "full",
                "tokens": _sum_tokens([verdict]) if verdict else {
                    "input": 0, "output": 0, "reasoning": 0, "total": 0,
                },
            },
        }
        return {
            "stages": stages,
            "total": sum(s["tokens"]["total"] for s in stages.values()),
            "installed": caveman_mod.is_installed(),
        }

    def _as_entries(
        self,
        models: List[str],
        results: Dict[str, Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        return [
            self._as_entry(model, results[model])
            for model in models
            if model in results
        ]

    async def _run_chairman(
        self,
        client: httpx.AsyncClient,
        positions: List[Dict[str, Any]],
        debate_rounds: List[Dict[str, Any]],
        reviews: List[Dict[str, Any]],
        aggregate: List[Dict[str, Any]],
        label_to_model: Dict[str, str],
        debate_was_compressed: bool = False,
        compression_modes: str = "",
        human_guidance: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Ask the chairman for the final decision.

        Always uncompressed, whatever the debate used: this is the report a
        human reads, and Caveman's own rules put third-party-facing prose
        outside the compressed register.
        """
        limit = (
            MAX_QUOTE_CHARS_COMPRESSED
            if debate_was_compressed else MAX_QUOTE_CHARS
        )
        positions_text = _positions_block(positions, limit)
        debate_text = _debate_block(debate_rounds, limit)
        review_text = _review_block(reviews)
        aggregate_text = _aggregate_block(aggregate)

        # Re-attach real names to the peer scores so the chairman can weigh
        # who is credible rather than just averaging numbers.
        review_with_names = []
        for review in reviews:
            named = [
                f"{label_to_model.get(label, label)} (rank {rank})"
                for rank, label in enumerate(review.get("parsed_ranking") or [], 1)
            ]
            review_with_names.append(
                f"[{review['model']}] ranked: "
                + (", ".join(named) if named else "(ranking could not be parsed)")
            )
        review_text = "\n".join(review_with_names) or "(no peer reviews returned)"

        prompt = prompts.verdict_prompt(
            self.user_query,
            positions_text,
            debate_text,
            review_text,
            aggregate_text,
            self.chairman,
            debate_was_compressed=debate_was_compressed,
            compression_modes=compression_modes,
            human_guidance=human_guidance,
        )

        # Reuse the chairman's own session if it is also a council member.
        if self.chairman in self.sessions:
            session = self.sessions[self.chairman]
        else:
            from .hybrid_client import HybridCouncilSession
            session = HybridCouncilSession(self.chairman, client, agent=COUNCIL_AGENT or None)
            await session.create()
            self.chair_session = session

        try:
            result = await session.ask(prompt)
        except Exception as exc:
            print(f"[council] chairman {self.chairman} failed: {exc}")
            return {
                "model": self.chairman,
                "response": "",
                "sections": {},
                "error": str(exc),
            }

        text = result.get("text", "")
        return {
            "model": self.chairman,
            "response": text,
            "sections": prompts.parse_verdict(text),
            "toolCalls": result.get("toolCalls", []),
            "tokens": result.get("tokens", {}),
            "cost": result.get("cost", 0),
            "error": result.get("error"),
        }

    def _empty_result(self, message: str) -> Dict[str, Any]:
        return {
            "positions": [],
            "debate": [],
            "review": [],
            "aggregate": [],
            "verdict": {"model": "error", "response": message, "sections": {}},
            "metadata": {
                "label_to_model": {},
                "aggregate_rankings": [],
                "rounds": self.rounds,
                "members": [],
                "requested_members": self.members,
                "chairman": self.chairman,
            },
        }


# --------------------------------------------------------------------------
# Convenience entry points
# --------------------------------------------------------------------------

async def run_full_council(
    user_query: str,
    members: Optional[List[str]] = None,
    chairman: Optional[str] = None,
    rounds: Optional[int] = None,
    token_cap_per_model: Optional[int] = None,
    token_budget_total: Optional[int] = None,
    time_limit_seconds: Optional[float] = None,
    model_thinking: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Resolve the roster, then run the full four-stage council."""
    selected, chair = await resolve_roster(members, chairman)
    run = CouncilRun(
        user_query,
        selected,
        chair,
        rounds,
        token_cap_per_model=token_cap_per_model,
        token_budget_total=token_budget_total,
        time_limit_seconds=time_limit_seconds,
        model_thinking=model_thinking,
    )
    return await run.run()


async def generate_conversation_title(user_query: str) -> str:
    """Short title for a conversation, using the fastest available model."""
    try:
        models = await list_models()
    except Exception:
        return "New Conversation"

    if not models:
        return "New Conversation"

    # Prefer a small-context model; titles are a trivial task.
    model = min(models, key=lambda m: (m.get("context") or 0))

    async with httpx.AsyncClient(timeout=60.0) as client:
        session = CouncilSession(model["id"], client, agent=COUNCIL_AGENT or None)
        try:
            await session.create()
            result = await session.ask(prompts.title_prompt(user_query), timeout=45.0)
        except Exception:
            return "New Conversation"
        finally:
            await session.close()

    title = (result.get("text") or "").strip().strip("\"'")
    title = " ".join(title.split())
    if not title:
        return "New Conversation"
    return title[:50] + "..." if len(title) > 50 else title
