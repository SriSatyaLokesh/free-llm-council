# CLAUDE.md - Technical Notes for LLM Council

Architecture decisions and implementation details for future sessions. This
project drives the **local opencode server** — it never calls a model provider
API directly and holds no provider credentials.

## Project overview

A four-stage multi-agent council. Members research with live web tools, debate
each other by name, score each other anonymously, and a chairman returns a
decision with tradeoffs and dissent.

## Transport: why opencode sessions

The obvious approach — a single completion call per model — **does not work**.
`POST /api/experimental/generate` returns:

```
503 {"_tag":"ServiceUnavailableError",
     "message":"Error from provider (Console): OpenCode's free tier can only be
                used from within OpenCode"}
```

The working path is session-based, which routes through opencode's normal agent
loop (and as a bonus gives every member the full toolbelt):

```
POST /api/session                       {title, model:{providerID,id}, agent, permissions}
POST /api/session/{id}/prompt           {text}  -> returns immediately (inbox item)
POST /api/experimental/session/{id}/wait {}     -> blocks until the agent loop is idle
GET  /api/session/{id}/message          ?type=assistant&order=asc
DELETE /api/session/{id}
```

**One session per member, reused for every stage.** By the time a member reaches
the debate it still has its own position and its own previous turns in context.
This is what makes the exchange a debate rather than disconnected prompts. It
also avoids re-paying context cost each round.

`_message_cursor` tracks how many assistant messages have been consumed, so each
`ask()` returns only what that prompt produced.

## Backend structure

**`opencode_client.py`** — everything that talks to opencode.
- `get_server_url()` — `OPENCODE_SERVER_URL`, else parse `opencode service
  status`, else `http://127.0.0.1:4096`
- `get_server_password()` — env, else `~/.config/opencode/service.json`
  (also checks `%APPDATA%/opencode` and `XDG_CONFIG_HOME`)
- `list_models()` — `GET /api/model`; the roster is **never hardcoded**
- `CouncilSession` — `create()`, `ask()`, `close()`, plus the permission watchdog
- `ask_many()` — parallel fan-out; owns and closes its sessions when not given any
- Every call is scoped with `?location[directory]=<workspace>`

All opencode endpoints wrap payloads in `{"data": ...}`. `opencode_request()`
unwraps it; `CouncilSession` reads `.json()["data"]` directly.

**`council.py`** — orchestration.
- `CouncilRun` owns all sessions and guarantees cleanup in a `finally`
- `run()` returns the result; `run_stream(queue)` additionally emits
  `positions` / `debate_round` / `review` / `aggregate` / `verdict` as they land
- `resolve_roster()` — defaults to every available model; chairman defaults to
  the largest context window, preferring a model already on the council
- `parse_ranking_from_text()` and `calculate_aggregate_rankings()` are carried
  over unchanged from the original 3-stage implementation

**`prompts.py`** — all four stage prompts plus `parse_verdict()`. The member
persona lives here as `COUNCIL_MEMBER_PREAMBLE` and is prepended to every prompt.

**`caveman.py`** — loads the official Caveman skill and builds per-level
instructions (see "Caveman compression" below).

**`settings.py`** — process-global live settings, deliberately not per-request so
the user can change them mid-run. `CouncilRun` reads them at the top of each
round, so a toggle applies from the next round. Assigning one value in a
module-level dict is atomic under the GIL, so no lock is needed.

**`main.py`** — FastAPI. `GET /api/models`, plus the streaming
`POST /api/conversations/{id}/message/stream` which forwards each stage to the
browser as it completes.

**`storage.py`** — persists the whole run under a `council` key, and also writes
`stage1`/`stage2`/`stage3` aliases so pre-existing conversations still render.

Backend runs on **port 8001**, frontend on **5173**.

## Sandbox

Two independent layers:

1. Members run under the built-in **`plan`** agent, which is read-only by design.
2. `council_permissions()` is passed on every `session.create`:
   - allow: `webfetch`, `websearch`, `read`, `grep`, `glob`, `list`
   - deny: `edit`, `bash`, `task`, `lsp`, `external_directory`, `todowrite`, `question`

Notes that cost time to discover:

- opencode has **no `write` or `patch` permission action**. All filesystem
  mutation goes through `edit`.
- Denying `task` matters: otherwise a member could spawn a subagent and escape
  the ruleset.
- `_deny_pending_permissions()` polls `/api/permission/request` once a second
  during `ask()` and replies `reject` to anything raised for that session, so an
  unanticipated permission request can never hang a run.

### Custom agents do not work from a project config

An agent declared in the repo's `opencode.json` **registers and appears in
`GET /api/agent`, but produces no output at all** — the prompt is accepted, the
wait returns, and zero assistant messages come back. Verified on opencode
2.0.18 with a minimal `{"mode":"primary"}` agent, with and without `prompt` and
`permission`. The identical agent in `~/.config/opencode/opencode.json` works
fine. Hence the built-in `plan` agent plus a session-level ruleset.

If you ever revisit this, re-test with a project-level agent before assuming the
workaround is still required.

## Prompt design

**Debate is named, scoring is blind.** Anonymity is a *scoring* device — it stops
reviewers favouring a known model. It is useless in a debate, where members need
to address each other. So stages 1, 2 and 4 use real names and stage 3 re-labels
positions as `Response A/B/C`.

The stage 3 prompt states which labels are valid and pins the exact
`FINAL RANKING:` format, because the ranking is parsed by regex. A reviewer that
ignores the format contributes nothing to the aggregate, and the UI says so
rather than silently dropping it.

The stage 4 prompt requires five `##` headings (`Decision`, `Reasoning`,
`Tradeoffs`, `Dissent`, `Confidence`); `parse_verdict()` splits on them and
falls back to showing the whole response unparsed if they are missing. The
chairman is told explicitly that the aggregate scores are *evidence, not a
verdict*, so it does not just parrot the ranking.

`MAX_QUOTE_CHARS` (12000) clips each member's text before it is quoted into the
next stage's prompt, so one verbose member cannot blow out another's context.

## Caveman compression

Stages 2 and 3 are model-to-model traffic, so they can be compressed. Stages 1
and 4 cannot: the opening positions are read in the UI, and the verdict is the
human-facing report.

### It is the upstream implementation, not a local imitation

Rules come from the official
[Caveman](https://github.com/JuliusBrussee/caveman) skill, installed with its own
installer and read from disk at runtime:

```bash
npx skills add JuliusBrussee/caveman -g -y --agent '*'
```

`caveman.py` locates the installed `SKILL.md`, parses its `## Rules`,
`## Intensity`, `## Auto-Clarity` and `## Boundaries` sections, and composes them
with a short council-specific output contract. It never restates Caveman's rules,
so an upstream upgrade changes behaviour with no code edit. The installed file
was verified byte-identical to upstream `main`.

Level names are Caveman's: `off`, `lite`, `full`, `ultra`. The `wenyan-*`
variants exist upstream and are listed in `caveman.status()` as unsupported,
because the council reasons in English.

Two things are ours, and both are additive rather than replacements:

- the **output contract** (rebut a named peer, concede what moved you, lead with
  `UPDATING`/`DEFENDING`, raise the missed tradeoff) — identical whether
  compressed or not, so the level cannot change what a round is asked to do
- the **tool suppression** below, which upstream has no concept of

Caveman's own "never drop not/never/no/only/except" rule is doing real work here:
it is what stops a compressed turn from inverting an argument. That is why the
contract re-states it.

### Tool suppression is enforced, not requested

A compressed round calls `session.set_permissions(council_permissions(
allow_research=False))`, which adds `execute` to the denied set.

`execute` matters: with only `webfetch`/`websearch` denied, models route around
the restriction and fetch pages through `execute` instead. Denying it is what
actually stops the spending.

**Do not add `"shell"` to any permission ruleset.** It is not a real permission
action, and a ruleset containing it makes opencode fail the entire session with
`outcome: "failed"` — even for a prompt that uses no tools. Found by bisection on
opencode 2.0.18; `execute`, `run` and `sh` are all safe.

### Why not the proxy or the middleware

Caveman also ships a **proxy** (shrinks what the model reads) and a
**middleware** (wraps provider calls in your own code). Neither applies:

- the middleware needs this app to make the provider call, but the council goes
  through opencode sessions, so it never does
- the proxy would compress web research, which is the largest single token cost
  in stage 1 — but it works by wrapping opencode itself (`caveman opencode`),
  which is a separate and much larger change

Upstream is explicit that the skill "affects generated prose. It does not
compress request context", so the quoted transcript in each round's prompt is
not directly shrunk by the level. It shortens indirectly, because the turns being
quoted get shorter. Upstream's own skill-only figure for agentic work is ~8.5%
fewer output tokens; the per-stage counts in the verdict panel are the number to
trust for this council.

### Measuring it

```bash
python -m backend.verify_caveman            # 3 runs per level, plus a full council
python -m backend.verify_caveman --quick    # 1 run per level, noisy
```

Part 1 sends an identical debate prompt at every level, repeated, and reports
the **median with the range**. A single sample is not enough: on these small
free models one run swings several hundred tokens, and an early single-sample
run here had `full` come out *longer* than the uncompressed baseline. The script
prints a `NOTE:` when a level loses, rather than quietly reporting the levels
that flattered the idea.

Part 2 runs a full council and flips the level between rounds, then asserts
round 1 ran `off`, round 2 ran `ultra`, the verdict is still a full report
(measured on the whole response, not on the `## Decision` section — a crisp
decision is supposed to be short), and no sessions leaked.

Two bugs this test caught, both of which would have shipped silently:

- `run_stream` only sent its `(None, None)` sentinel from a wrapper in
  `main.py`, so any other consumer of the queue blocked forever. The sentinel is
  now emitted by `run_stream` itself, including on error.
- `emit()` did not yield after `queue.put()`, so the pipeline ran ahead of its
  reader and a mid-run settings change could never land between two rounds. It
  now does `await asyncio.sleep(0)`, which is what makes the "flip it while it
  runs" promise actually true.

### What the numbers looked like

Median of 3 runs per level, `opencode/big-pickle`, byte-identical debate prompt:

| level | median output | range | vs off |
|---|---|---|---|
| off | 695 | 505–1063 | baseline |
| lite | 472 | 432–852 | −32% |
| full | 363 | 254–366 | −48% |
| ultra | 397 | 282–3158 | −43% |

The level is **not monotonic**: `full` and `ultra` are effectively tied, and
`ultra` had a 3158-token outlier where the model ignored compression entirely.
More importantly, the uncompressed baseline alone spanned 505–1063 on an
identical prompt. Any single run here is noise; the median is the smallest
honest unit.

Upstream's own rigorous measurement for the skill alone in agentic coding work
is ~8.5% fewer output tokens. The per-stage counts in the verdict panel are the
authority for this council — do not quote a headline percentage from this table
as if it were a guarantee.

## Frontend

Rebuilt on a token-based design system derived from the
[`ui-ux-pro-max`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) database
(install to `~/.agents/skills`; its `scripts/search.py` runs standalone against
its CSVs and needs no project access).

**`styles/tokens.css`** is the only file allowed to contain a hex literal. Every
colour, size, duration and easing is a custom property; the previous build had
228 raw hex values spread across 8 stylesheets.

Direction, and the database hit behind each choice:

| Decision | Source |
|---|---|
| Minimalism & Swiss: radius 0, no shadows, no gradients | `--domain style "ai-native interface minimal swiss"` |
| Dark Mode (OLED) slate + run-green | `--design-system "...dark dense console" --density 8 --motion 4` |
| JetBrains Mono + IBM Plex Sans | `--domain typography "developer technical monospace variable"` |
| 68ch measure on prose | `--domain ux` line-length rule (65-75ch) |
| `prefers-reduced-motion` block | `--domain ux`, Severity High |
| linear easing on spinners only | `--domain ux` easing rule |

**The database's own palette failed contrast** and was corrected:
`--color-border` `#475569` is 2.07:1 on card and `--color-destructive` `#EF4444`
is 4.16:1. Replaced with `#6B7A94` (3.61:1) and `#F87171` (5.66:1). Body text is
17.06:1. If you touch the palette, re-run the ratio check — the source values are
not safe on a dark surface.

**Structure is verdict-led.** `RunRail` → `VerdictHero` → `ProcessPanel`. The
verdict is the page; the three working stages collapse into one disclosure.
Previously all four stages were equal-weight tabs, so the deliverable got the
same space as the process. `Council.jsx` and `Stage4.jsx` were removed;
`ProcessPanel` and `VerdictHero` replaced them, and the stage components are
reused unchanged inside.

`RunRail` exists because the skill's UX rules flag "loading spinner for 10s+"
as an anti-pattern and a run takes minutes. It shows stage, per-model progress,
elapsed time and the active compression level, and is an `aria-live="polite"`
region.

`DebateMode.jsx` POSTs to the server rather than only setting local state — that
is what makes a mid-run level change take effect.

Icons are inline SVG in `components/icons.jsx`, not a package, to stay inside
the no-new-dependencies constraint while satisfying the "no glyphs as icons"
checklist item.

## Common gotchas

1. **Module imports** — run the backend as `python -m backend.main` from the repo
   root, never from inside `backend/`.
2. **Auth is required on every call** — an unauthenticated request returns 401,
   which surfaces as an empty result rather than an error. `CouncilSession`
   attaches `_auth_headers()` to each request.
3. **Absolute URLs** — `CouncilSession` builds `f"{self._base}{path}"`; a bare
   `/api/...` path makes httpx raise `UnsupportedProtocol`.
4. **Model ids are `provider/model`** — `Model.Ref` needs `{providerID, id}`
   separately. A bare string is rejected with a 400.
5. **Config reload is asynchronous** — after editing `opencode.json`, the agent
   list lags. `POST /api/location/reload` then wait a couple of seconds.
6. **Rosters drift** — `resolve_roster()` silently drops requested models that
   opencode no longer offers; the UI surfaces the dropped ids.
7. **Session location must be set in the request BODY.** The
   `?location[directory]=` query parameter is accepted on every endpoint but is
   **ignored when creating a session**, leaving the session scoped to whatever
   directory the opencode server was started in. On this machine that is
   `C:\Users\SatyaK`, so the council could not read the repo it was being asked
   about — while appearing to work fine. `CouncilSession.create()` therefore
   passes `location: {"directory": ...}` in the body. Verify with
   `GET /api/session/{id}` and check `location.directory`.
8. **Empty response does not mean empty answer.** A failed agent loop reports
   `outcome: "failed"` on `GET /api/session/{id}`, with zero tokens and zero
   assistant messages. `_collect_new_messages()` checks that flag and sets an
   `error` rather than returning a blank that looks like a real answer.
9. **Token totals must be summed, not taken from the last message.** A prompt
   that uses tools emits several assistant messages, each a real billed call.
   Keeping only the last understates exactly the uncompressed runs being
   compared against, which flatters compression. opencode also returns no
   `total` field, so it is computed as input + output + reasoning. Cache reads
   are excluded on purpose: they are cheaper than fresh input and would flatter
   the compressed stages.

## Verification

```bash
python -m backend.verify_opencode   # discovery, roster, agent, webfetch, write-blocked
python -m backend.verify_api        # full HTTP + SSE event sequence
```

`verify_opencode` step 5 is the safety gate: it asks a council model to create
`backend/.council_canary.txt` and fails if the file exists afterwards.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
