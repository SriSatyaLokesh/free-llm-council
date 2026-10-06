# Graph Report - llm-council  (2026-10-06)

## Corpus Check
- 101 files · ~58,879 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 19 file(s) not represented in the graph (top: .css 14, (none) 4, .lock 1)

## Summary
- 1000 nodes · 1809 edges · 85 communities (76 shown, 9 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 118 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a1ddabc1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- storage.py
- CouncilSession
- icons.jsx
- provider_keys.py
- caveman.py
- package.json
- test_caveman_max.py
- test_opencode_discovery.py
- CLAUDE.md - Technical Notes for LLM Council
- test_chairman_selection.py
- CouncilRun
- test_human_steering.py
- council.py
- test_token_budgeting.py
- backend/main.py
- create_conversation
- Technical Strategy
- BaseModel
- opencode_client.py
- OpenCode Standards & Transport Architecture
- get_conversation
- test_exports_and_conversation_id.py
- get_server_password
- Detailed Phases
- verify_caveman.py
- delete_conversation
- run_full_council
- LLM Council Pro Max
- HybridCouncilSession
- send_message_stream
- get_server_url
- start.sh
- tests/__init__.py
- llm-council
- test_hybrid_providers.py
- What We Build: The OpenCode-Native Council
- Definition of Done
- 1. Core Architectural Laws
- LLM Council Validation Framework (SDD + TDD)
- settings.py
- get_active_run
- list_models
- Technical Strategy
- build_instruction
- Functional Scope
- Functional Scope
- Functional Scope
- Definition of Done
- Definition of Done
- Definition of Done
- 1. Model Deduplication & Roster Hygiene
- Technical Strategy
- Phase 2 Requirements — Dynamic Member Fault-Tolerance & Eviction
- Phase 3 Requirements — Token & Time Budgeting Engine
- debate_prompt
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
- post
- AGENTS.md
- rules/graphify.md
- workflows/graphify.md
- create_project
- test_projects_and_folders.py
- prompts.py
- list_unified_models
- Phase 6 Requirements — Hybrid Provider & Custom API Key Ingestion
- config.py
- post_settings
- Phase 5 Plan — Caveman Max Mode & Debate Compression
- update_project

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

## Communities (85 total, 9 thin omitted)

### Community 0 - "storage.py"
Cohesion: 0.18
Nodes (22): create_project(), delete_project(), ensure_data_dir(), get_project(), get_projects_file(), list_projects(), load_all_projects(), prune_empty_conversations() (+14 more)

### Community 1 - "CouncilSession"
Cohesion: 0.16
Nodes (14): CouncilSession, _parse_assistant_message(), Any, Flatten an opencode assistant message into text / reasoning / tool calls., One opencode session driven by one council member. The session is reused across…, Create the underlying opencode session., Delete the opencode session so it does not clutter the user's list., Replace this session's permission ruleset mid-run. Used to tighten the sandbox… (+6 more)

### Community 2 - "icons.jsx"
Cohesion: 0.09
Nodes (52): Frontend, api, App(), ChatInterface(), DebateMode(), LEVEL_LABELS, AlertTriangle(), Archive() (+44 more)

### Community 3 - "provider_keys.py"
Cohesion: 0.15
Nodes (16): post_provider_key(), Update or remove a provider API key dynamically., delete_key(), get_key(), get_key_statuses(), Any, Secure in-memory and environment-backed provider API key management. Supports…, Retrieve the raw secret key for a provider. (+8 more)

### Community 4 - "caveman.py"
Cohesion: 0.20
Nodes (12): Intelligent capability scoring matrix for LLM Council Chairman election. Ranks…, is_installed(), load_skill(), Path, Official Caveman compression, loaded at runtime from the installed skill.…, What the UI needs to render the mode picker honestly., Read the installed SKILL.md, cached against the file's mtime. Returns None when…, skill_path() (+4 more)

### Community 5 - "package.json"
Cohesion: 0.06
Nodes (35): allowScripts, esbuild@0.25.12, dependencies, react, react-dom, react-markdown, devDependencies, eslint (+27 more)

### Community 6 - "test_caveman_max.py"
Cohesion: 0.22
Nodes (8): asyncio, Real, non-mocked tests for Phase 5: Caveman Max Mode & Debate Compression.…, Functional test: When debateMode is 'max', CouncilRun marks…, Ensure 'max' is recognized as a first-class debate compression level., HTTP integration test: FastAPI POST /api/settings accepts debateMode='max'., test_caveman_levels_includes_max(), test_council_run_records_max_caveman_mode(), test_settings_api_accepts_max_mode()

### Community 7 - "test_opencode_discovery.py"
Cohesion: 0.06
Nodes (41): pytest, make_mock_session(), asyncio, Unit tests for Phase 2: Dynamic Member Fault-Tolerance & Model Eviction., If a model succeeds in Stage 1 but crashes in Debate Round 1, it must be…, Create a mock CouncilSession that records ask() calls and session lifecycle., If the designated chairman fails during deliberation, the council must promote…, When run_stream is used, an eviction should emit a 'model_evicted' event. (+33 more)

### Community 8 - "CLAUDE.md - Technical Notes for LLM Council"
Cohesion: 0.12
Nodes (15): parse_verdict(), Split a chairman response into its sections. Falls back to putting everything…, Caveman compression, CLAUDE.md - Technical Notes for LLM Council, Custom agents do not work from a project config, graphify, Measuring it, Project overview (+7 more)

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
Cohesion: 0.08
Nodes (25): Live test script executing an end-to-end deliberation across real OpenCode…, httpx, 1. Automated Budgeting Tests Pass, 2. Full Regression Suite Passes, 3. Early Termination Verification, 4. Human-in-the-Loop Sign-Off, Definition of Done, Phase 3 Validation — Token & Time Budgeting Engine (+17 more)

### Community 14 - "backend/main.py"
Cohesion: 0.11
Nodes (22): get_conversation(), get_models(), get_project(), health(), list_conversations(), list_projects(), FastAPI backend for LLM Council., Health check endpoint. (+14 more)

### Community 15 - "create_conversation"
Cohesion: 0.14
Nodes (20): add_user_message(), create_conversation(), delete_conversation(), list_conversations(), List all conversations (metadata only). By default, empty conversations (0…, Add a user message to a conversation. Args: conversation_id: Conversation…, Create a new conversation. Args: conversation_id: Unique identifier for the…, Permanently delete a conversation from storage. Returns: True if the file was… (+12 more)

### Community 16 - "Technical Strategy"
Cohesion: 0.22
Nodes (7): Inject human operator guidance and resources into the ongoing deliberation., 1. Active Run Registry, 3. API Endpoint, 4. Frontend UI, 5. Verification, Phase 11 Implementation Plan — Human-in-the-Loop Mid-Debate Steering & Resource Injection, Technical Strategy

### Community 17 - "BaseModel"
Cohesion: 0.15
Nodes (13): ConversationMetadata, create_conversation(), CreateConversationRequest, ProviderKeyUpdate, Payload to configure or remove a provider API key., Create a new conversation., Request to create a new conversation., Request to update a project. (+5 more)

### Community 18 - "opencode_client.py"
Cohesion: 0.19
Nodes (11): asyncio, LLM Council backend package., Client for the local opencode server. This module replaces the old OpenRouter…, End-to-end test of the HTTP API, including the SSE streaming path. Creates a…, Verification script for the opencode client and the council sandbox. Run with:…, base64, pathlib, shutil (+3 more)

### Community 19 - "OpenCode Standards & Transport Architecture"
Cohesion: 0.10
Nodes (19): 1. What is OpenCode?, 2. Server Discovery & Authentication, 3. Model Fetching & Schema, 4. Transport: Why Sessions and Not Completions, 5. Critical Transport Discoveries & Edge Cases, 6. How Current Code Changed vs Original Karpathy Implementation, A. Server URL Resolution, A. Workspace Directory Scoping (Body vs Query Parameter) (+11 more)

### Community 20 - "get_conversation"
Cohesion: 0.17
Nodes (18): Update conversation metadata such as title or assigned project folder., update_conversation(), add_assistant_message(), assign_conversation_project(), get_conversation(), get_conversation_path(), Get the file path for a conversation., Add an assistant message holding a complete council run. The whole run is… (+10 more)

### Community 21 - "test_exports_and_conversation_id.py"
Cohesion: 0.12
Nodes (16): export_conversation_report(), export_conversation_zip_archive(), Export a council deliberation as a formatted Markdown report document., Export the entire council discussion as a downloadable ZIP package containing…, export_conversation_zip(), format_conversation_markdown(), Format a complete council deliberation into a clean, comprehensive Markdown…, Build an in-memory zip archive containing: - report.md (human-readable… (+8 more)

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

### Community 27 - "LLM Council Pro Max"
Cohesion: 0.11
Nodes (18): 1. Clone & Configure Remote, 1. Hybrid Local + Frontier Cloud Provider Engine, 2. Install Dependencies, 2. Workspace Organization & Project Folders, 3. Human-in-the-Loop Mid-Debate Steering, 3. Start the Platform, 4. Comprehensive Deliberation Exports, 5. Token Economics & Caveman Compression (+10 more)

### Community 28 - "HybridCouncilSession"
Cohesion: 0.15
Nodes (9): HybridCouncilSession, AsyncClient, Unified session wrapper routing to either local OpenCode daemon or direct…, get_provider_keys(), Get status and redacted preview of configured provider API keys., Phase 6 Plan — Hybrid Provider & Custom API Key Ingestion, Step 1: Red Test, Step 2: Green Implementation (+1 more)

### Community 29 - "send_message_stream"
Cohesion: 0.18
Nodes (10): Send a message and stream the council as it runs. Emits Server-Sent Events as…, Request to send a message in a conversation., send_message_stream(), emit(), event_generator(), SendMessageRequest, Phase 3 Plan — Token & Time Budgeting Engine, Step 1: Red Test (+2 more)

### Community 30 - "get_server_url"
Cohesion: 0.14
Nodes (15): ask_many(), diagnose_connection(), get_server_url(), _location_params(), opencode_request(), Resolve the opencode server base URL. Order: OPENCODE_SERVER_URL env var,…, Every opencode call is scoped to the council's workspace directory., Actively inspect the connection to the OpenCode server and return a detailed… (+7 more)

### Community 36 - "test_hybrid_providers.py"
Cohesion: 0.21
Nodes (10): asyncio, Real, non-mocked tests for Phase 6: Hybrid Provider & Custom API Key Ingestion.…, If an external keyed model fails with 401 Unauthorized (invalid key/no…, HTTP integration test: GET /api/providers/keys POST /api/providers/keys, list_unified_models() must return OpenCode models when no keys exist, and merge…, HybridCouncilSession dispatches OpenCode models to CouncilSession, and keyed…, test_hybrid_council_session_routing(), test_keyed_model_401_triggers_immediate_eviction() (+2 more)

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

### Community 41 - "settings.py"
Cohesion: 0.08
Nodes (31): get_settings(), Current council settings, plus whether the official Caveman skill is installed.…, Send a message and run the full four-stage council. Returns the complete…, send_message(), get_debate_mode(), get_settings(), get_time_limit_seconds(), get_token_budget_total() (+23 more)

### Community 42 - "get_active_run"
Cohesion: 0.33
Nodes (6): get_active_run(), Retrieve the active CouncilRun for a conversation ID, if any., Inject human operator guidance and resources into an ongoing deliberation., Request to inject human operator guidance into an ongoing debate., steer_conversation(), SteerRequest

### Community 43 - "list_models"
Cohesion: 0.22
Nodes (8): generate_conversation_title(), Short title for a conversation, using the fastest available model., list_models(), Fetch the models available inside opencode. This is the council roster -…, Phase 8 Plan — Per-Model Thinking Quality & Model Deduplication, Step 1: Red Tests (TDD), Step 3: Frontend Implementation, Step 4: Verification

### Community 44 - "Technical Strategy"
Cohesion: 0.22
Nodes (8): Conversation, Full conversation with all messages., 1. Storage Architecture, 2. Backend API, 3. Frontend Implementation, 4. Verification, Phase 10 Implementation Plan — Projects & Workspace Folder Hierarchy, Technical Strategy

### Community 45 - "build_instruction"
Cohesion: 0.22
Nodes (10): build_instruction(), intensity_for(), Return the text under '## <heading>', up to the next '## '., Pull one level's row out of Caveman's own Intensity table. Keeping this parsed…, Build the Caveman instruction for a level, or None for "off". Returns None when…, _section(), Verify that build_instruction('max') emits the ultra-dense claim-and-evidence…, Verify that debate_prompt embeds the Caveman max instruction cleanly. (+2 more)

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

### Community 52 - "1. Model Deduplication & Roster Hygiene"
Cohesion: 0.29
Nodes (6): 1. Model Deduplication & Roster Hygiene, 2. Per-Model Thinking Quality Configuration, Acceptance Criteria, Phase 8 Requirements — Per-Model Thinking Quality & Model Deduplication, Scope, User Story

### Community 53 - "Technical Strategy"
Cohesion: 0.29
Nodes (6): 1. Backend: Empty Conversation Pruning & Delete Endpoint, 2. Frontend: Lazy Conversation Lifecycle, 3. Frontend & Backend: Persisted Council Presets, 4. TDD Verification, Phase 9 Implementation Plan — Clean Conversation Lifecycle & Persisted Presets, Technical Strategy

### Community 54 - "Phase 2 Requirements — Dynamic Member Fault-Tolerance & Eviction"
Cohesion: 0.33
Nodes (5): Acceptance Criteria, Out of Scope, Phase 2 Requirements — Dynamic Member Fault-Tolerance & Eviction, Scope, User Story

### Community 55 - "Phase 3 Requirements — Token & Time Budgeting Engine"
Cohesion: 0.33
Nodes (5): Acceptance Criteria, Out of Scope, Phase 3 Requirements — Token & Time Budgeting Engine, Scope, User Story

### Community 56 - "debate_prompt"
Cohesion: 0.22
Nodes (10): debate_prompt(), Stage 4: the chairman's decision. Never compressed - a human reads this., Stage 2: named cross-examination, one round at a time. `caveman_instruction` is…, verdict_prompt(), Step 2: Green Implementation, 2. Prompting Integration, Verify that verdict_prompt alerts the chairman to expand compressed debate…, test_chairman_prompt_contains_expansion_directive_for_max() (+2 more)

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

### Community 72 - "post"
Cohesion: 0.22
Nodes (8): prune_empty_conversations(), Prune all empty abandoned conversations (0 messages)., _auth_headers(), AsyncClient, council_sessions(), main(), post(), Council sessions currently left in the user's opencode session list.

### Community 76 - "create_project"
Cohesion: 0.50
Nodes (4): create_project(), CreateProjectRequest, Create a new project workspace folder., Request to create a new project workspace folder.

### Community 77 - "test_projects_and_folders.py"
Cohesion: 0.28
Nodes (8): asyncio, Unit and integration tests for Phase 10: Projects & Workspace Folder Hierarchy., Verify creating debate directly in project, moving between projects, and…, Verify HTTP API PATCH endpoint for renaming and archiving conversations., HTTP API integration tests for /api/projects and /api/conversations/{id}., test_conversation_archive_and_rename_api(), test_create_conversation_with_project_and_move_lifecycle(), test_projects_http_api()

### Community 78 - "prompts.py"
Cohesion: 0.25
Nodes (7): position_prompt(), Prompts for the four council stages. Kept in one place so the wording of each…, Stage 3: blind, anonymized scoring of the positions., Stage 1: independent first opinion. Never compressed - a human reads this., Short conversation title., review_prompt(), title_prompt()

### Community 79 - "list_unified_models"
Cohesion: 0.33
Nodes (4): list_unified_models(), Any, Hybrid Council transport and unified model registry. Seamlessly combines local…, Return all available models across local OpenCode and configured external…

### Community 80 - "Phase 6 Requirements — Hybrid Provider & Custom API Key Ingestion"
Cohesion: 0.33
Nodes (5): Acceptance Criteria, Out of Scope, Phase 6 Requirements — Hybrid Provider & Custom API Key Ingestion, Scope, User Story

### Community 81 - "config.py"
Cohesion: 0.50
Nodes (3): Configuration for the LLM Council. The council runs entirely on models that are…, dotenv, os

### Community 82 - "post_settings"
Cohesion: 0.50
Nodes (4): post_settings(), Change live council settings. Takes effect on the next debate round., Live settings the user can change while a run is in flight., SettingsUpdate

### Community 83 - "Phase 5 Plan — Caveman Max Mode & Debate Compression"
Cohesion: 0.50
Nodes (3): Phase 5 Plan — Caveman Max Mode & Debate Compression, Step 1: Red Test, Step 3: Refactor & Verification

### Community 84 - "update_project"
Cohesion: 0.67
Nodes (3): Update a project name or description., update_project(), patch

## Knowledge Gaps
- **198 isolated node(s):** `graphify`, `Workflow: graphify`, `graphify`, `Project overview`, `Transport: why opencode sessions` (+193 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 518 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CouncilRun` connect `CouncilRun` to `CouncilSession`, `test_caveman_max.py`, `test_opencode_discovery.py`, `test_chairman_selection.py`, `test_human_steering.py`, `council.py`, `test_token_budgeting.py`, `backend/main.py`, `Technical Strategy`, `Detailed Phases`, `verify_caveman.py`, `run_full_council`, `HybridCouncilSession`, `send_message_stream`, `test_hybrid_providers.py`, `settings.py`, `list_models`, `Functional Scope`, `Phase 2 Requirements — Dynamic Member Fault-Tolerance & Eviction`, `Backend structure`, `._tighten`, `Phase 6 Requirements — Hybrid Provider & Custom API Key Ingestion`?**
  _High betweenness centrality (0.275) - this node is a cross-community bridge._
- **Why does `CouncilSession` connect `CouncilSession` to `Backend structure`, `test_opencode_discovery.py`, `post`, `LLM Council Validation Framework (SDD + TDD)`, `CouncilRun`, `list_models`, `council.py`, `list_unified_models`, `Phase 6 Requirements — Hybrid Provider & Custom API Key Ingestion`, `opencode_client.py`, `1. Model Deduplication & Roster Hygiene`, `Detailed Phases`, `verify_caveman.py`, `HybridCouncilSession`, `get_server_url`?**
  _High betweenness centrality (0.128) - this node is a cross-community bridge._
- **Why does `shortModel()` connect `icons.jsx` to `list_models`, `1. Model Deduplication & Roster Hygiene`, `Detailed Phases`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `CouncilRun` (e.g. with `HybridCouncilSession` and `CouncilSession`) actually correct?**
  _`CouncilRun` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `CouncilSession` (e.g. with `CouncilRun` and `HybridCouncilSession`) actually correct?**
  _`CouncilSession` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `list_models()` (e.g. with `Backend structure` and `Step 1: Red Tests (TDD)`) actually correct?**
  _`list_models()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify`, `Workflow: graphify`, `graphify` to the rest of the system?**
  _198 weakly-connected nodes found - possible documentation gaps or missing edges._