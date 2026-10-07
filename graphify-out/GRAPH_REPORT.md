# Graph Report - free-llm-council  (2026-10-07)

## Corpus Check
- 68 files · ~69,858 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 21 file(s) not represented in the graph (top: .css 15, (none) 4, .cff 1)

## Summary
- 906 nodes · 1782 edges · 70 communities (61 shown, 9 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 61 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2be03ad5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- storage.py
- CouncilSession
- icons.jsx
- council.py
- CouncilRun
- package.json
- get
- test_thinking_quality_and_deduplication.py
- caveman.py
- test_chairman_selection.py
- create_conversation
- Appendix B - Canonical Sources (read these before reinventing)
- opencode_client.py
- test_human_steering.py
- backend/main.py
- get_conversation
- test_caveman_max.py
- create_conversation
- send_message_stream
- format_conversation_detailed
- provider_keys.py
- test_token_budgeting.py
- BaseModel
- 4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)
- list_models
- verify_caveman.py
- HybridCouncilSession
- Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine
- 4. Component Standards
- get_active_run
- resolve_roster
- start.sh
- tests/__init__.py
- 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)
- test_projects_and_folders.py
- tasteskill: Anti-Slop Frontend Skill
- 9. AI TELLS (Forbidden Patterns)
- 11. REDESIGN PROTOCOL
- 3. DEFAULT ARCHITECTURE & CONVENTIONS
- settings.py
- test_opencode_discovery.py
- 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS
- post_settings
- 0. BRIEF INFERENCE (Read the Room Before Anything Else)
- 12. THE BLOCK LIBRARY (Contract - Implementations Land Here Iteratively)
- 5. CONTEXT-AWARE PROACTIVITY
- 8. DARK MODE PROTOCOL
- 7. DIAL DEFINITIONS (Technical Reference)
- httpx
- test_hybrid_providers.py
- git-workflow.md
- free-llm-council
- test_ui_controls_telemetry.py
- backend/__init__.py
- prompts.py
- debate_prompt
- post
- send_message
- ._open_sessions
- list_conversations
- post_provider_key
- reconcile_council_preset
- update_project
- graphify.js
- React + Vite
- AGENTS.md
- rules/graphify.md
- workflows/graphify.md

## God Nodes (most connected - your core abstractions)
1. `CouncilRun` - 60 edges
2. `CouncilSession` - 27 edges
3. `get_conversation()` - 22 edges
4. `Sidebar()` - 21 edges
5. `list_models()` - 16 edges
6. `react` - 16 edges
7. `tasteskill: Anti-Slop Frontend Skill` - 16 edges
8. `HybridCouncilSession` - 15 edges
9. `Appendix B - Canonical Sources (read these before reinventing)` - 15 edges
10. `send_message()` - 14 edges

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

## Communities (70 total, 9 thin omitted)

### Community 0 - "storage.py"
Cohesion: 0.16
Nodes (24): create_project(), delete_project(), ensure_data_dir(), get_project(), get_projects_file(), list_projects(), load_all_projects(), prune_empty_conversations() (+16 more)

### Community 1 - "CouncilSession"
Cohesion: 0.08
Nodes (29): AsyncClient, ask_many(), CouncilSession, _parse_assistant_message(), Any, Flatten an opencode assistant message into text / reasoning / tool calls., One opencode session driven by one council member. The session is reused across…, Create the underlying opencode session. (+21 more)

### Community 2 - "icons.jsx"
Cohesion: 0.08
Nodes (61): Frontend, B. Workspace Header & Breadcrumbs, api, App(), ChatInterface(), DebateMode(), LEVEL_LABELS, AlertTriangle() (+53 more)

### Community 3 - "council.py"
Cohesion: 0.13
Nodes (20): _aggregate_block(), calculate_aggregate_rankings(), _clip(), _debate_block(), _label(), parse_ranking_from_text(), _positions_block(), Any (+12 more)

### Community 4 - "CouncilRun"
Cohesion: 0.10
Nodes (12): CouncilRun, emit(), One council deliberation, owning every session it creates., Inject human operator guidance and resources into the ongoing deliberation., Check if any active model has exceeded token_cap_per_model. If exceeded, retire…, Determine if the debate loop should terminate early due to: 1. Total token…, Evict a failing or depleted model immediately and ensure it is never called…, If current chairman is evicted or inactive, fail over to the next highest-… (+4 more)

### Community 5 - "package.json"
Cohesion: 0.06
Nodes (36): allowScripts, esbuild@0.25.12, dependencies, react, react-dom, react-markdown, remark-gfm, devDependencies (+28 more)

### Community 6 - "get"
Cohesion: 0.12
Nodes (17): export_conversation_pdf(), export_conversation_zip_archive(), get_conversation(), get_project(), list_projects(), List all project folders with metadata and debate counts., Get details for a specific project., Get a specific conversation with all its messages. (+9 more)

### Community 7 - "test_thinking_quality_and_deduplication.py"
Cohesion: 0.09
Nodes (26): make_mock_session(), asyncio, Unit tests for Phase 2: Dynamic Member Fault-Tolerance & Model Eviction., If a model succeeds in Stage 1 but crashes in Debate Round 1, it must be…, Create a mock CouncilSession that records ask() calls and session lifecycle., If the designated chairman fails during deliberation, the council must promote…, When run_stream is used, an eviction should emit a 'model_evicted' event., If a model fails in Stage 1, it must be evicted immediately and NEVER called… (+18 more)

### Community 8 - "caveman.py"
Cohesion: 0.09
Nodes (28): Intelligent capability scoring matrix for LLM Council Chairman election. Ranks…, build_instruction(), intensity_for(), is_installed(), load_skill(), Path, Official Caveman compression, loaded at runtime from the installed skill.…, Return the text under '## <heading>', up to the next '## '. (+20 more)

### Community 9 - "test_chairman_selection.py"
Cohesion: 0.10
Nodes (25): Any, Select the highest capability model ID from a list of model dicts or model IDs., Compute an intelligence score (0 to 100+) for a given model dict or model ID…, score_model_capability(), select_best_chairman(), get_models(), The council roster, read live from OpenCode and configured custom providers.…, default_chairman() (+17 more)

### Community 10 - "create_conversation"
Cohesion: 0.13
Nodes (19): create_conversation(), delete_conversation(), get_conversation_path(), Get the file path for a conversation., Create a new conversation. Args: conversation_id: Unique identifier for the…, Permanently delete a conversation from storage. Returns: True if the file was…, asyncio, Unit tests for Phase 9: Clean Conversation Lifecycle & Persisted Council… (+11 more)

### Community 11 - "Appendix B - Canonical Sources (read these before reinventing)"
Cohesion: 0.09
Nodes (21): APPENDICES - Real Source-Backed Reference Material, Appendix A - Install Commands per Design System, Appendix B - Canonical Sources (read these before reinventing), Appendix C - Apple Liquid Glass: Honest Web Approximation, Apple Liquid Glass (Apple platforms only), Atlassian, Bootstrap, Carbon (+13 more)

### Community 12 - "opencode_client.py"
Cohesion: 0.18
Nodes (10): Configuration for the LLM Council. The council runs entirely on models that are…, Path, Client for the local opencode server. This module replaces the old OpenRouter…, Possible locations of opencode's service.json., _service_config_candidates(), base64, dotenv, os (+2 more)

### Community 13 - "test_human_steering.py"
Cohesion: 0.17
Nodes (13): Register an ongoing CouncilRun by conversation ID., Unregister an ongoing CouncilRun by conversation ID., register_active_run(), unregister_active_run(), asyncio, Unit and integration tests for Phase 11: Human-in-the-Loop Mid-Debate Steering…, Verify active run registration and steering injection on CouncilRun., Verify that steering injected into a CouncilRun appears in debate prompt, queue… (+5 more)

### Community 14 - "backend/main.py"
Cohesion: 0.14
Nodes (14): delete_conversation(), delete_project(), FastAPI backend for LLM Council., Health check endpoint., Delete a project folder and revert its debates to independent mode., Delete a conversation by ID., root(), delete (+6 more)

### Community 15 - "get_conversation"
Cohesion: 0.16
Nodes (20): Update conversation metadata such as title or assigned project folder., update_conversation(), add_assistant_message(), add_user_message(), assign_conversation_project(), get_conversation(), Add a user message to a conversation. Args: conversation_id: Conversation…, Add an assistant message holding a complete council run. The whole run is… (+12 more)

### Community 16 - "test_caveman_max.py"
Cohesion: 0.17
Nodes (11): get_debate_mode(), asyncio, Real, non-mocked tests for Phase 5: Caveman Max Mode & Debate Compression.…, Functional test: When debateMode is 'max', CouncilRun marks…, Ensure 'max' is recognized as a first-class debate compression level., Verify backend.settings accepts and returns 'max' debate mode., HTTP integration test: FastAPI POST /api/settings accepts debateMode='max'., test_caveman_levels_includes_max() (+3 more)

### Community 17 - "create_conversation"
Cohesion: 0.50
Nodes (4): create_conversation(), CreateConversationRequest, Create a new conversation., Request to create a new conversation.

### Community 18 - "send_message_stream"
Cohesion: 0.33
Nodes (6): Send a message and stream the council as it runs. Emits Server-Sent Events as…, Request to send a message in a conversation., send_message_stream(), emit(), event_generator(), SendMessageRequest

### Community 19 - "format_conversation_detailed"
Cohesion: 0.11
Nodes (24): export_conversation_html(), export_conversation_report(), get_conversation_reports(), Export a council deliberation as a formatted Markdown report document…, Export a council deliberation as a standalone publication-grade HTML report., Return pre-rendered executive and detailed reports with deliberation metadata…, _clean_table_cell(), _extract_non_reporting_models() (+16 more)

### Community 20 - "provider_keys.py"
Cohesion: 0.16
Nodes (15): get_provider_keys(), health(), Detailed health check validating connection to OpenCode and BYOK readiness., Get status and redacted preview of configured provider API keys., _get_env_key(), get_key(), get_key_statuses(), _init_from_env() (+7 more)

### Community 21 - "test_token_budgeting.py"
Cohesion: 0.14
Nodes (16): asyncio, Real, non-mocked tests for Phase 3: Token & Time Budgeting Engine. Tests verify…, Functional test: When cumulative tokens across all models exceed…, Real wall-clock test: When real elapsed time crosses time_limit_seconds, debate…, Integration test: In a 4-round deliberation, when the token budget is capped…, Real HTTP integration test: Verify that FastAPI /api/settings accepts and…, Verify token summation logic against realistic OpenCode token telemetry: input…, Verify that CouncilRun properly initializes token and time tracking structures. (+8 more)

### Community 22 - "BaseModel"
Cohesion: 0.22
Nodes (9): Conversation, ConversationMetadata, Full conversation with all messages., Request to update a project., Request to update a conversation (project assignment, title, or archive status)., Conversation metadata for list view., UpdateConversationRequest, UpdateProjectRequest (+1 more)

### Community 23 - "4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)"
Cohesion: 0.17
Nodes (12): 4.10 Quotes & Testimonials, 4.11 Page Theme Lock (Light / Dark Mode Consistency), 4.1 Typography, 4.2 Color Calibration, 4.3 Layout Diversification, 4.4 Materiality, Shadows, Cards, 4.5 Interactive UI States, 4.6 Data & Form Patterns (+4 more)

### Community 24 - "list_models"
Cohesion: 0.18
Nodes (19): _auth_headers(), diagnose_connection(), get_server_password(), get_server_url(), list_models(), _location_params(), opencode_request(), AsyncClient (+11 more)

### Community 25 - "verify_caveman.py"
Cohesion: 0.27
Nodes (10): council_permissions(), Build the permission ruleset for council members. Allow the research and read…, main(), _median(), one_shot(), part_one(), part_two(), Measures what the Caveman levels actually do, on this council. python -m… (+2 more)

### Community 26 - "HybridCouncilSession"
Cohesion: 0.22
Nodes (5): generate_conversation_title(), Short title for a conversation, using the fastest available model., HybridCouncilSession, Any, Unified session wrapper routing to either local OpenCode daemon or direct…

### Community 27 - "Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine"
Cohesion: 0.10
Nodes (20): 1. Prerequisites, 2. Start OpenCode Service, 3. Clone & Install, 4. Launch the Platform, Can I still use commercial models like Claude 3.5 Sonnet, GPT-4o, or DeepSeek R1?, Citation, Comparison: Upstream Concept vs. Free LLM Council, Configuration & BYOK Cloud Providers (+12 more)

### Community 28 - "4. Component Standards"
Cohesion: 0.17
Nodes (11): 1. Dials & Atmosphere, 2. Color Palette & Surface Elevation, 3. Typography & Micro-Hierarchy, 4. Component Standards, 5. Performance, Ergonomics & Fast Handling, A. Left-Hand Sidebar (Workspace Tree), Accents & Signal Colors, C. Live RunRail (Real-Time Progress) (+3 more)

### Community 29 - "get_active_run"
Cohesion: 0.33
Nodes (6): get_active_run(), Retrieve the active CouncilRun for a conversation ID, if any., Inject human operator guidance and resources into an ongoing deliberation., Request to inject human operator guidance into an ongoing debate., steer_conversation(), SteerRequest

### Community 30 - "resolve_roster"
Cohesion: 0.29
Nodes (7): Resolve the roster, then run the full four-stage council., Work out who sits on the council and who chairs it. Defaults to every model…, resolve_roster(), run_full_council(), OpencodeUnavailable, Raised when the local opencode server cannot be reached., RuntimeError

### Community 34 - "10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)"
Cohesion: 0.20
Nodes (10): 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know), Animation Library Choice, Cards & Containers, Galleries & Media, Hero Paradigms, Layout & Grids, Micro-Interactions & Effects, Navigation & Menus (+2 more)

### Community 36 - "test_projects_and_folders.py"
Cohesion: 0.28
Nodes (8): asyncio, Unit and integration tests for Phase 10: Projects & Workspace Folder Hierarchy., Verify creating debate directly in project, moving between projects, and…, Verify HTTP API PATCH endpoint for renaming and archiving conversations., HTTP API integration tests for /api/projects and /api/conversations/{id}., test_conversation_archive_and_rename_api(), test_create_conversation_with_project_and_move_lifecycle(), test_projects_http_api()

### Community 37 - "tasteskill: Anti-Slop Frontend Skill"
Cohesion: 0.20
Nodes (10): 13. OUT OF SCOPE, 14. FINAL PRE-FLIGHT CHECK, 1.A Dial Inference (design read → dial values), 1.B Use-Case Presets, 1.C How the Dials Drive Output, 1. THE THREE DIALS (Core Configuration), 2.A When to reach for a real design system (use official packages), 2.B When the brief is an aesthetic, not a system (+2 more)

### Community 38 - "9. AI TELLS (Forbidden Patterns)"
Cohesion: 0.25
Nodes (8): 9.A Visual & CSS, 9. AI TELLS (Forbidden Patterns), 9.B Typography, 9.C Layout & Spacing, 9.D Content & Data ("Jane Doe" Effect), 9.E External Resources & Components, 9.F Production-Test Tells (banned outright), 9.G EM-DASH BAN (the single most-violated Tell)

### Community 39 - "11. REDESIGN PROTOCOL"
Cohesion: 0.29
Nodes (7): 11.A Detect the Mode (first action), 11.B Audit Before Touching, 11.C Preservation Rules, 11.D Modernisation Levers (priority order), 11.E Decision Tree: Targeted Evolution vs Full Redesign, 11.F What Never Changes Silently, 11. REDESIGN PROTOCOL

### Community 40 - "3. DEFAULT ARCHITECTURE & CONVENTIONS"
Cohesion: 0.29
Nodes (7): 3.A Stack, 3.B State, 3.C Icons, 3.D Emoji Policy, 3. DEFAULT ARCHITECTURE & CONVENTIONS, 3.E Responsiveness & Layout Mechanics, 3.F Dependency Verification (mandatory)

### Community 41 - "settings.py"
Cohesion: 0.20
Nodes (8): get_settings(), Current council settings, plus whether the official Caveman skill is installed.…, get_settings(), Live, mutable council settings. These are deliberately process-global rather…, Apply a partial update. Unknown keys and bad values are ignored., Note which mode a stage ran in., record_stage_mode(), update_settings()

### Community 42 - "test_opencode_discovery.py"
Cohesion: 0.14
Nodes (14): asyncio, Unit tests for OpenCode discovery, port resilience, and health diagnostics., OPENCODE_SERVER_URL env var should override all detection., Dynamic port from 'opencode service status' should be extracted cleanly., Password should be resolved from service.json candidate directories., When no service.json exists, an informative OpencodeUnavailable error is raised., If a port is open but occupied by another process (e.g. Kilo on 4096),…, FastAPI /api/health endpoint should report OpenCode connection and diagnostics. (+6 more)

### Community 43 - "6. PERFORMANCE & ACCESSIBILITY GUARDRAILS"
Cohesion: 0.29
Nodes (7): 6.A Hardware Acceleration, 6.B Reduced Motion (mandatory), 6.C Dark Mode (mandatory for any consumer-facing page), 6.D Core Web Vitals Targets, 6.E DOM Cost, 6.F Z-Index Restraint, 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS

### Community 44 - "post_settings"
Cohesion: 0.50
Nodes (4): post_settings(), Change live council settings. Takes effect on the next debate round., Live settings the user can change while a run is in flight., SettingsUpdate

### Community 45 - "0. BRIEF INFERENCE (Read the Room Before Anything Else)"
Cohesion: 0.40
Nodes (5): 0.A Read these signals first, 0.B Output a one-line "Design Read" before generating, 0. BRIEF INFERENCE (Read the Room Before Anything Else), 0.C If the brief is ambiguous, ask one question, do not guess, 0.D Anti-Default Discipline

### Community 46 - "12. THE BLOCK LIBRARY (Contract - Implementations Land Here Iteratively)"
Cohesion: 0.40
Nodes (5): 12.A File Location, 12.B Required Frontmatter, 12.C Required Body Sections, 12.D Block-Library Discipline, 12. THE BLOCK LIBRARY (Contract - Implementations Land Here Iteratively)

### Community 47 - "5. CONTEXT-AWARE PROACTIVITY"
Cohesion: 0.40
Nodes (5): 5.A Sticky-Stack - Canonical Skeleton, 5.B Horizontal-Pan - Canonical Skeleton, 5.C Scroll-Reveal Stagger - Canonical Skeleton (lighter alternative), 5. CONTEXT-AWARE PROACTIVITY, 5.D Forbidden Animation Patterns

### Community 48 - "8. DARK MODE PROTOCOL"
Cohesion: 0.40
Nodes (5): 8.A Token Strategy (pick one, stick to it), 8.B Do Not Prescribe Specific Colors Here, 8.C Default Mode, 8.D Test in Both Modes Before Finishing, 8. DARK MODE PROTOCOL

### Community 49 - "7. DIAL DEFINITIONS (Technical Reference)"
Cohesion: 0.50
Nodes (4): 7. DIAL DEFINITIONS (Technical Reference), DESIGN_VARIANCE (Level 1-10), MOTION_INTENSITY (Level 1-10), VISUAL_DENSITY (Level 1-10)

### Community 50 - "httpx"
Cohesion: 0.15
Nodes (10): Hybrid Council transport and unified model registry. Seamlessly combines local…, Live test script executing an end-to-end deliberation across real OpenCode…, httpx, io, json, Tests for conversation ID exposure, markdown report export, and zip bundle…, Verify in-memory zip archive packages executive-report.md, detailed-report.md,…, test_export_conversation_zip_archive() (+2 more)

### Community 51 - "test_hybrid_providers.py"
Cohesion: 0.13
Nodes (22): list_unified_models(), Return all available models across local OpenCode and configured external…, delete_key(), Store or clear a key for a provider., Delete a key for a provider., set_key(), asyncio, Real, non-mocked tests for Phase 6: Hybrid Provider & Custom API Key Ingestion.… (+14 more)

### Community 54 - "test_ui_controls_telemetry.py"
Cohesion: 0.24
Nodes (9): pytest, asyncio, Unit and integration tests for Phase 7: UI Controls, Eviction Badges & Budget…, Verify CouncilRun captures evicted_models, retired_models, and emits early…, Verify /api/health provides all fields required by the frontend Sidebar health…, Verify /api/providers/keys endpoints support modal interactions: list, update,…, test_council_session_budget_and_eviction_telemetry(), test_health_api_contract_matches_frontend() (+1 more)

### Community 55 - "backend/__init__.py"
Cohesion: 0.27
Nodes (7): asyncio, LLM Council backend package., End-to-end test of the HTTP API, including the SSE streaming path. Creates a…, Verification script for the opencode client and the council sandbox. Run with:…, pathlib, sys, urllib_request

### Community 56 - "prompts.py"
Cohesion: 0.18
Nodes (10): parse_verdict(), position_prompt(), Prompts for the four council stages. Kept in one place so the wording of each…, Stage 3: blind, anonymized scoring of the positions., Stage 1: independent first opinion. Never compressed - a human reads this., Split a chairman response into its sections. Falls back to putting everything…, Short conversation title., review_prompt() (+2 more)

### Community 57 - "debate_prompt"
Cohesion: 0.20
Nodes (10): debate_prompt(), Stage 4: the chairman's decision. Never compressed - a human reads this., Stage 2: named cross-examination, one round at a time. `caveman_instruction` is…, verdict_prompt(), Verify that verdict_prompt alerts the chairman to expand compressed debate…, Verify that debate_prompt embeds the Caveman max instruction cleanly., test_chairman_prompt_contains_expansion_directive_for_max(), test_prompts_integrate_max_contract() (+2 more)

### Community 58 - "post"
Cohesion: 0.25
Nodes (8): create_project(), CreateProjectRequest, prune_empty_conversations(), Create a new project workspace folder., Prune all empty abandoned conversations (0 messages)., Request to create a new project workspace folder., main(), post()

### Community 59 - "send_message"
Cohesion: 0.39
Nodes (8): Send a message and run the full four-stage council. Returns the complete…, send_message(), get_time_limit_seconds(), get_token_budget_total(), get_token_cap_per_model(), Any, Verify /api/settings handles both retrieval and updates for debate mode and…, test_settings_api_supports_budget_controls()

### Community 60 - "._open_sessions"
Cohesion: 0.33
Nodes (4): _call_make(), AsyncClient, Determine thinking quality / reasoning effort per model: - Honored if…, Create one session per member with resolved thinking quality. Returns the…

### Community 61 - "list_conversations"
Cohesion: 0.50
Nodes (4): list_conversations(), List all conversations (metadata only)., list_conversations(), List all conversations (metadata only). By default, empty conversations (0…

### Community 62 - "post_provider_key"
Cohesion: 0.50
Nodes (4): post_provider_key(), ProviderKeyUpdate, Payload to configure or remove a provider API key., Update or remove a provider API key dynamically.

### Community 63 - "reconcile_council_preset"
Cohesion: 0.50
Nodes (4): Reconciles a saved council preset against currently available OpenCode models.…, reconcile_council_preset(), Verify preset reconciliation logic: If a saved model is missing from OpenCode,…, test_preset_auto_reconciliation()

### Community 64 - "update_project"
Cohesion: 0.67
Nodes (3): Update a project name or description., update_project(), patch

### Community 66 - "graphify.js"
Cohesion: 0.40
Nodes (3): IMPORTANT: keep the reminder string free of backticks and $(...) constructs., ref_fs, ref_path

### Community 69 - "React + Vite"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

## Knowledge Gaps
- **162 isolated node(s):** `name`, `private`, `version`, `type`, `dev` (+157 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 469 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CLAUDE.md - Technical Notes for LLM Council` connect `CouncilSession` to `list_models`, `icons.jsx`, `prompts.py`?**
  _High betweenness centrality (0.218) - this node is a cross-community bridge._
- **Why does `CouncilRun` connect `CouncilRun` to `CouncilSession`, `council.py`, `test_thinking_quality_and_deduplication.py`, `caveman.py`, `test_chairman_selection.py`, `test_human_steering.py`, `backend/main.py`, `test_caveman_max.py`, `send_message_stream`, `test_hybrid_providers.py`, `test_token_budgeting.py`, `test_ui_controls_telemetry.py`, `list_models`, `verify_caveman.py`, `HybridCouncilSession`, `._open_sessions`, `resolve_roster`?**
  _High betweenness centrality (0.214) - this node is a cross-community bridge._
- **Why does `Frontend` connect `icons.jsx` to `CouncilSession`?**
  _High betweenness centrality (0.206) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `CouncilRun` (e.g. with `HybridCouncilSession` and `CouncilSession`) actually correct?**
  _`CouncilRun` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `CouncilSession` (e.g. with `CouncilRun` and `HybridCouncilSession`) actually correct?**
  _`CouncilSession` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _162 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `CouncilSession` be split into smaller, more focused modules?**
  _Cohesion score 0.07610993657505286 - nodes in this community are weakly interconnected._