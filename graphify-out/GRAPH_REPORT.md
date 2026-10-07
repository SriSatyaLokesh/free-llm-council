# Graph Report - free-llm-council  (2026-10-07)

## Corpus Check
- 70 files · ~72,861 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 22 file(s) not represented in the graph (top: .css 16, (none) 4, .cff 1)

## Summary
- 916 nodes · 1846 edges · 68 communities (56 shown, 12 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 61 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `99942194`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Any
- CouncilSession
- icons.jsx
- council.py
- CouncilRun
- package.json
- get
- test_model_eviction.py
- verify_caveman.py
- test_chairman_selection.py
- create_conversation
- Appendix B - Canonical Sources (read these before reinventing)
- test_thinking_quality_and_deduplication.py
- test_human_steering.py
- backend/main.py
- get_conversation
- OpencodeUnavailable
- post
- generate_conversation_title
- storage.py
- provider_keys.py
- test_token_budgeting.py
- BaseModel
- 4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)
- list_models
- ._check_budget_limits
- HybridCouncilSession
- Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine
- 4. Component Standards
- get_active_run
- test_non_reporting_agents.py
- start.sh
- tests/__init__.py
- 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)
- pytest
- tasteskill: Anti-Slop Frontend Skill
- 9. AI TELLS (Forbidden Patterns)
- 11. REDESIGN PROTOCOL
- 3. DEFAULT ARCHITECTURE & CONVENTIONS
- post_settings
- test_opencode_discovery.py
- 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS
- _sum_tokens
- 0. BRIEF INFERENCE (Read the Room Before Anything Else)
- 12. THE BLOCK LIBRARY (Contract - Implementations Land Here Iteratively)
- 5. CONTEXT-AWARE PROACTIVITY
- 8. DARK MODE PROTOCOL
- 7. DIAL DEFINITIONS (Technical Reference)
- backend/__init__.py
- test_hybrid_providers.py
- git-workflow.md
- free-llm-council
- settings.py
- opencode_client.py
- prompts.py
- delete_conversation
- create_project
- diagnose_connection
- ._ask_all
- ._tighten
- .__init__
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
5. `ChatInterface()` - 19 edges
6. `react` - 17 edges
7. `list_models()` - 16 edges
8. `tasteskill: Anti-Slop Frontend Skill` - 16 edges
9. `HybridCouncilSession` - 15 edges
10. `ReportPage()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `It is the upstream implementation, not a local imitation` --references--> `status()`  [INFERRED]
  CLAUDE.md → backend/caveman.py
- `Backend structure` --references--> `resolve_roster()`  [INFERRED]
  CLAUDE.md → backend/council.py
- `Common gotchas` --references--> `resolve_roster()`  [INFERRED]
  CLAUDE.md → backend/council.py
- `Backend structure` --references--> `calculate_aggregate_rankings()`  [INFERRED]
  CLAUDE.md → backend/council.py
- `Backend structure` --references--> `CouncilRun`  [INFERRED]
  CLAUDE.md → backend/council.py

## Import Cycles
- None detected.

## Communities (68 total, 12 thin omitted)

### Community 0 - "Any"
Cohesion: 0.15
Nodes (23): Update a project name or description., update_project(), create_project(), delete_project(), ensure_data_dir(), get_project(), get_projects_file(), list_projects() (+15 more)

### Community 1 - "CouncilSession"
Cohesion: 0.16
Nodes (14): CouncilSession, _parse_assistant_message(), Any, Flatten an opencode assistant message into text / reasoning / tool calls., One opencode session driven by one council member. The session is reused across…, Create the underlying opencode session., Delete the opencode session so it does not clutter the user's list., Replace this session's permission ruleset mid-run. Used to tighten the sandbox… (+6 more)

### Community 2 - "icons.jsx"
Cohesion: 0.08
Nodes (69): Frontend, B. Workspace Header & Breadcrumbs, api, App(), ChatInterface(), DebateMode(), LEVEL_LABELS, AlertTriangle() (+61 more)

### Community 3 - "council.py"
Cohesion: 0.21
Nodes (13): _aggregate_block(), calculate_aggregate_rankings(), _clip(), _debate_block(), _label(), _positions_block(), AsyncClient, Four-stage LLM Council orchestration. Stage 1 Positions - every member answers… (+5 more)

### Community 4 - "CouncilRun"
Cohesion: 0.13
Nodes (13): CouncilRun, _call_make(), Any, Resolve the roster, then run the full four-stage council., One council deliberation, owning every session it creates., Inject human operator guidance and resources into the ongoing deliberation., Determine thinking quality / reasoning effort per model: - Honored if…, Accumulate token telemetry for a model and update global council totals. (+5 more)

### Community 5 - "package.json"
Cohesion: 0.06
Nodes (35): allowScripts, esbuild@0.25.12, dependencies, react, react-dom, react-markdown, remark-gfm, devDependencies (+27 more)

### Community 6 - "get"
Cohesion: 0.11
Nodes (19): export_conversation_pdf(), export_conversation_report(), export_conversation_zip_archive(), get_conversation(), get_project(), list_projects(), List all project folders with metadata and debate counts., Get details for a specific project. (+11 more)

### Community 7 - "test_model_eviction.py"
Cohesion: 0.18
Nodes (13): make_mock_session(), asyncio, Unit tests for Phase 2: Dynamic Member Fault-Tolerance & Model Eviction., If a model succeeds in Stage 1 but crashes in Debate Round 1, it must be…, Create a mock CouncilSession that records ask() calls and session lifecycle., If the designated chairman fails during deliberation, the council must promote…, When run_stream is used, an eviction should emit a 'model_evicted' event., If a model fails in Stage 1, it must be evicted immediately and NEVER called… (+5 more)

### Community 8 - "verify_caveman.py"
Cohesion: 0.06
Nodes (42): build_instruction(), intensity_for(), is_installed(), load_skill(), Path, Official Caveman compression, loaded at runtime from the installed skill.…, Return the text under '## <heading>', up to the next '## '., Pull one level's row out of Caveman's own Intensity table. Keeping this parsed… (+34 more)

### Community 9 - "test_chairman_selection.py"
Cohesion: 0.09
Nodes (28): Any, Intelligent capability scoring matrix for LLM Council Chairman election. Ranks…, Select the highest capability model ID from a list of model dicts or model IDs., Compute an intelligence score (0 to 100+) for a given model dict or model ID…, score_model_capability(), select_best_chairman(), Work out who sits on the council and who chairs it. Defaults to every model…, resolve_roster() (+20 more)

### Community 10 - "create_conversation"
Cohesion: 0.11
Nodes (22): list_conversations(), List all conversations (metadata only)., create_conversation(), delete_conversation(), get_conversation_path(), list_conversations(), prune_empty_conversations(), Prune all abandoned conversations that have 0 messages. Args: except_id:… (+14 more)

### Community 11 - "Appendix B - Canonical Sources (read these before reinventing)"
Cohesion: 0.09
Nodes (21): APPENDICES - Real Source-Backed Reference Material, Appendix A - Install Commands per Design System, Appendix B - Canonical Sources (read these before reinventing), Appendix C - Apple Liquid Glass: Honest Web Approximation, Apple Liquid Glass (Apple platforms only), Atlassian, Bootstrap, Carbon (+13 more)

### Community 12 - "test_thinking_quality_and_deduplication.py"
Cohesion: 0.18
Nodes (12): asyncio, Unit tests for Phase 8: Per-Model Thinking Quality & Model Deduplication., Verify distinct models like ling 3.1 and ling 3.0 fin are not collapsed to the…, Verify CouncilRun defaults the Chairman to max thinking and regular members to…, Verify user overrides for thinking quality are honored over defaults., Verify list_models includes variants list and deduplicates identical IDs., Verify CouncilSession includes variant in the model specification object., test_council_run_defaults_chairman_to_max_thinking() (+4 more)

### Community 13 - "test_human_steering.py"
Cohesion: 0.17
Nodes (13): Register an ongoing CouncilRun by conversation ID., Unregister an ongoing CouncilRun by conversation ID., register_active_run(), unregister_active_run(), asyncio, Unit and integration tests for Phase 11: Human-in-the-Loop Mid-Debate Steering…, Verify active run registration and steering injection on CouncilRun., Verify that steering injected into a CouncilRun appears in debate prompt, queue… (+5 more)

### Community 14 - "backend/main.py"
Cohesion: 0.14
Nodes (13): get_provider_keys(), health(), FastAPI backend for LLM Council., Health check endpoint., Detailed health check validating connection to OpenCode and BYOK readiness., Get status and redacted preview of configured provider API keys., root(), fastapi (+5 more)

### Community 15 - "get_conversation"
Cohesion: 0.15
Nodes (21): Update conversation metadata such as title or assigned project folder., update_conversation(), add_assistant_message(), add_user_message(), assign_conversation_project(), get_conversation(), Add a user message to a conversation. Args: conversation_id: Conversation…, Add an assistant message holding a complete council run. The whole run is… (+13 more)

### Community 16 - "OpencodeUnavailable"
Cohesion: 0.17
Nodes (12): get_server_password(), OpencodeUnavailable, Path, Raised when the local opencode server cannot be reached., Possible locations of opencode's service.json., Resolve the opencode server password. Order: OPENCODE_SERVER_PASSWORD env var,…, _service_config_candidates(), RuntimeError (+4 more)

### Community 17 - "post"
Cohesion: 0.18
Nodes (11): create_conversation(), CreateConversationRequest, post_provider_key(), ProviderKeyUpdate, prune_empty_conversations(), Payload to configure or remove a provider API key., Update or remove a provider API key dynamically., Create a new conversation. (+3 more)

### Community 18 - "generate_conversation_title"
Cohesion: 0.25
Nodes (8): generate_conversation_title(), Short title for a conversation, using the fastest available model., Send a message and stream the council as it runs. Emits Server-Sent Events as…, Request to send a message in a conversation., send_message_stream(), emit(), event_generator(), SendMessageRequest

### Community 19 - "storage.py"
Cohesion: 0.11
Nodes (26): export_conversation_html(), get_conversation_reports(), Export a council deliberation as a standalone publication-grade HTML report., Return pre-rendered executive and detailed reports with deliberation metadata…, _clean_table_cell(), _extract_non_reporting_models(), format_conversation_detailed(), format_conversation_executive() (+18 more)

### Community 20 - "provider_keys.py"
Cohesion: 0.20
Nodes (13): _get_env_key(), get_key(), get_key_statuses(), _init_from_env(), Any, Secure in-memory and environment-backed provider API key management. Supports…, Retrieve key from environment variables including known aliases., Retrieve the raw secret key for a provider. (+5 more)

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
Cohesion: 0.14
Nodes (18): parse_ranking_from_text(), Extract the ordered labels from a 'FINAL RANKING:' block., ask_many(), _auth_headers(), get_server_url(), list_models(), opencode_request(), AsyncClient (+10 more)

### Community 25 - "._check_budget_limits"
Cohesion: 0.22
Nodes (5): emit(), Check if any active model has exceeded token_cap_per_model. If exceeded, retire…, Determine if the debate loop should terminate early due to: 1. Total token…, Evict a failing or depleted model immediately and ensure it is never called…, If current chairman is evicted or inactive, fail over to the next highest-…

### Community 26 - "HybridCouncilSession"
Cohesion: 0.29
Nodes (3): HybridCouncilSession, Any, Unified session wrapper routing to either local OpenCode daemon or direct…

### Community 27 - "Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine"
Cohesion: 0.10
Nodes (20): 1. Prerequisites, 2. Start OpenCode Service, 3. Clone & Install, 4. Launch the Platform, Can I still use commercial models like Claude 3.5 Sonnet, GPT-4o, or DeepSeek R1?, Citation, Comparison: Upstream Concept vs. Free LLM Council, Configuration & BYOK Cloud Providers (+12 more)

### Community 28 - "4. Component Standards"
Cohesion: 0.17
Nodes (11): 1. Dials & Atmosphere, 2. Color Palette & Surface Elevation, 3. Typography & Micro-Hierarchy, 4. Component Standards, 5. Performance, Ergonomics & Fast Handling, A. Left-Hand Sidebar (Workspace Tree), Accents & Signal Colors, C. Live RunRail (Real-Time Progress) (+3 more)

### Community 29 - "get_active_run"
Cohesion: 0.33
Nodes (6): get_active_run(), Retrieve the active CouncilRun for a conversation ID, if any., Inject human operator guidance and resources into an ongoing deliberation., Request to inject human operator guidance into an ongoing debate., steer_conversation(), SteerRequest

### Community 30 - "test_non_reporting_agents.py"
Cohesion: 0.29
Nodes (8): make_mock_session(), asyncio, Unit tests for non-reporting agents, upfront report notices, and Phase 1…, If a member cannot initialize session, it is registered as evicted and excluded…, If a member times out in Phase 1, it quits before debate and is excluded from…, test_phase_1_dropout_quits_debate_and_excluded_from_prompts(), test_session_init_failure_evicts_non_reporting_member(), fake_make()

### Community 34 - "10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)"
Cohesion: 0.20
Nodes (10): 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know), Animation Library Choice, Cards & Containers, Galleries & Media, Hero Paradigms, Layout & Grids, Micro-Interactions & Effects, Navigation & Menus (+2 more)

### Community 36 - "pytest"
Cohesion: 0.24
Nodes (9): pytest, asyncio, Unit and integration tests for Phase 10: Projects & Workspace Folder Hierarchy., Verify creating debate directly in project, moving between projects, and…, Verify HTTP API PATCH endpoint for renaming and archiving conversations., HTTP API integration tests for /api/projects and /api/conversations/{id}., test_conversation_archive_and_rename_api(), test_create_conversation_with_project_and_move_lifecycle() (+1 more)

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

### Community 41 - "post_settings"
Cohesion: 0.50
Nodes (4): post_settings(), Change live council settings. Takes effect on the next debate round., Live settings the user can change while a run is in flight., SettingsUpdate

### Community 42 - "test_opencode_discovery.py"
Cohesion: 0.29
Nodes (7): asyncio, Unit tests for OpenCode discovery, port resilience, and health diagnostics., If a port is open but occupied by another process (e.g. Kilo on 4096),…, FastAPI /api/health endpoint should report OpenCode connection and diagnostics., test_diagnose_connection_detects_port_conflict(), test_health_endpoint_returns_diagnostics(), unittest_mock

### Community 43 - "6. PERFORMANCE & ACCESSIBILITY GUARDRAILS"
Cohesion: 0.29
Nodes (7): 6.A Hardware Acceleration, 6.B Reduced Motion (mandatory), 6.C Dark Mode (mandatory for any consumer-facing page), 6.D Core Web Vitals Targets, 6.E DOM Cost, 6.F Z-Index Restraint, 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS

### Community 44 - "_sum_tokens"
Cohesion: 0.50
Nodes (3): Total the token counts opencode reported for a set of entries. opencode returns…, Token totals per stage, so the toggle's effect is visible rather than promised.…, _sum_tokens()

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

### Community 50 - "backend/__init__.py"
Cohesion: 0.12
Nodes (14): Hybrid Council transport and unified model registry. Seamlessly combines local…, LLM Council backend package., Live test script executing an end-to-end deliberation across real OpenCode…, httpx, io, json, Real, non-mocked tests for Phase 5: Caveman Max Mode & Debate Compression.…, Ensure 'max' is recognized as a first-class debate compression level. (+6 more)

### Community 51 - "test_hybrid_providers.py"
Cohesion: 0.14
Nodes (20): list_unified_models(), Return all available models across local OpenCode and configured external…, delete_key(), Store or clear a key for a provider., Delete a key for a provider., set_key(), asyncio, Real, non-mocked tests for Phase 6: Hybrid Provider & Custom API Key Ingestion.… (+12 more)

### Community 54 - "settings.py"
Cohesion: 0.07
Nodes (36): get_settings(), Current council settings, plus whether the official Caveman skill is installed.…, Send a message and run the full four-stage council. Returns the complete…, send_message(), get_debate_mode(), get_settings(), get_time_limit_seconds(), get_token_budget_total() (+28 more)

### Community 55 - "opencode_client.py"
Cohesion: 0.14
Nodes (16): asyncio, Configuration for the LLM Council. The council runs entirely on models that are…, Client for the local opencode server. This module replaces the old OpenRouter…, council_sessions(), main(), End-to-end test of the HTTP API, including the SSE streaming path. Creates a…, Council sessions currently left in the user's opencode session list., Verification script for the opencode client and the council sandbox. Run with:… (+8 more)

### Community 56 - "prompts.py"
Cohesion: 0.10
Nodes (20): debate_prompt(), parse_verdict(), position_prompt(), Prompts for the four council stages. Kept in one place so the wording of each…, Stage 3: blind, anonymized scoring of the positions., Stage 4: the chairman's decision. Never compressed - a human reads this., Stage 1: independent first opinion. Never compressed - a human reads this., Split a chairman response into its sections. Falls back to putting everything… (+12 more)

### Community 57 - "delete_conversation"
Cohesion: 0.40
Nodes (5): delete_conversation(), delete_project(), Delete a project folder and revert its debates to independent mode., Delete a conversation by ID., delete

### Community 58 - "create_project"
Cohesion: 0.50
Nodes (4): create_project(), CreateProjectRequest, Create a new project workspace folder., Request to create a new project workspace folder.

### Community 59 - "diagnose_connection"
Cohesion: 0.50
Nodes (4): diagnose_connection(), _location_params(), Every opencode call is scoped to the council's workspace directory., Actively inspect the connection to the OpenCode server and return a detailed…

### Community 66 - "graphify.js"
Cohesion: 0.40
Nodes (3): IMPORTANT: keep the reminder string free of backticks and $(...) constructs., ref_fs, ref_path

### Community 69 - "React + Vite"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

## Knowledge Gaps
- **162 isolated node(s):** `name`, `private`, `version`, `type`, `dev` (+157 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 470 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CLAUDE.md - Technical Notes for LLM Council` connect `verify_caveman.py` to `list_models`, `CouncilSession`, `icons.jsx`, `prompts.py`?**
  _High betweenness centrality (0.228) - this node is a cross-community bridge._
- **Why does `Frontend` connect `icons.jsx` to `verify_caveman.py`?**
  _High betweenness centrality (0.216) - this node is a cross-community bridge._
- **Why does `CouncilRun` connect `CouncilRun` to `CouncilSession`, `council.py`, `test_model_eviction.py`, `verify_caveman.py`, `test_chairman_selection.py`, `test_thinking_quality_and_deduplication.py`, `test_human_steering.py`, `backend/main.py`, `generate_conversation_title`, `test_token_budgeting.py`, `list_models`, `._check_budget_limits`, `HybridCouncilSession`, `test_non_reporting_agents.py`, `_sum_tokens`, `backend/__init__.py`, `test_hybrid_providers.py`, `settings.py`, `._ask_all`, `._tighten`?**
  _High betweenness centrality (0.215) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `CouncilRun` (e.g. with `HybridCouncilSession` and `CouncilSession`) actually correct?**
  _`CouncilRun` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `CouncilSession` (e.g. with `CouncilRun` and `HybridCouncilSession`) actually correct?**
  _`CouncilSession` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _162 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `icons.jsx` be split into smaller, more focused modules?**
  _Cohesion score 0.07553124342520513 - nodes in this community are weakly interconnected._