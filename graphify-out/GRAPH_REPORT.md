# Graph Report - llm-council  (2026-10-06)

## Corpus Check
- 66 files · ~63,476 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 20 file(s) not represented in the graph (top: .css 14, (none) 4, .cff 1)

## Summary
- 860 nodes · 1655 edges · 67 communities (57 shown, 10 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 57 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d0ec6b98`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- storage.py
- CouncilSession
- icons.jsx
- council.py
- prompts.py
- package.json
- post
- test_thinking_quality_and_deduplication.py
- verify_caveman.py
- test_chairman_selection.py
- create_conversation
- Appendix B - Canonical Sources (read these before reinventing)
- CouncilRun
- test_opencode_discovery.py
- backend/main.py
- get_conversation
- _sum_tokens
- BaseModel
- backend/__init__.py
- Any
- debate_prompt
- test_token_budgeting.py
- ._check_budget_limits
- 4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)
- opencode_client.py
- delete_conversation
- test_caveman_max.py
- Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine
- 4. Component Standards
- get_server_password
- list_models
- start.sh
- tests/__init__.py
- 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)
- test_projects_and_folders.py
- tasteskill: Anti-Slop Frontend Skill
- 9. AI TELLS (Forbidden Patterns)
- 11. REDESIGN PROTOCOL
- 3. DEFAULT ARCHITECTURE & CONVENTIONS
- settings.py
- get_active_run
- 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS
- test_ui_controls_telemetry.py
- 0. BRIEF INFERENCE (Read the Room Before Anything Else)
- 12. THE BLOCK LIBRARY (Contract - Implementations Land Here Iteratively)
- 5. CONTEXT-AWARE PROACTIVITY
- 8. DARK MODE PROTOCOL
- 7. DIAL DEFINITIONS (Technical Reference)
- add_assistant_message
- test_hybrid_providers.py
- git-workflow.md
- free-llm-council
- diagnose_connection
- get_project
- test_human_steering.py
- send_message
- ._open_sessions
- send_message_stream
- post_settings
- asyncio
- graphify.js
- React + Vite
- AGENTS.md
- rules/graphify.md
- workflows/graphify.md

## God Nodes (most connected - your core abstractions)
1. `CouncilRun` - 57 edges
2. `CouncilSession` - 27 edges
3. `Sidebar()` - 19 edges
4. `get_conversation()` - 19 edges
5. `list_models()` - 16 edges
6. `tasteskill: Anti-Slop Frontend Skill` - 16 edges
7. `HybridCouncilSession` - 15 edges
8. `Appendix B - Canonical Sources (read these before reinventing)` - 15 edges
9. `react` - 15 edges
10. `send_message()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Backend structure` --references--> `CouncilSession`  [INFERRED]
  CLAUDE.md → backend/opencode_client.py
- `Backend structure` --references--> `CouncilRun`  [INFERRED]
  CLAUDE.md → backend/council.py
- `Backend structure` --references--> `get_server_password()`  [INFERRED]
  CLAUDE.md → backend/opencode_client.py
- `Common gotchas` --references--> `_auth_headers()`  [INFERRED]
  CLAUDE.md → backend/opencode_client.py
- `Backend structure` --references--> `calculate_aggregate_rankings()`  [INFERRED]
  CLAUDE.md → backend/council.py

## Import Cycles
- None detected.

## Communities (67 total, 10 thin omitted)

### Community 0 - "storage.py"
Cohesion: 0.18
Nodes (19): create_project(), delete_project(), ensure_data_dir(), get_projects_file(), list_projects(), load_all_projects(), prune_empty_conversations(), JSON-based storage for conversations. (+11 more)

### Community 1 - "CouncilSession"
Cohesion: 0.09
Nodes (26): CouncilSession, _parse_assistant_message(), Any, Flatten an opencode assistant message into text / reasoning / tool calls., One opencode session driven by one council member. The session is reused across…, Create the underlying opencode session., Delete the opencode session so it does not clutter the user's list., Replace this session's permission ruleset mid-run. Used to tighten the sandbox… (+18 more)

### Community 2 - "icons.jsx"
Cohesion: 0.08
Nodes (56): Frontend, B. Workspace Header & Breadcrumbs, api, App(), ChatInterface(), DebateMode(), LEVEL_LABELS, AlertTriangle() (+48 more)

### Community 3 - "council.py"
Cohesion: 0.16
Nodes (17): _aggregate_block(), calculate_aggregate_rankings(), _clip(), _debate_block(), _label(), _positions_block(), Any, Four-stage LLM Council orchestration. Stage 1 Positions - every member answers… (+9 more)

### Community 4 - "prompts.py"
Cohesion: 0.15
Nodes (12): generate_conversation_title(), Short title for a conversation, using the fastest available model., parse_verdict(), position_prompt(), Prompts for the four council stages. Kept in one place so the wording of each…, Stage 3: blind, anonymized scoring of the positions., Stage 1: independent first opinion. Never compressed - a human reads this., Split a chairman response into its sections. Falls back to putting everything… (+4 more)

### Community 5 - "package.json"
Cohesion: 0.06
Nodes (34): allowScripts, esbuild@0.25.12, dependencies, react, react-dom, react-markdown, devDependencies, eslint (+26 more)

### Community 6 - "post"
Cohesion: 0.18
Nodes (11): create_conversation(), create_project(), CreateConversationRequest, CreateProjectRequest, prune_empty_conversations(), Create a new project workspace folder., Create a new conversation., Prune all empty abandoned conversations (0 messages). (+3 more)

### Community 7 - "test_thinking_quality_and_deduplication.py"
Cohesion: 0.07
Nodes (32): Reconciles a saved council preset against currently available OpenCode models.…, reconcile_council_preset(), pytest, Unit tests for Phase 9: Clean Conversation Lifecycle & Persisted Council…, Verify preset reconciliation logic: If a saved model is missing from OpenCode,…, test_preset_auto_reconciliation(), make_mock_session(), asyncio (+24 more)

### Community 8 - "verify_caveman.py"
Cohesion: 0.26
Nodes (11): council_permissions(), Build the permission ruleset for council members. Allow the research and read…, council_sessions(), main(), _median(), one_shot(), part_one(), part_two() (+3 more)

### Community 9 - "test_chairman_selection.py"
Cohesion: 0.06
Nodes (45): Any, Intelligent capability scoring matrix for LLM Council Chairman election. Ranks…, Select the highest capability model ID from a list of model dicts or model IDs., Compute an intelligence score (0 to 100+) for a given model dict or model ID…, score_model_capability(), select_best_chairman(), build_instruction(), intensity_for() (+37 more)

### Community 10 - "create_conversation"
Cohesion: 0.21
Nodes (12): create_conversation(), delete_conversation(), get_conversation_path(), Get the file path for a conversation., Create a new conversation. Args: conversation_id: Unique identifier for the…, Permanently delete a conversation from storage. Returns: True if the file was…, Verify that abandoned empty conversations (0 messages) are pruned., Verify list_conversations does not return phantom empty conversations. (+4 more)

### Community 11 - "Appendix B - Canonical Sources (read these before reinventing)"
Cohesion: 0.09
Nodes (21): APPENDICES - Real Source-Backed Reference Material, Appendix A - Install Commands per Design System, Appendix B - Canonical Sources (read these before reinventing), Appendix C - Apple Liquid Glass: Honest Web Approximation, Apple Liquid Glass (Apple platforms only), Atlassian, Bootstrap, Carbon (+13 more)

### Community 12 - "CouncilRun"
Cohesion: 0.13
Nodes (9): CouncilRun, One council deliberation, owning every session it creates., Inject human operator guidance and resources into the ongoing deliberation., Execute all four stages and return the full result. On any failure that is not…, Execute all four stages, optionally emitting progress as it goes. `queue`…, Re-scope every member's permissions, ignoring individual failures., Queue, Verify that CouncilRun properly initializes token and time tracking structures. (+1 more)

### Community 13 - "test_opencode_discovery.py"
Cohesion: 0.29
Nodes (7): json, asyncio, Unit tests for OpenCode discovery, port resilience, and health diagnostics., If a port is open but occupied by another process (e.g. Kilo on 4096),…, FastAPI /api/health endpoint should report OpenCode connection and diagnostics., test_diagnose_connection_detects_port_conflict(), test_health_endpoint_returns_diagnostics()

### Community 14 - "backend/main.py"
Cohesion: 0.09
Nodes (28): export_conversation_report(), export_conversation_zip_archive(), get_conversation(), get_models(), get_project(), get_provider_keys(), health(), list_conversations() (+20 more)

### Community 15 - "get_conversation"
Cohesion: 0.18
Nodes (18): Update conversation metadata such as title or assigned project folder., update_conversation(), add_user_message(), assign_conversation_project(), get_conversation(), Add a user message to a conversation. Args: conversation_id: Conversation…, Update the title of a conversation. Args: conversation_id: Conversation…, Set the archived status of a conversation. Args: conversation_id: Conversation… (+10 more)

### Community 16 - "_sum_tokens"
Cohesion: 0.33
Nodes (5): Total the token counts opencode reported for a set of entries. opencode returns…, Token totals per stage, so the toggle's effect is visible rather than promised.…, _sum_tokens(), Verify token summation logic against realistic OpenCode token telemetry: input…, test_sum_tokens_real_telemetry()

### Community 17 - "BaseModel"
Cohesion: 0.18
Nodes (11): Conversation, ConversationMetadata, ProviderKeyUpdate, Full conversation with all messages., Payload to configure or remove a provider API key., Request to update a project., Request to update a conversation (project assignment, title, or archive status)., Conversation metadata for list view. (+3 more)

### Community 18 - "backend/__init__.py"
Cohesion: 0.17
Nodes (12): asyncio, LLM Council backend package., council_sessions(), main(), End-to-end test of the HTTP API, including the SSE streaming path. Creates a…, Council sessions currently left in the user's opencode session list., Verification script for the opencode client and the council sandbox. Run with:…, pathlib (+4 more)

### Community 19 - "Any"
Cohesion: 0.15
Nodes (14): export_conversation_zip(), format_conversation_markdown(), list_conversations(), Any, List all conversations (metadata only). By default, empty conversations (0…, Format a complete council deliberation into a clean, comprehensive Markdown…, Build an in-memory zip archive containing: - report.md (human-readable…, io (+6 more)

### Community 20 - "debate_prompt"
Cohesion: 0.20
Nodes (10): debate_prompt(), Stage 4: the chairman's decision. Never compressed - a human reads this., Stage 2: named cross-examination, one round at a time. `caveman_instruction` is…, verdict_prompt(), Verify that verdict_prompt alerts the chairman to expand compressed debate…, Verify that debate_prompt embeds the Caveman max instruction cleanly., test_chairman_prompt_contains_expansion_directive_for_max(), test_prompts_integrate_max_contract() (+2 more)

### Community 21 - "test_token_budgeting.py"
Cohesion: 0.13
Nodes (15): Live test script executing an end-to-end deliberation across real OpenCode…, httpx, asyncio, Real, non-mocked tests for Phase 3: Token & Time Budgeting Engine. Tests verify…, Functional test: When cumulative tokens across all models exceed…, Real wall-clock test: When real elapsed time crosses time_limit_seconds, debate…, Integration test: In a 4-round deliberation, when the token budget is capped…, Real HTTP integration test: Verify that FastAPI /api/settings accepts and… (+7 more)

### Community 22 - "._check_budget_limits"
Cohesion: 0.22
Nodes (5): emit(), Check if any active model has exceeded token_cap_per_model. If exceeded, retire…, Determine if the debate loop should terminate early due to: 1. Total token…, Evict a failing or depleted model immediately and ensure it is never called…, If current chairman is evicted or inactive, fail over to the next highest-…

### Community 23 - "4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)"
Cohesion: 0.17
Nodes (12): 4.10 Quotes & Testimonials, 4.11 Page Theme Lock (Light / Dark Mode Consistency), 4.1 Typography, 4.2 Color Calibration, 4.3 Layout Diversification, 4.4 Materiality, Shadows, Cards, 4.5 Interactive UI States, 4.6 Data & Form Patterns (+4 more)

### Community 24 - "opencode_client.py"
Cohesion: 0.25
Nodes (7): Configuration for the LLM Council. The council runs entirely on models that are…, Client for the local opencode server. This module replaces the old OpenRouter…, base64, dotenv, os, shutil, subprocess

### Community 25 - "delete_conversation"
Cohesion: 0.40
Nodes (5): delete_conversation(), delete_project(), Delete a project folder and revert its debates to independent mode., Delete a conversation by ID., delete

### Community 26 - "test_caveman_max.py"
Cohesion: 0.22
Nodes (8): asyncio, Real, non-mocked tests for Phase 5: Caveman Max Mode & Debate Compression.…, Functional test: When debateMode is 'max', CouncilRun marks…, Ensure 'max' is recognized as a first-class debate compression level., HTTP integration test: FastAPI POST /api/settings accepts debateMode='max'., test_caveman_levels_includes_max(), test_council_run_records_max_caveman_mode(), test_settings_api_accepts_max_mode()

### Community 27 - "Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine"
Cohesion: 0.10
Nodes (20): 1. Prerequisites, 2. Start OpenCode Service, 3. Clone & Install, 4. Launch the Platform, Can I still use commercial models like Claude 3.5 Sonnet, GPT-4o, or DeepSeek R1?, Citation, Comparison: Upstream Concept vs. Free LLM Council, Configuration & BYOK Cloud Providers (+12 more)

### Community 28 - "4. Component Standards"
Cohesion: 0.17
Nodes (11): 1. Dials & Atmosphere, 2. Color Palette & Surface Elevation, 3. Typography & Micro-Hierarchy, 4. Component Standards, 5. Performance, Ergonomics & Fast Handling, A. Left-Hand Sidebar (Workspace Tree), Accents & Signal Colors, C. Live RunRail (Real-Time Progress) (+3 more)

### Community 29 - "get_server_password"
Cohesion: 0.22
Nodes (9): get_server_password(), Path, Possible locations of opencode's service.json., Resolve the opencode server password. Order: OPENCODE_SERVER_PASSWORD env var,…, _service_config_candidates(), Password should be resolved from service.json candidate directories., When no service.json exists, an informative OpencodeUnavailable error is raised., test_get_server_password_missing_raises_actionable_error() (+1 more)

### Community 30 - "list_models"
Cohesion: 0.11
Nodes (21): parse_ranking_from_text(), Extract the ordered labels from a 'FINAL RANKING:' block., ask_many(), _auth_headers(), get_server_url(), list_models(), opencode_request(), OpencodeUnavailable (+13 more)

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
Cohesion: 0.16
Nodes (11): get_settings(), Current council settings, plus whether the official Caveman skill is installed.…, get_debate_mode(), get_settings(), Live, mutable council settings. These are deliberately process-global rather…, Apply a partial update. Unknown keys and bad values are ignored., Note which mode a stage ran in., record_stage_mode() (+3 more)

### Community 42 - "get_active_run"
Cohesion: 0.33
Nodes (6): get_active_run(), Retrieve the active CouncilRun for a conversation ID, if any., Inject human operator guidance and resources into an ongoing deliberation., Request to inject human operator guidance into an ongoing debate., steer_conversation(), SteerRequest

### Community 43 - "6. PERFORMANCE & ACCESSIBILITY GUARDRAILS"
Cohesion: 0.29
Nodes (7): 6.A Hardware Acceleration, 6.B Reduced Motion (mandatory), 6.C Dark Mode (mandatory for any consumer-facing page), 6.D Core Web Vitals Targets, 6.E DOM Cost, 6.F Z-Index Restraint, 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS

### Community 44 - "test_ui_controls_telemetry.py"
Cohesion: 0.27
Nodes (8): asyncio, Unit and integration tests for Phase 7: UI Controls, Eviction Badges & Budget…, Verify CouncilRun captures evicted_models, retired_models, and emits early…, Verify /api/health provides all fields required by the frontend Sidebar health…, Verify /api/providers/keys endpoints support modal interactions: list, update,…, test_council_session_budget_and_eviction_telemetry(), test_health_api_contract_matches_frontend(), test_provider_keys_api_integration()

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

### Community 50 - "add_assistant_message"
Cohesion: 0.40
Nodes (5): add_assistant_message(), Add an assistant message holding a complete council run. The whole run is…, asyncio, Verify HTTP GET endpoints for report and zip downloads., test_export_endpoints_http()

### Community 51 - "test_hybrid_providers.py"
Cohesion: 0.07
Nodes (40): HybridCouncilSession, list_unified_models(), Any, AsyncClient, Hybrid Council transport and unified model registry. Seamlessly combines local…, Return all available models across local OpenCode and configured external…, Unified session wrapper routing to either local OpenCode daemon or direct…, post_provider_key() (+32 more)

### Community 54 - "diagnose_connection"
Cohesion: 0.50
Nodes (4): diagnose_connection(), _location_params(), Every opencode call is scoped to the council's workspace directory., Actively inspect the connection to the OpenCode server and return a detailed…

### Community 55 - "get_project"
Cohesion: 0.40
Nodes (5): Update a project name or description., update_project(), get_project(), Retrieve a project by ID., patch

### Community 56 - "test_human_steering.py"
Cohesion: 0.17
Nodes (13): Register an ongoing CouncilRun by conversation ID., Unregister an ongoing CouncilRun by conversation ID., register_active_run(), unregister_active_run(), asyncio, Unit and integration tests for Phase 11: Human-in-the-Loop Mid-Debate Steering…, Verify active run registration and steering injection on CouncilRun., Verify that steering injected into a CouncilRun appears in debate prompt, queue… (+5 more)

### Community 57 - "send_message"
Cohesion: 0.39
Nodes (8): Send a message and run the full four-stage council. Returns the complete…, send_message(), get_time_limit_seconds(), get_token_budget_total(), get_token_cap_per_model(), Any, Verify /api/settings handles both retrieval and updates for debate mode and…, test_settings_api_supports_budget_controls()

### Community 58 - "._open_sessions"
Cohesion: 0.33
Nodes (4): _call_make(), AsyncClient, Determine thinking quality / reasoning effort per model: - Honored if…, Create one session per member with resolved thinking quality. Returns the…

### Community 59 - "send_message_stream"
Cohesion: 0.33
Nodes (6): Send a message and stream the council as it runs. Emits Server-Sent Events as…, Request to send a message in a conversation., send_message_stream(), emit(), event_generator(), SendMessageRequest

### Community 60 - "post_settings"
Cohesion: 0.50
Nodes (4): post_settings(), Change live council settings. Takes effect on the next debate round., Live settings the user can change while a run is in flight., SettingsUpdate

### Community 66 - "graphify.js"
Cohesion: 0.40
Nodes (3): IMPORTANT: keep the reminder string free of backticks and $(...) constructs., ref_fs, ref_path

### Community 69 - "React + Vite"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

## Knowledge Gaps
- **161 isolated node(s):** `base`, `Appendix A - Install Commands per Design System`, `Apple Liquid Glass (Apple platforms only)`, `Atlassian`, `Bootstrap` (+156 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 450 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CLAUDE.md - Technical Notes for LLM Council` connect `CouncilSession` to `icons.jsx`, `prompts.py`, `list_models`?**
  _High betweenness centrality (0.212) - this node is a cross-community bridge._
- **Why does `CouncilRun` connect `CouncilRun` to `CouncilSession`, `council.py`, `test_caveman_max.py`, `test_thinking_quality_and_deduplication.py`, `verify_caveman.py`, `test_chairman_selection.py`, `test_ui_controls_telemetry.py`, `backend/main.py`, `_sum_tokens`, `test_hybrid_providers.py`, `test_token_budgeting.py`, `._check_budget_limits`, `test_human_steering.py`, `._open_sessions`, `send_message_stream`, `list_models`?**
  _High betweenness centrality (0.204) - this node is a cross-community bridge._
- **Why does `Frontend` connect `icons.jsx` to `CouncilSession`?**
  _High betweenness centrality (0.199) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `CouncilRun` (e.g. with `HybridCouncilSession` and `CouncilSession`) actually correct?**
  _`CouncilRun` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `CouncilSession` (e.g. with `CouncilRun` and `HybridCouncilSession`) actually correct?**
  _`CouncilSession` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `base`, `Appendix A - Install Commands per Design System`, `Apple Liquid Glass (Apple platforms only)` to the rest of the system?**
  _161 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `CouncilSession` be split into smaller, more focused modules?**
  _Cohesion score 0.08906882591093117 - nodes in this community are weakly interconnected._