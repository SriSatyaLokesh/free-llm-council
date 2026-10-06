# Graph Report - llm-council  (2026-10-06)

## Corpus Check
- 101 files · ~59,029 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 19 file(s) not represented in the graph (top: .css 14, (none) 4, .lock 1)

## Summary
- 995 nodes · 1804 edges · 78 communities (69 shown, 9 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 118 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `92e1fccb`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- storage.py
- CouncilSession
- icons.jsx
- HybridCouncilSession
- caveman.py
- package.json
- test_caveman_max.py
- pytest
- CLAUDE.md - Technical Notes for LLM Council
- test_chairman_selection.py
- CouncilRun
- test_human_steering.py
- council.py
- test_token_budgeting.py
- backend/main.py
- test_opencode_discovery.py
- Technical Strategy
- BaseModel
- opencode_client.py
- OpenCode Standards & Transport Architecture
- test_thinking_quality_and_deduplication.py
- backend/__init__.py
- get_server_password
- Detailed Phases
- verify_caveman.py
- delete_conversation
- run_full_council
- LLM Council
- update_settings
- post_settings
- get_server_url
- start.sh
- tests/__init__.py
- llm-council
- send_message
- What We Build: The OpenCode-Native Council
- Definition of Done
- 1. Core Architectural Laws
- LLM Council Validation Framework (SDD + TDD)
- test_ui_controls_telemetry.py
- get_active_run
- list_models
- Technical Strategy
- settings.py
- Functional Scope
- Functional Scope
- Functional Scope
- Definition of Done
- Definition of Done
- Definition of Done
- SendMessageRequest
- Technical Strategy
- Phase 2 Requirements — Dynamic Member Fault-Tolerance & Eviction
- Phase 3 Requirements — Token & Time Budgeting Engine
- Any
- Phase 4 Requirements — Intelligent Chairman Selection Matrix
- Phase 5 Requirements — Caveman Max Mode & Debate Compression
- Phase 7 Requirements — UI Controls, Eviction Badges & Budget Telemetry
- Definition of Done
- Definition of Done
- Definition of Done
- Definition of Done
- Definition of Done
- Backend structure
- graphify.js
- Phase 7 Plan — UI Controls, Eviction Badges & Budget Telemetry
- Definition of Done
- React + Vite
- Phase 2 Plan — Dynamic Member Fault-Tolerance & Eviction
- ._tighten
- send_message_stream
- AGENTS.md
- rules/graphify.md
- workflows/graphify.md
- create_project
- reconcile_council_preset

## God Nodes (most connected - your core abstractions)
1. `CouncilRun` - 67 edges
2. `CouncilSession` - 33 edges
3. `list_models()` - 19 edges
4. `get_conversation()` - 19 edges
5. `Sidebar()` - 19 edges
6. `HybridCouncilSession` - 17 edges
7. `shortModel()` - 17 edges
8. `get_server_url()` - 16 edges
9. `react` - 15 edges
10. `select_best_chairman()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `2. Diagnostics Endpoint Responds` --references--> `status()`  [INFERRED]
  specs/issues/001-opencode-discovery-resilience/validation.md → backend/caveman.py
- `Scope` --references--> `CouncilRun`  [INFERRED]
  specs/issues/002-model-fault-tolerance-eviction/requirements.md → backend/council.py
- `1. Active Run Registry` --references--> `CouncilRun`  [INFERRED]
  specs/issues/011-human-in-the-loop-debate-steering/plan.md → backend/council.py
- `3. API Endpoint` --references--> `CouncilRun`  [INFERRED]
  specs/issues/011-human-in-the-loop-debate-steering/plan.md → backend/council.py
- `2. Deliberation Context Injection` --references--> `CouncilRun`  [INFERRED]
  specs/issues/011-human-in-the-loop-debate-steering/requirements.md → backend/council.py

## Import Cycles
- None detected.

## Communities (78 total, 9 thin omitted)

### Community 0 - "storage.py"
Cohesion: 0.05
Nodes (79): export_conversation_report(), export_conversation_zip_archive(), Update a project name or description., Update conversation metadata such as title or assigned project folder., Export a council deliberation as a formatted Markdown report document., Export the entire council discussion as a downloadable ZIP package containing…, update_conversation(), update_project() (+71 more)

### Community 1 - "CouncilSession"
Cohesion: 0.18
Nodes (11): CouncilSession, One opencode session driven by one council member. The session is reused across…, Create the underlying opencode session., Delete the opencode session so it does not clutter the user's list., Replace this session's permission ruleset mid-run. Used to tighten the sandbox…, Send a prompt and wait for the agent loop to finish. Returns {text, reasoning,…, Read the session's own outcome flag. opencode reports a failed agent loop as…, Stop a runaway agent loop so the session does not keep burning tokens. (+3 more)

### Community 2 - "icons.jsx"
Cohesion: 0.09
Nodes (52): Frontend, api, App(), ChatInterface(), DebateMode(), LEVEL_LABELS, AlertTriangle(), Archive() (+44 more)

### Community 3 - "HybridCouncilSession"
Cohesion: 0.05
Nodes (44): HybridCouncilSession, list_unified_models(), Any, AsyncClient, Hybrid Council transport and unified model registry. Seamlessly combines local…, Return all available models across local OpenCode and configured external…, Unified session wrapper routing to either local OpenCode daemon or direct…, get_provider_keys() (+36 more)

### Community 4 - "caveman.py"
Cohesion: 0.20
Nodes (15): build_instruction(), intensity_for(), is_installed(), load_skill(), Path, Official Caveman compression, loaded at runtime from the installed skill.…, Return the text under '## <heading>', up to the next '## '., Pull one level's row out of Caveman's own Intensity table. Keeping this parsed… (+7 more)

### Community 5 - "package.json"
Cohesion: 0.06
Nodes (35): allowScripts, esbuild@0.25.12, dependencies, react, react-dom, react-markdown, devDependencies, eslint (+27 more)

### Community 6 - "test_caveman_max.py"
Cohesion: 0.18
Nodes (10): asyncio, Real, non-mocked tests for Phase 5: Caveman Max Mode & Debate Compression.…, Functional test: When debateMode is 'max', CouncilRun marks…, Ensure 'max' is recognized as a first-class debate compression level., Verify that build_instruction('max') emits the ultra-dense claim-and-evidence…, HTTP integration test: FastAPI POST /api/settings accepts debateMode='max'., test_build_instruction_max_structure_and_contract(), test_caveman_levels_includes_max() (+2 more)

### Community 7 - "pytest"
Cohesion: 0.17
Nodes (14): pytest, make_mock_session(), asyncio, Unit tests for Phase 2: Dynamic Member Fault-Tolerance & Model Eviction., If a model succeeds in Stage 1 but crashes in Debate Round 1, it must be…, Create a mock CouncilSession that records ask() calls and session lifecycle., If the designated chairman fails during deliberation, the council must promote…, When run_stream is used, an eviction should emit a 'model_evicted' event. (+6 more)

### Community 8 - "CLAUDE.md - Technical Notes for LLM Council"
Cohesion: 0.05
Nodes (37): debate_prompt(), parse_verdict(), position_prompt(), Prompts for the four council stages. Kept in one place so the wording of each…, Stage 3: blind, anonymized scoring of the positions., Stage 4: the chairman's decision. Never compressed - a human reads this., Stage 1: independent first opinion. Never compressed - a human reads this., Split a chairman response into its sections. Falls back to putting everything… (+29 more)

### Community 9 - "test_chairman_selection.py"
Cohesion: 0.09
Nodes (28): Any, Select the highest capability model ID from a list of model dicts or model IDs., Compute an intelligence score (0 to 100+) for a given model dict or model ID…, score_model_capability(), select_best_chairman(), Work out who sits on the council and who chairs it. Defaults to every model…, resolve_roster(), default_chairman() (+20 more)

### Community 10 - "CouncilRun"
Cohesion: 0.11
Nodes (14): CouncilRun, emit(), One council deliberation, owning every session it creates., Check if any active model has exceeded token_cap_per_model. If exceeded, retire…, Determine if the debate loop should terminate early due to: 1. Total token…, Evict a failing or depleted model immediately and ensure it is never called…, If current chairman is evicted or inactive, fail over to the next highest-…, Run one prompt across the live sessions in parallel. (+6 more)

### Community 11 - "test_human_steering.py"
Cohesion: 0.17
Nodes (13): Register an ongoing CouncilRun by conversation ID., Unregister an ongoing CouncilRun by conversation ID., register_active_run(), unregister_active_run(), asyncio, Unit and integration tests for Phase 11: Human-in-the-Loop Mid-Debate Steering…, Verify active run registration and steering injection on CouncilRun., Verify that steering injected into a CouncilRun appears in debate prompt, queue… (+5 more)

### Community 12 - "council.py"
Cohesion: 0.16
Nodes (17): _aggregate_block(), calculate_aggregate_rankings(), _clip(), _debate_block(), _label(), _positions_block(), Any, Four-stage LLM Council orchestration. Stage 1 Positions - every member answers… (+9 more)

### Community 13 - "test_token_budgeting.py"
Cohesion: 0.09
Nodes (22): 1. Automated Budgeting Tests Pass, 2. Full Regression Suite Passes, 3. Early Termination Verification, 4. Human-in-the-Loop Sign-Off, Definition of Done, Phase 3 Validation — Token & Time Budgeting Engine, asyncio, Real, non-mocked tests for Phase 3: Token & Time Budgeting Engine. Tests verify… (+14 more)

### Community 14 - "backend/main.py"
Cohesion: 0.11
Nodes (22): get_conversation(), get_models(), get_project(), health(), list_conversations(), list_projects(), FastAPI backend for LLM Council., Health check endpoint. (+14 more)

### Community 15 - "test_opencode_discovery.py"
Cohesion: 0.11
Nodes (17): Live test script executing an end-to-end deliberation across real OpenCode…, httpx, json, asyncio, Unit tests for OpenCode discovery, port resilience, and health diagnostics., OPENCODE_SERVER_URL env var should override all detection., Dynamic port from 'opencode service status' should be extracted cleanly., Password should be resolved from service.json candidate directories. (+9 more)

### Community 16 - "Technical Strategy"
Cohesion: 0.22
Nodes (7): Inject human operator guidance and resources into the ongoing deliberation., 1. Active Run Registry, 3. API Endpoint, 4. Frontend UI, 5. Verification, Phase 11 Implementation Plan — Human-in-the-Loop Mid-Debate Steering & Resource Injection, Technical Strategy

### Community 17 - "BaseModel"
Cohesion: 0.15
Nodes (13): ConversationMetadata, create_conversation(), CreateConversationRequest, ProviderKeyUpdate, Payload to configure or remove a provider API key., Create a new conversation., Request to create a new conversation., Request to update a project. (+5 more)

### Community 18 - "opencode_client.py"
Cohesion: 0.13
Nodes (18): asyncio, Configuration for the LLM Council. The council runs entirely on models that are…, prune_empty_conversations(), Prune all empty abandoned conversations (0 messages)., Client for the local opencode server. This module replaces the old OpenRouter…, main(), post(), End-to-end test of the HTTP API, including the SSE streaming path. Creates a… (+10 more)

### Community 19 - "OpenCode Standards & Transport Architecture"
Cohesion: 0.10
Nodes (19): 1. What is OpenCode?, 2. Server Discovery & Authentication, 3. Model Fetching & Schema, 4. Transport: Why Sessions and Not Completions, 5. Critical Transport Discoveries & Edge Cases, 6. How Current Code Changed vs Original Karpathy Implementation, A. Server URL Resolution, A. Workspace Directory Scoping (Body vs Query Parameter) (+11 more)

### Community 20 - "test_thinking_quality_and_deduplication.py"
Cohesion: 0.16
Nodes (13): asyncio, Unit tests for Phase 8: Per-Model Thinking Quality & Model Deduplication., Verify distinct models like ling 3.1 and ling 3.0 fin are not collapsed to the…, Verify CouncilRun defaults the Chairman to max thinking and regular members to…, Verify user overrides for thinking quality are honored over defaults., Verify list_models includes variants list and deduplicates identical IDs., Verify CouncilSession includes variant in the model specification object., test_council_run_defaults_chairman_to_max_thinking() (+5 more)

### Community 21 - "backend/__init__.py"
Cohesion: 0.20
Nodes (8): LLM Council backend package., io, Tests for conversation ID exposure, markdown report export, and zip bundle…, Verify markdown generator produces structured sections., Verify in-memory zip archive packages report.md, conversation.json, and…, test_export_conversation_zip_archive(), test_format_conversation_markdown_structure(), zipfile

### Community 22 - "get_server_password"
Cohesion: 0.16
Nodes (13): get_server_password(), OpencodeUnavailable, Path, Raised when the local opencode server cannot be reached., Possible locations of opencode's service.json., Resolve the opencode server password. Order: OPENCODE_SERVER_PASSWORD env var,…, _service_config_candidates(), RuntimeError (+5 more)

### Community 23 - "Detailed Phases"
Cohesion: 0.12
Nodes (15): Detailed Phases, LLM Council Phased Implementation Roadmap, Phase 10: Projects & Workspace Folder Hierarchy, Phase 11: Human-in-the-Loop Mid-Debate Steering & Resource Injection, Phase 1: OpenCode Server Discovery & Port Resilience, Phase 2: Dynamic Member Fault-Tolerance & Eviction Engine, Phase 3: Token & Time Budgeting Engine, Phase 4: Intelligent Chairman Capability Matrix (+7 more)

### Community 24 - "verify_caveman.py"
Cohesion: 0.26
Nodes (11): council_permissions(), Build the permission ruleset for council members. Allow the research and read…, council_sessions(), main(), _median(), one_shot(), part_one(), part_two() (+3 more)

### Community 25 - "delete_conversation"
Cohesion: 0.40
Nodes (5): delete_conversation(), delete_project(), Delete a project folder and revert its debates to independent mode., Delete a conversation by ID., delete

### Community 26 - "run_full_council"
Cohesion: 0.22
Nodes (7): _call_make(), AsyncClient, Resolve the roster, then run the full four-stage council., Determine thinking quality / reasoning effort per model: - Honored if…, Create one session per member with resolved thinking quality. Returns the…, run_full_council(), Step 2: Backend Implementation (Green Code)

### Community 27 - "LLM Council"
Cohesion: 0.14
Nodes (13): 1. opencode, 2. Backend, 3. Frontend, Caveman compression, Configuration, Cost and time, Honest limits, How a run works (+5 more)

### Community 28 - "update_settings"
Cohesion: 0.25
Nodes (8): get_settings(), Current council settings, plus whether the official Caveman skill is installed.…, get_debate_mode(), get_settings(), Apply a partial update. Unknown keys and bad values are ignored., update_settings(), Verify backend.settings accepts and returns 'max' debate mode., test_settings_module_accepts_max_mode()

### Community 29 - "post_settings"
Cohesion: 0.22
Nodes (8): post_settings(), Change live council settings. Takes effect on the next debate round., Live settings the user can change while a run is in flight., SettingsUpdate, Phase 3 Plan — Token & Time Budgeting Engine, Step 1: Red Test, Step 2: Green Implementation, Step 3: Refactor & Verification

### Community 30 - "get_server_url"
Cohesion: 0.14
Nodes (17): _auth_headers(), diagnose_connection(), get_server_url(), _location_params(), opencode_request(), AsyncClient, Resolve the opencode server base URL. Order: OPENCODE_SERVER_URL env var,…, Every opencode call is scoped to the council's workspace directory. (+9 more)

### Community 36 - "send_message"
Cohesion: 0.39
Nodes (8): Send a message and run the full four-stage council. Returns the complete…, send_message(), get_time_limit_seconds(), get_token_budget_total(), get_token_cap_per_model(), Any, Verify /api/settings handles both retrieval and updates for debate mode and…, test_settings_api_supports_budget_controls()

### Community 37 - "What We Build: The OpenCode-Native Council"
Cohesion: 0.15
Nodes (12): 1. Zero-Cost, Auto-Discovered Roster, 2. Dynamic Fault Tolerance & Model Eviction, 3. Dual-Layer Token & Time Governance, 4. Intelligent Benchmark-Ranked Decider Selection, 5. Caveman Ultra & Max Inter-Model Compression, 6. Sandboxed Toolbelt, LLM Council Mission, Mission Statement (+4 more)

### Community 38 - "Definition of Done"
Cohesion: 0.29
Nodes (6): 1. Automated Tests Pass, 2. Diagnostics Endpoint Responds, 3. Clear Diagnostics on Stopped Server, 4. Human-in-the-Loop Sign-Off, Definition of Done, Phase 1 Validation — OpenCode Discovery & Port Resilience

### Community 39 - "1. Core Architectural Laws"
Cohesion: 0.18
Nodes (10): 1. Core Architectural Laws, 2. Technical Stack & Conventions, 3. The Issue Development Protocol, Law 1: Zero External Cost Guarantee (OpenCode-First), Law 2: Spec-Driven & Test-Driven Development (SDD & TDD), Law 3: Member Isolation & Fault Tolerance, Law 4: Strict Sandbox & Workspace Protection, Law 5: Hard Token & Time Governance (+2 more)

### Community 40 - "LLM Council Validation Framework (SDD + TDD)"
Cohesion: 0.20
Nodes (9): 1. The Red-Green-Refactor Lifecycle, 2. Test Classification & Architecture, 3. Human-in-the-Loop (HITL) Verification Protocol, 4. Definition of Done (DoD) Checklist, Checkpoints:, Layer A: Unit & Orchestration Tests (Deterministic, Fast, Mocks), Layer B: OpenCode Contract Tests (Transport & Protocol), Layer C: Live Integration & Verification Scripts (Real Environment) (+1 more)

### Community 41 - "test_ui_controls_telemetry.py"
Cohesion: 0.27
Nodes (8): asyncio, Unit and integration tests for Phase 7: UI Controls, Eviction Badges & Budget…, Verify CouncilRun captures evicted_models, retired_models, and emits early…, Verify /api/health provides all fields required by the frontend Sidebar health…, Verify /api/providers/keys endpoints support modal interactions: list, update,…, test_council_session_budget_and_eviction_telemetry(), test_health_api_contract_matches_frontend(), test_provider_keys_api_integration()

### Community 42 - "get_active_run"
Cohesion: 0.33
Nodes (6): get_active_run(), Retrieve the active CouncilRun for a conversation ID, if any., Inject human operator guidance and resources into an ongoing deliberation., Request to inject human operator guidance into an ongoing debate., steer_conversation(), SteerRequest

### Community 43 - "list_models"
Cohesion: 0.22
Nodes (8): generate_conversation_title(), Short title for a conversation, using the fastest available model., list_models(), Fetch the models available inside opencode. This is the council roster -…, Phase 8 Plan — Per-Model Thinking Quality & Model Deduplication, Step 1: Red Tests (TDD), Step 3: Frontend Implementation, Step 4: Verification

### Community 44 - "Technical Strategy"
Cohesion: 0.22
Nodes (8): Conversation, Full conversation with all messages., 1. Storage Architecture, 2. Backend API, 3. Frontend Implementation, 4. Verification, Phase 10 Implementation Plan — Projects & Workspace Folder Hierarchy, Technical Strategy

### Community 45 - "settings.py"
Cohesion: 0.20
Nodes (6): Intelligent capability scoring matrix for LLM Council Chairman election. Ranks…, Live, mutable council settings. These are deliberately process-global rather…, Note which mode a stage ran in., record_stage_mode(), re, typing

### Community 46 - "Functional Scope"
Cohesion: 0.25
Nodes (7): 1. Discard Empty / Abandoned Conversations, 2. Persist Settings Preset in Model Selection Panel, 3. Model Auto-Reconciliation, Acceptance Criteria, Functional Scope, Phase 9 Requirements — Clean Conversation Lifecycle & Persisted Presets, User Story

### Community 47 - "Functional Scope"
Cohesion: 0.25
Nodes (7): 1. Project & Workspace Data Model, 2. Backend Project Management Endpoints, 3. Frontend UI Hierarchy (Antigravity Workspace Style), Acceptance Criteria, Functional Scope, Phase 10 Requirements — Projects & Workspace Folder Hierarchy, User Story

### Community 48 - "Functional Scope"
Cohesion: 0.25
Nodes (7): 1. Mid-Debate Steering Input Interface, 2. Deliberation Context Injection, 3. API & Streaming Hand-off, Acceptance Criteria, Functional Scope, Phase 11 Requirements — Human-in-the-Loop Mid-Debate Steering & Resource Injection, User Story

### Community 49 - "Definition of Done"
Cohesion: 0.29
Nodes (6): 1. Automated Eviction Test Passes, 2. Full Regression Suite Passes, 3. Verification of Event Stream, 4. Human-in-the-Loop Sign-Off, Definition of Done, Phase 2 Validation — Dynamic Member Fault-Tolerance & Eviction

### Community 50 - "Definition of Done"
Cohesion: 0.29
Nodes (6): 1. Automated Instruction Test Passes, 2. Full Regression Suite Passes, 3. Token Compression Verification, 4. Human-in-the-Loop Sign-Off, Definition of Done, Phase 5 Validation — Caveman Max Mode & Debate Compression

### Community 51 - "Definition of Done"
Cohesion: 0.29
Nodes (6): 1. Automated Hybrid Provider Tests Pass, 2. Full Regression Suite Passes, 3. Key Ingestion and Model Discovery Verification, 4. Human-in-the-Loop Sign-Off, Definition of Done, Phase 6 Validation — Hybrid Provider & Custom API Key Ingestion

### Community 52 - "SendMessageRequest"
Cohesion: 0.22
Nodes (8): Request to send a message in a conversation., SendMessageRequest, 1. Model Deduplication & Roster Hygiene, 2. Per-Model Thinking Quality Configuration, Acceptance Criteria, Phase 8 Requirements — Per-Model Thinking Quality & Model Deduplication, Scope, User Story

### Community 53 - "Technical Strategy"
Cohesion: 0.29
Nodes (6): 1. Backend: Empty Conversation Pruning & Delete Endpoint, 2. Frontend: Lazy Conversation Lifecycle, 3. Frontend & Backend: Persisted Council Presets, 4. TDD Verification, Phase 9 Implementation Plan — Clean Conversation Lifecycle & Persisted Presets, Technical Strategy

### Community 54 - "Phase 2 Requirements — Dynamic Member Fault-Tolerance & Eviction"
Cohesion: 0.33
Nodes (5): Acceptance Criteria, Out of Scope, Phase 2 Requirements — Dynamic Member Fault-Tolerance & Eviction, Scope, User Story

### Community 55 - "Phase 3 Requirements — Token & Time Budgeting Engine"
Cohesion: 0.33
Nodes (5): Acceptance Criteria, Out of Scope, Phase 3 Requirements — Token & Time Budgeting Engine, Scope, User Story

### Community 56 - "Any"
Cohesion: 0.33
Nodes (5): ask_many(), _parse_assistant_message(), Any, Flatten an opencode assistant message into text / reasoning / tool calls., Run one prompt across many models in parallel. If `sessions` is given, those…

### Community 57 - "Phase 4 Requirements — Intelligent Chairman Selection Matrix"
Cohesion: 0.33
Nodes (5): Acceptance Criteria, Out of Scope, Phase 4 Requirements — Intelligent Chairman Selection Matrix, Scope, User Story

### Community 58 - "Phase 5 Requirements — Caveman Max Mode & Debate Compression"
Cohesion: 0.33
Nodes (5): Acceptance Criteria, Out of Scope, Phase 5 Requirements — Caveman Max Mode & Debate Compression, Scope, User Story

### Community 59 - "Phase 7 Requirements — UI Controls, Eviction Badges & Budget Telemetry"
Cohesion: 0.33
Nodes (5): Acceptance Criteria, Out of Scope, Phase 7 Requirements — UI Controls, Eviction Badges & Budget Telemetry, Scope, User Story

### Community 60 - "Definition of Done"
Cohesion: 0.33
Nodes (5): 1. Frontend Build Verification, 2. Live API & UI Contract Verification, 3. Human-in-the-Loop Sign-Off, Definition of Done, Phase 7 Validation — UI Controls, Eviction Badges & Budget Telemetry

### Community 61 - "Definition of Done"
Cohesion: 0.33
Nodes (5): 1. Automated Test Suite, 2. Frontend Build Verification, 3. Functional Verification Checkpoints, Definition of Done, Phase 8 Validation — Per-Model Thinking Quality & Model Deduplication

### Community 62 - "Definition of Done"
Cohesion: 0.33
Nodes (5): 1. Automated Test Suite, 2. Frontend Build Verification, 3. Functional Verification Checkpoints, Definition of Done, Phase 9 Validation — Clean Conversation Lifecycle & Persisted Presets

### Community 63 - "Definition of Done"
Cohesion: 0.33
Nodes (5): 1. Automated Test Suite, 2. Frontend Build Verification, 3. Functional Verification Checkpoints, Definition of Done, Phase 10 Validation — Projects & Workspace Folder Hierarchy

### Community 64 - "Definition of Done"
Cohesion: 0.33
Nodes (5): 1. Automated Test Suite, 2. Frontend Build Verification, 3. Functional Verification Checkpoints, Definition of Done, Phase 11 Validation — Human-in-the-Loop Mid-Debate Steering & Resource Injection

### Community 65 - "Backend structure"
Cohesion: 0.67
Nodes (3): parse_ranking_from_text(), Extract the ordered labels from a 'FINAL RANKING:' block., Backend structure

### Community 66 - "graphify.js"
Cohesion: 0.40
Nodes (3): IMPORTANT: keep the reminder string free of backticks and $(...) constructs., ref_fs, ref_path

### Community 67 - "Phase 7 Plan — UI Controls, Eviction Badges & Budget Telemetry"
Cohesion: 0.40
Nodes (4): Phase 7 Plan — UI Controls, Eviction Badges & Budget Telemetry, Step 1: Frontend API Client Extension, Step 2: Component Updates, Step 3: Verification

### Community 68 - "Definition of Done"
Cohesion: 0.33
Nodes (5): 1. Automated Ranking Tests Pass, 2. Full Regression Suite Passes, 4. Human-in-the-Loop Sign-Off, Definition of Done, Phase 4 Validation — Intelligent Chairman Selection Matrix

### Community 69 - "React + Vite"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

### Community 70 - "Phase 2 Plan — Dynamic Member Fault-Tolerance & Eviction"
Cohesion: 0.50
Nodes (3): Phase 2 Plan — Dynamic Member Fault-Tolerance & Eviction, Step 1: Red Test, Step 3: Refactor & Regression Test

### Community 72 - "send_message_stream"
Cohesion: 0.50
Nodes (4): Send a message and stream the council as it runs. Emits Server-Sent Events as…, send_message_stream(), emit(), event_generator()

### Community 76 - "create_project"
Cohesion: 0.50
Nodes (4): create_project(), CreateProjectRequest, Create a new project workspace folder., Request to create a new project workspace folder.

### Community 77 - "reconcile_council_preset"
Cohesion: 0.50
Nodes (4): Reconciles a saved council preset against currently available OpenCode models.…, reconcile_council_preset(), Verify preset reconciliation logic: If a saved model is missing from OpenCode,…, test_preset_auto_reconciliation()

## Knowledge Gaps
- **193 isolated node(s):** `name`, `private`, `version`, `type`, `dev` (+188 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 513 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CouncilRun` connect `CouncilRun` to `CouncilSession`, `HybridCouncilSession`, `test_caveman_max.py`, `pytest`, `test_chairman_selection.py`, `test_human_steering.py`, `council.py`, `test_token_budgeting.py`, `backend/main.py`, `Technical Strategy`, `test_thinking_quality_and_deduplication.py`, `Detailed Phases`, `verify_caveman.py`, `run_full_council`, `test_ui_controls_telemetry.py`, `list_models`, `Functional Scope`, `Phase 2 Requirements — Dynamic Member Fault-Tolerance & Eviction`, `Backend structure`, `._tighten`, `send_message_stream`?**
  _High betweenness centrality (0.278) - this node is a cross-community bridge._
- **Why does `CouncilSession` connect `CouncilSession` to `Backend structure`, `HybridCouncilSession`, `LLM Council Validation Framework (SDD + TDD)`, `CouncilRun`, `list_models`, `council.py`, `opencode_client.py`, `SendMessageRequest`, `test_thinking_quality_and_deduplication.py`, `Detailed Phases`, `Any`, `verify_caveman.py`, `get_server_url`?**
  _High betweenness centrality (0.129) - this node is a cross-community bridge._
- **Why does `shortModel()` connect `icons.jsx` to `list_models`, `SendMessageRequest`, `Detailed Phases`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `CouncilRun` (e.g. with `HybridCouncilSession` and `CouncilSession`) actually correct?**
  _`CouncilRun` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `CouncilSession` (e.g. with `CouncilRun` and `HybridCouncilSession`) actually correct?**
  _`CouncilSession` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `list_models()` (e.g. with `Backend structure` and `Step 1: Red Tests (TDD)`) actually correct?**
  _`list_models()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _193 weakly-connected nodes found - possible documentation gaps or missing edges._