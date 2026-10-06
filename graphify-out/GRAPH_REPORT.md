# Graph Report - llm-council  (2026-10-06)

## Corpus Check
- 63 files · ~46,117 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 19 file(s) not represented in the graph (top: .css 14, (none) 4, .lock 1)

## Summary
- 722 nodes · 1506 edges · 49 communities (38 shown, 11 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 55 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `57e6a1fb`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- storage.py
- CouncilSession
- icons.jsx
- provider_keys.py
- test_opencode_discovery.py
- package.json
- test_thinking_quality_and_deduplication.py
- test_eviction_on_debate_round_failure
- verify_caveman.py
- test_chairman_selection.py
- CouncilRun
- test_human_steering.py
- ._pipeline
- asyncio
- backend/main.py
- create_conversation
- ._check_budget_limits
- BaseModel
- opencode_client.py
- _sum_tokens
- get_conversation
- test_exports_and_conversation_id.py
- ._ask_all
- test_model_formatting_preserves_distinct_variants
- delete_conversation
- ._open_sessions
- LLM Council Pro Max
- send_message_stream
- list_models
- start.sh
- tests/__init__.py
- llm-council
- test_hybrid_providers.py
- settings.py
- get_active_run
- council.py
- prompts.py
- graphify.js
- React + Vite
- ._tighten
- AGENTS.md
- rules/graphify.md
- workflows/graphify.md
- post
- test_projects_and_folders.py
- post_settings
- update_project

## God Nodes (most connected - your core abstractions)
1. `CouncilRun` - 57 edges
2. `CouncilSession` - 28 edges
3. `get_conversation()` - 19 edges
4. `Sidebar()` - 19 edges
5. `list_models()` - 16 edges
6. `react` - 15 edges
7. `HybridCouncilSession` - 14 edges
8. `send_message()` - 14 edges
9. `select_best_chairman()` - 13 edges
10. `create_conversation()` - 13 edges

## Surprising Connections (you probably didn't know these)
- `It is the upstream implementation, not a local imitation` --references--> `status()`  [INFERRED]
  CLAUDE.md → backend/caveman.py
- `Backend structure` --references--> `resolve_roster()`  [INFERRED]
  CLAUDE.md → backend/council.py
- `Common gotchas` --references--> `resolve_roster()`  [INFERRED]
  CLAUDE.md → backend/council.py
- `Backend structure` --references--> `parse_ranking_from_text()`  [INFERRED]
  CLAUDE.md → backend/council.py
- `Backend structure` --references--> `calculate_aggregate_rankings()`  [INFERRED]
  CLAUDE.md → backend/council.py

## Import Cycles
- None detected.

## Communities (49 total, 11 thin omitted)

### Community 0 - "storage.py"
Cohesion: 0.18
Nodes (22): create_project(), delete_project(), ensure_data_dir(), get_project(), get_projects_file(), list_projects(), load_all_projects(), prune_empty_conversations() (+14 more)

### Community 1 - "CouncilSession"
Cohesion: 0.09
Nodes (20): HybridCouncilSession, Any, AsyncClient, Unified session wrapper routing to either local OpenCode daemon or direct…, ask_many(), CouncilSession, _parse_assistant_message(), Any (+12 more)

### Community 2 - "icons.jsx"
Cohesion: 0.09
Nodes (52): Frontend, api, App(), ChatInterface(), DebateMode(), LEVEL_LABELS, AlertTriangle(), Archive() (+44 more)

### Community 3 - "provider_keys.py"
Cohesion: 0.10
Nodes (23): post_provider_key(), Update or remove a provider API key dynamically., delete_key(), get_key(), get_key_statuses(), Any, Secure in-memory and environment-backed provider API key management. Supports…, Retrieve the raw secret key for a provider. (+15 more)

### Community 4 - "test_opencode_discovery.py"
Cohesion: 0.13
Nodes (15): json, asyncio, Unit tests for OpenCode discovery, port resilience, and health diagnostics., OPENCODE_SERVER_URL env var should override all detection., Dynamic port from 'opencode service status' should be extracted cleanly., Password should be resolved from service.json candidate directories., When no service.json exists, an informative OpencodeUnavailable error is raised., If a port is open but occupied by another process (e.g. Kilo on 4096),… (+7 more)

### Community 5 - "package.json"
Cohesion: 0.06
Nodes (35): allowScripts, esbuild@0.25.12, dependencies, react, react-dom, react-markdown, devDependencies, eslint (+27 more)

### Community 6 - "test_thinking_quality_and_deduplication.py"
Cohesion: 0.24
Nodes (10): asyncio, Unit tests for Phase 8: Per-Model Thinking Quality & Model Deduplication., Verify CouncilRun defaults the Chairman to max thinking and regular members to…, Verify user overrides for thinking quality are honored over defaults., Verify list_models includes variants list and deduplicates identical IDs., Verify CouncilSession includes variant in the model specification object., test_council_run_defaults_chairman_to_max_thinking(), test_council_run_honors_user_thinking_overrides() (+2 more)

### Community 7 - "test_eviction_on_debate_round_failure"
Cohesion: 0.17
Nodes (12): make_mock_session(), asyncio, If a model succeeds in Stage 1 but crashes in Debate Round 1, it must be…, Create a mock CouncilSession that records ask() calls and session lifecycle., If the designated chairman fails during deliberation, the council must promote…, When run_stream is used, an eviction should emit a 'model_evicted' event., If a model fails in Stage 1, it must be evicted immediately and NEVER called…, test_chairman_failover_when_chairman_evicted() (+4 more)

### Community 8 - "verify_caveman.py"
Cohesion: 0.07
Nodes (37): build_instruction(), intensity_for(), is_installed(), load_skill(), Path, Official Caveman compression, loaded at runtime from the installed skill.…, Return the text under '## <heading>', up to the next '## '., Pull one level's row out of Caveman's own Intensity table. Keeping this parsed… (+29 more)

### Community 9 - "test_chairman_selection.py"
Cohesion: 0.11
Nodes (24): Any, Intelligent capability scoring matrix for LLM Council Chairman election. Ranks…, Select the highest capability model ID from a list of model dicts or model IDs., Compute an intelligence score (0 to 100+) for a given model dict or model ID…, score_model_capability(), select_best_chairman(), Work out who sits on the council and who chairs it. Defaults to every model…, resolve_roster() (+16 more)

### Community 10 - "CouncilRun"
Cohesion: 0.15
Nodes (10): CouncilRun, One council deliberation, owning every session it creates., Inject human operator guidance and resources into the ongoing deliberation., Execute all four stages and return the full result. On any failure that is not…, Execute all four stages, optionally emitting progress as it goes. `queue`…, Queue, If the initial chairman is evicted, CouncilRun._ensure_active_chairman() must…, test_council_run_chairman_failover_elects_highest_capability_survivor() (+2 more)

### Community 11 - "test_human_steering.py"
Cohesion: 0.17
Nodes (13): Register an ongoing CouncilRun by conversation ID., Unregister an ongoing CouncilRun by conversation ID., register_active_run(), unregister_active_run(), asyncio, Unit and integration tests for Phase 11: Human-in-the-Loop Mid-Debate Steering…, Verify active run registration and steering injection on CouncilRun., Verify that steering injected into a CouncilRun appears in debate prompt, queue… (+5 more)

### Community 12 - "._pipeline"
Cohesion: 0.20
Nodes (12): _aggregate_block(), calculate_aggregate_rankings(), _clip(), _debate_block(), _label(), _positions_block(), Any, Ask the chairman for the final decision. Always uncompressed, whatever the… (+4 more)

### Community 13 - "asyncio"
Cohesion: 0.17
Nodes (11): asyncio, Functional test: When cumulative tokens across all models exceed…, Real wall-clock test: When real elapsed time crosses time_limit_seconds, debate…, Integration test: In a 4-round deliberation, when the token budget is capped…, Real HTTP integration test: Verify that FastAPI /api/settings accepts and…, Functional test: When a model exceeds its token_cap_per_model, it must be…, test_council_run_retires_model_exceeding_token_cap(), test_council_run_stops_debate_when_global_budget_exhausted() (+3 more)

### Community 14 - "backend/main.py"
Cohesion: 0.11
Nodes (22): get_conversation(), get_project(), get_provider_keys(), health(), list_conversations(), list_projects(), FastAPI backend for LLM Council., Health check endpoint. (+14 more)

### Community 15 - "create_conversation"
Cohesion: 0.14
Nodes (20): add_user_message(), create_conversation(), delete_conversation(), list_conversations(), List all conversations (metadata only). By default, empty conversations (0…, Add a user message to a conversation. Args: conversation_id: Conversation…, Create a new conversation. Args: conversation_id: Unique identifier for the…, Permanently delete a conversation from storage. Returns: True if the file was… (+12 more)

### Community 16 - "._check_budget_limits"
Cohesion: 0.22
Nodes (5): emit(), Check if any active model has exceeded token_cap_per_model. If exceeded, retire…, Determine if the debate loop should terminate early due to: 1. Total token…, Evict a failing or depleted model immediately and ensure it is never called…, If current chairman is evicted or inactive, fail over to the next highest-…

### Community 17 - "BaseModel"
Cohesion: 0.18
Nodes (11): Conversation, ConversationMetadata, ProviderKeyUpdate, Full conversation with all messages., Payload to configure or remove a provider API key., Request to update a project., Request to update a conversation (project assignment, title, or archive status)., Conversation metadata for list view. (+3 more)

### Community 18 - "opencode_client.py"
Cohesion: 0.12
Nodes (18): asyncio, Configuration for the LLM Council. The council runs entirely on models that are…, LLM Council backend package., Path, Client for the local opencode server. This module replaces the old OpenRouter…, Possible locations of opencode's service.json., _service_config_candidates(), main() (+10 more)

### Community 19 - "_sum_tokens"
Cohesion: 0.33
Nodes (5): Total the token counts opencode reported for a set of entries. opencode returns…, Token totals per stage, so the toggle's effect is visible rather than promised.…, _sum_tokens(), Verify token summation logic against realistic OpenCode token telemetry: input…, test_sum_tokens_real_telemetry()

### Community 20 - "get_conversation"
Cohesion: 0.17
Nodes (18): Update conversation metadata such as title or assigned project folder., update_conversation(), add_assistant_message(), assign_conversation_project(), get_conversation(), get_conversation_path(), Get the file path for a conversation., Add an assistant message holding a complete council run. The whole run is… (+10 more)

### Community 21 - "test_exports_and_conversation_id.py"
Cohesion: 0.13
Nodes (15): export_conversation_report(), export_conversation_zip_archive(), Export a council deliberation as a formatted Markdown report document., Export the entire council discussion as a downloadable ZIP package containing…, export_conversation_zip(), format_conversation_markdown(), Format a complete council deliberation into a clean, comprehensive Markdown…, Build an in-memory zip archive containing: - report.md (human-readable… (+7 more)

### Community 25 - "delete_conversation"
Cohesion: 0.40
Nodes (5): delete_conversation(), delete_project(), Delete a project folder and revert its debates to independent mode., Delete a conversation by ID., delete

### Community 26 - "._open_sessions"
Cohesion: 0.33
Nodes (4): _call_make(), AsyncClient, Determine thinking quality / reasoning effort per model: - Honored if…, Create one session per member with resolved thinking quality. Returns the…

### Community 27 - "LLM Council Pro Max"
Cohesion: 0.11
Nodes (18): 1. Clone & Configure Remote, 1. Hybrid Local + Frontier Cloud Provider Engine, 2. Install Dependencies, 2. Workspace Organization & Project Folders, 3. Human-in-the-Loop Mid-Debate Steering, 3. Start the Platform, 4. Comprehensive Deliberation Exports, 5. Token Economics & Caveman Compression (+10 more)

### Community 29 - "send_message_stream"
Cohesion: 0.33
Nodes (6): Send a message and stream the council as it runs. Emits Server-Sent Events as…, Request to send a message in a conversation., send_message_stream(), emit(), event_generator(), SendMessageRequest

### Community 30 - "list_models"
Cohesion: 0.18
Nodes (19): _auth_headers(), diagnose_connection(), get_server_password(), get_server_url(), list_models(), _location_params(), opencode_request(), AsyncClient (+11 more)

### Community 36 - "test_hybrid_providers.py"
Cohesion: 0.14
Nodes (15): list_unified_models(), Hybrid Council transport and unified model registry. Seamlessly combines local…, Return all available models across local OpenCode and configured external…, get_models(), The council roster, read live from OpenCode and configured custom providers., OpencodeUnavailable, Raised when the local opencode server cannot be reached., pytest (+7 more)

### Community 41 - "settings.py"
Cohesion: 0.06
Nodes (41): get_settings(), Current council settings, plus whether the official Caveman skill is installed.…, Send a message and run the full four-stage council. Returns the complete…, send_message(), get_debate_mode(), get_settings(), get_time_limit_seconds(), get_token_budget_total() (+33 more)

### Community 42 - "get_active_run"
Cohesion: 0.33
Nodes (6): get_active_run(), Retrieve the active CouncilRun for a conversation ID, if any., Inject human operator guidance and resources into an ongoing deliberation., Request to inject human operator guidance into an ongoing debate., steer_conversation(), SteerRequest

### Community 43 - "council.py"
Cohesion: 0.14
Nodes (13): generate_conversation_title(), parse_ranking_from_text(), Four-stage LLM Council orchestration. Stage 1 Positions - every member answers…, Resolve the roster, then run the full four-stage council., Short title for a conversation, using the fastest available model., Extract the ordered labels from a 'FINAL RANKING:' block., run_full_council(), Live test script executing an end-to-end deliberation across real OpenCode… (+5 more)

### Community 56 - "prompts.py"
Cohesion: 0.10
Nodes (20): debate_prompt(), parse_verdict(), position_prompt(), Prompts for the four council stages. Kept in one place so the wording of each…, Stage 3: blind, anonymized scoring of the positions., Stage 4: the chairman's decision. Never compressed - a human reads this., Stage 1: independent first opinion. Never compressed - a human reads this., Split a chairman response into its sections. Falls back to putting everything… (+12 more)

### Community 66 - "graphify.js"
Cohesion: 0.40
Nodes (3): IMPORTANT: keep the reminder string free of backticks and $(...) constructs., ref_fs, ref_path

### Community 69 - "React + Vite"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

### Community 76 - "post"
Cohesion: 0.18
Nodes (11): create_conversation(), create_project(), CreateConversationRequest, CreateProjectRequest, prune_empty_conversations(), Create a new project workspace folder., Create a new conversation., Prune all empty abandoned conversations (0 messages). (+3 more)

### Community 77 - "test_projects_and_folders.py"
Cohesion: 0.28
Nodes (8): asyncio, Unit and integration tests for Phase 10: Projects & Workspace Folder Hierarchy., Verify creating debate directly in project, moving between projects, and…, Verify HTTP API PATCH endpoint for renaming and archiving conversations., HTTP API integration tests for /api/projects and /api/conversations/{id}., test_conversation_archive_and_rename_api(), test_create_conversation_with_project_and_move_lifecycle(), test_projects_http_api()

### Community 82 - "post_settings"
Cohesion: 0.50
Nodes (4): post_settings(), Change live council settings. Takes effect on the next debate round., Live settings the user can change while a run is in flight., SettingsUpdate

### Community 84 - "update_project"
Cohesion: 0.67
Nodes (3): Update a project name or description., update_project(), patch

## Knowledge Gaps
- **59 isolated node(s):** `name`, `private`, `version`, `type`, `dev` (+54 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 341 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CouncilRun` connect `CouncilRun` to `CouncilSession`, `provider_keys.py`, `test_thinking_quality_and_deduplication.py`, `test_eviction_on_debate_round_failure`, `verify_caveman.py`, `test_chairman_selection.py`, `test_human_steering.py`, `._pipeline`, `asyncio`, `backend/main.py`, `._check_budget_limits`, `_sum_tokens`, `._ask_all`, `._open_sessions`, `send_message_stream`, `list_models`, `test_hybrid_providers.py`, `settings.py`, `council.py`, `._tighten`?**
  _High betweenness centrality (0.271) - this node is a cross-community bridge._
- **Why does `CLAUDE.md - Technical Notes for LLM Council` connect `verify_caveman.py` to `prompts.py`, `CouncilSession`, `icons.jsx`, `list_models`?**
  _High betweenness centrality (0.260) - this node is a cross-community bridge._
- **Why does `Frontend` connect `icons.jsx` to `verify_caveman.py`?**
  _High betweenness centrality (0.241) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `CouncilRun` (e.g. with `HybridCouncilSession` and `CouncilSession`) actually correct?**
  _`CouncilRun` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `CouncilSession` (e.g. with `CouncilRun` and `HybridCouncilSession`) actually correct?**
  _`CouncilSession` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _59 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `CouncilSession` be split into smaller, more focused modules?**
  _Cohesion score 0.09388335704125178 - nodes in this community are weakly interconnected._