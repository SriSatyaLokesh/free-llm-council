# Graph Report - llm-council  (2026-10-06)

## Corpus Check
- 65 files · ~60,756 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 20 file(s) not represented in the graph (top: .css 14, (none) 4, .cff 1)

## Summary
- 844 nodes · 1628 edges · 63 communities (54 shown, 9 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 57 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5f937165`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- get_conversation
- CouncilSession
- icons.jsx
- get_key_statuses
- test_diagnose_connection_detects_port_conflict
- package.json
- test_thinking_quality_and_deduplication.py
- test_model_eviction.py
- caveman.py
- test_chairman_selection.py
- .run_stream
- Appendix B - Canonical Sources (read these before reinventing)
- council.py
- test_token_budgeting.py
- get
- CLAUDE.md - Technical Notes for LLM Council
- ._check_budget_limits
- BaseModel
- opencode_client.py
- _sum_tokens
- storage.py
- test_hybrid_providers.py
- CouncilRun
- 4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)
- verify_caveman.py
- delete_conversation
- HybridCouncilSession
- Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine
- 4. Component Standards
- get_server_password
- list_models
- start.sh
- tests/__init__.py
- 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)
- list_unified_models
- tasteskill: Anti-Slop Frontend Skill
- 9. AI TELLS (Forbidden Patterns)
- 11. REDESIGN PROTOCOL
- 3. DEFAULT ARCHITECTURE & CONVENTIONS
- settings.py
- get_active_run
- 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS
- ._collect_new_messages
- 0. BRIEF INFERENCE (Read the Room Before Anything Else)
- 12. THE BLOCK LIBRARY (Contract - Implementations Land Here Iteratively)
- 5. CONTEXT-AWARE PROACTIVITY
- 8. DARK MODE PROTOCOL
- 7. DIAL DEFINITIONS (Technical Reference)
- create_project
- post_provider_key
- .__init__
- free-llm-council
- test_human_steering.py
- graphify.js
- React + Vite
- AGENTS.md
- rules/graphify.md
- workflows/graphify.md
- backend/main.py
- test_projects_and_folders.py
- post_settings

## God Nodes (most connected - your core abstractions)
1. `CouncilRun` - 57 edges
2. `CouncilSession` - 28 edges
3. `get_conversation()` - 19 edges
4. `Sidebar()` - 19 edges
5. `list_models()` - 16 edges
6. `tasteskill: Anti-Slop Frontend Skill` - 16 edges
7. `react` - 15 edges
8. `Appendix B - Canonical Sources (read these before reinventing)` - 15 edges
9. `HybridCouncilSession` - 14 edges
10. `send_message()` - 14 edges

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

## Communities (63 total, 9 thin omitted)

### Community 0 - "get_conversation"
Cohesion: 0.05
Nodes (70): prune_empty_conversations(), Update a project name or description., Update conversation metadata such as title or assigned project folder., Prune all empty abandoned conversations (0 messages)., update_conversation(), update_project(), add_assistant_message(), add_user_message() (+62 more)

### Community 1 - "CouncilSession"
Cohesion: 0.20
Nodes (9): CouncilSession, One opencode session driven by one council member. The session is reused across…, Create the underlying opencode session., Delete the opencode session so it does not clutter the user's list., Replace this session's permission ruleset mid-run. Used to tighten the sandbox…, Send a prompt and wait for the agent loop to finish. Returns {text, reasoning,…, Stop a runaway agent loop so the session does not keep burning tokens., Watchdog: auto-reject any permission request raised for this session. Our… (+1 more)

### Community 2 - "icons.jsx"
Cohesion: 0.09
Nodes (53): Frontend, B. Workspace Header & Breadcrumbs, api, App(), ChatInterface(), DebateMode(), LEVEL_LABELS, AlertTriangle() (+45 more)

### Community 3 - "get_key_statuses"
Cohesion: 0.10
Nodes (22): delete_key(), get_key(), get_key_statuses(), Any, Retrieve the raw secret key for a provider., Store or clear a key for a provider., Delete a key for a provider., Redact a secret key so it can be safely displayed in the UI. (+14 more)

### Community 4 - "test_diagnose_connection_detects_port_conflict"
Cohesion: 0.40
Nodes (5): asyncio, If a port is open but occupied by another process (e.g. Kilo on 4096),…, FastAPI /api/health endpoint should report OpenCode connection and diagnostics., test_diagnose_connection_detects_port_conflict(), test_health_endpoint_returns_diagnostics()

### Community 5 - "package.json"
Cohesion: 0.06
Nodes (35): allowScripts, esbuild@0.25.12, dependencies, react, react-dom, react-markdown, devDependencies, eslint (+27 more)

### Community 6 - "test_thinking_quality_and_deduplication.py"
Cohesion: 0.18
Nodes (12): asyncio, Unit tests for Phase 8: Per-Model Thinking Quality & Model Deduplication., Verify distinct models like ling 3.1 and ling 3.0 fin are not collapsed to the…, Verify CouncilRun defaults the Chairman to max thinking and regular members to…, Verify user overrides for thinking quality are honored over defaults., Verify list_models includes variants list and deduplicates identical IDs., Verify CouncilSession includes variant in the model specification object., test_council_run_defaults_chairman_to_max_thinking() (+4 more)

### Community 7 - "test_model_eviction.py"
Cohesion: 0.18
Nodes (13): make_mock_session(), asyncio, Unit tests for Phase 2: Dynamic Member Fault-Tolerance & Model Eviction., If a model succeeds in Stage 1 but crashes in Debate Round 1, it must be…, Create a mock CouncilSession that records ask() calls and session lifecycle., If the designated chairman fails during deliberation, the council must promote…, When run_stream is used, an eviction should emit a 'model_evicted' event., If a model fails in Stage 1, it must be evicted immediately and NEVER called… (+5 more)

### Community 8 - "caveman.py"
Cohesion: 0.12
Nodes (22): build_instruction(), intensity_for(), is_installed(), load_skill(), Path, Official Caveman compression, loaded at runtime from the installed skill.…, Return the text under '## <heading>', up to the next '## '., Pull one level's row out of Caveman's own Intensity table. Keeping this parsed… (+14 more)

### Community 9 - "test_chairman_selection.py"
Cohesion: 0.10
Nodes (26): Any, Intelligent capability scoring matrix for LLM Council Chairman election. Ranks…, Select the highest capability model ID from a list of model dicts or model IDs., Compute an intelligence score (0 to 100+) for a given model dict or model ID…, score_model_capability(), select_best_chairman(), Work out who sits on the council and who chairs it. Defaults to every model…, resolve_roster() (+18 more)

### Community 10 - ".run_stream"
Cohesion: 0.29
Nodes (3): Execute all four stages and return the full result. On any failure that is not…, Execute all four stages, optionally emitting progress as it goes. `queue`…, Queue

### Community 11 - "Appendix B - Canonical Sources (read these before reinventing)"
Cohesion: 0.09
Nodes (21): APPENDICES - Real Source-Backed Reference Material, Appendix A - Install Commands per Design System, Appendix B - Canonical Sources (read these before reinventing), Appendix C - Apple Liquid Glass: Honest Web Approximation, Apple Liquid Glass (Apple platforms only), Atlassian, Bootstrap, Carbon (+13 more)

### Community 12 - "council.py"
Cohesion: 0.19
Nodes (16): _aggregate_block(), calculate_aggregate_rankings(), _clip(), _debate_block(), _label(), _positions_block(), Any, Four-stage LLM Council orchestration. Stage 1 Positions - every member answers… (+8 more)

### Community 13 - "test_token_budgeting.py"
Cohesion: 0.15
Nodes (15): asyncio, Real, non-mocked tests for Phase 3: Token & Time Budgeting Engine. Tests verify…, Functional test: When cumulative tokens across all models exceed…, Real wall-clock test: When real elapsed time crosses time_limit_seconds, debate…, Integration test: In a 4-round deliberation, when the token budget is capped…, Real HTTP integration test: Verify that FastAPI /api/settings accepts and…, Verify that CouncilRun properly initializes token and time tracking structures., Functional test: When a model exceeds its token_cap_per_model, it must be… (+7 more)

### Community 14 - "get"
Cohesion: 0.11
Nodes (19): export_conversation_report(), export_conversation_zip_archive(), get_conversation(), get_project(), get_provider_keys(), health(), list_conversations(), list_projects() (+11 more)

### Community 15 - "CLAUDE.md - Technical Notes for LLM Council"
Cohesion: 0.14
Nodes (13): Caveman compression, CLAUDE.md - Technical Notes for LLM Council, Custom agents do not work from a project config, graphify, It is the upstream implementation, not a local imitation, Measuring it, Project overview, Sandbox (+5 more)

### Community 16 - "._check_budget_limits"
Cohesion: 0.22
Nodes (5): emit(), Check if any active model has exceeded token_cap_per_model. If exceeded, retire…, Determine if the debate loop should terminate early due to: 1. Total token…, Evict a failing or depleted model immediately and ensure it is never called…, If current chairman is evicted or inactive, fail over to the next highest-…

### Community 17 - "BaseModel"
Cohesion: 0.18
Nodes (11): Conversation, ConversationMetadata, Full conversation with all messages., Request to update a project., Request to update a conversation (project assignment, title, or archive status)., Request to send a message in a conversation., Conversation metadata for list view., SendMessageRequest (+3 more)

### Community 18 - "opencode_client.py"
Cohesion: 0.17
Nodes (14): asyncio, Client for the local opencode server. This module replaces the old OpenRouter…, council_sessions(), main(), post(), End-to-end test of the HTTP API, including the SSE streaming path. Creates a…, Council sessions currently left in the user's opencode session list., Verification script for the opencode client and the council sandbox. Run with:… (+6 more)

### Community 19 - "_sum_tokens"
Cohesion: 0.33
Nodes (5): Total the token counts opencode reported for a set of entries. opencode returns…, Token totals per stage, so the toggle's effect is visible rather than promised.…, _sum_tokens(), Verify token summation logic against realistic OpenCode token telemetry: input…, test_sum_tokens_real_telemetry()

### Community 20 - "storage.py"
Cohesion: 0.19
Nodes (8): Configuration for the LLM Council. The council runs entirely on models that are…, Hybrid Council transport and unified model registry. Seamlessly combines local…, Secure in-memory and environment-backed provider API key management. Supports…, JSON-based storage for conversations., datetime, dotenv, os, typing

### Community 21 - "test_hybrid_providers.py"
Cohesion: 0.16
Nodes (12): LLM Council backend package., Live test script executing an end-to-end deliberation across real OpenCode…, httpx, io, json, pytest, Unit tests for Phase 9: Clean Conversation Lifecycle & Persisted Council…, Tests for conversation ID exposure, markdown report export, and zip bundle… (+4 more)

### Community 22 - "CouncilRun"
Cohesion: 0.17
Nodes (5): CouncilRun, One council deliberation, owning every session it creates., Inject human operator guidance and resources into the ongoing deliberation., Run one prompt across the live sessions in parallel., Re-scope every member's permissions, ignoring individual failures.

### Community 23 - "4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)"
Cohesion: 0.17
Nodes (12): 4.10 Quotes & Testimonials, 4.11 Page Theme Lock (Light / Dark Mode Consistency), 4.1 Typography, 4.2 Color Calibration, 4.3 Layout Diversification, 4.4 Materiality, Shadows, Cards, 4.5 Interactive UI States, 4.6 Data & Form Patterns (+4 more)

### Community 24 - "verify_caveman.py"
Cohesion: 0.26
Nodes (11): council_permissions(), Build the permission ruleset for council members. Allow the research and read…, council_sessions(), main(), _median(), one_shot(), part_one(), part_two() (+3 more)

### Community 25 - "delete_conversation"
Cohesion: 0.40
Nodes (5): delete_conversation(), delete_project(), Delete a project folder and revert its debates to independent mode., Delete a conversation by ID., delete

### Community 26 - "HybridCouncilSession"
Cohesion: 0.18
Nodes (6): _call_make(), AsyncClient, Determine thinking quality / reasoning effort per model: - Honored if…, Create one session per member with resolved thinking quality. Returns the…, HybridCouncilSession, Unified session wrapper routing to either local OpenCode daemon or direct…

### Community 27 - "Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine"
Cohesion: 0.10
Nodes (20): 1. Prerequisites, 2. Start OpenCode Service, 3. Clone & Install, 4. Launch the Platform, Can I still use commercial models like Claude 3.5 Sonnet, GPT-4o, or DeepSeek R1?, Citation, Comparison: Upstream Concept vs. Free LLM Council, Configuration & BYOK Cloud Providers (+12 more)

### Community 28 - "4. Component Standards"
Cohesion: 0.17
Nodes (11): 1. Dials & Atmosphere, 2. Color Palette & Surface Elevation, 3. Typography & Micro-Hierarchy, 4. Component Standards, 5. Performance, Ergonomics & Fast Handling, A. Left-Hand Sidebar (Workspace Tree), Accents & Signal Colors, C. Live RunRail (Real-Time Progress) (+3 more)

### Community 29 - "get_server_password"
Cohesion: 0.18
Nodes (11): diagnose_connection(), get_server_password(), Path, Actively inspect the connection to the OpenCode server and return a detailed…, Possible locations of opencode's service.json., Resolve the opencode server password. Order: OPENCODE_SERVER_PASSWORD env var,…, _service_config_candidates(), Password should be resolved from service.json candidate directories. (+3 more)

### Community 30 - "list_models"
Cohesion: 0.11
Nodes (22): generate_conversation_title(), parse_ranking_from_text(), Short title for a conversation, using the fastest available model., Extract the ordered labels from a 'FINAL RANKING:' block., ask_many(), _auth_headers(), get_server_url(), list_models() (+14 more)

### Community 34 - "10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)"
Cohesion: 0.20
Nodes (10): 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know), Animation Library Choice, Cards & Containers, Galleries & Media, Hero Paradigms, Layout & Grids, Micro-Interactions & Effects, Navigation & Menus (+2 more)

### Community 36 - "list_unified_models"
Cohesion: 0.22
Nodes (8): list_unified_models(), Any, Return all available models across local OpenCode and configured external…, get_models(), The council roster, read live from OpenCode and configured custom providers., OpencodeUnavailable, Raised when the local opencode server cannot be reached., RuntimeError

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
Cohesion: 0.07
Nodes (36): get_settings(), Current council settings, plus whether the official Caveman skill is installed.…, Send a message and run the full four-stage council. Returns the complete…, send_message(), get_debate_mode(), get_settings(), get_time_limit_seconds(), get_token_budget_total() (+28 more)

### Community 42 - "get_active_run"
Cohesion: 0.33
Nodes (6): get_active_run(), Retrieve the active CouncilRun for a conversation ID, if any., Inject human operator guidance and resources into an ongoing deliberation., Request to inject human operator guidance into an ongoing debate., steer_conversation(), SteerRequest

### Community 43 - "6. PERFORMANCE & ACCESSIBILITY GUARDRAILS"
Cohesion: 0.29
Nodes (7): 6.A Hardware Acceleration, 6.B Reduced Motion (mandatory), 6.C Dark Mode (mandatory for any consumer-facing page), 6.D Core Web Vitals Targets, 6.E DOM Cost, 6.F Z-Index Restraint, 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS

### Community 44 - "._collect_new_messages"
Cohesion: 0.38
Nodes (5): _parse_assistant_message(), Any, Flatten an opencode assistant message into text / reasoning / tool calls., Read the session's own outcome flag. opencode reports a failed agent loop as…, Read the assistant messages produced since the last prompt.

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

### Community 50 - "create_project"
Cohesion: 0.50
Nodes (4): create_project(), CreateProjectRequest, Create a new project workspace folder., Request to create a new project workspace folder.

### Community 51 - "post_provider_key"
Cohesion: 0.50
Nodes (4): post_provider_key(), ProviderKeyUpdate, Payload to configure or remove a provider API key., Update or remove a provider API key dynamically.

### Community 56 - "test_human_steering.py"
Cohesion: 0.06
Nodes (35): Register an ongoing CouncilRun by conversation ID., Unregister an ongoing CouncilRun by conversation ID., register_active_run(), unregister_active_run(), Send a message and stream the council as it runs. Emits Server-Sent Events as…, send_message_stream(), emit(), event_generator() (+27 more)

### Community 66 - "graphify.js"
Cohesion: 0.40
Nodes (3): IMPORTANT: keep the reminder string free of backticks and $(...) constructs., ref_fs, ref_path

### Community 69 - "React + Vite"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

### Community 76 - "backend/main.py"
Cohesion: 0.18
Nodes (11): create_conversation(), CreateConversationRequest, FastAPI backend for LLM Council., Create a new conversation., Request to create a new conversation., fastapi, fastapi_middleware_cors, fastapi_responses (+3 more)

### Community 77 - "test_projects_and_folders.py"
Cohesion: 0.28
Nodes (8): asyncio, Unit and integration tests for Phase 10: Projects & Workspace Folder Hierarchy., Verify creating debate directly in project, moving between projects, and…, Verify HTTP API PATCH endpoint for renaming and archiving conversations., HTTP API integration tests for /api/projects and /api/conversations/{id}., test_conversation_archive_and_rename_api(), test_create_conversation_with_project_and_move_lifecycle(), test_projects_http_api()

### Community 82 - "post_settings"
Cohesion: 0.50
Nodes (4): post_settings(), Change live council settings. Takes effect on the next debate round., Live settings the user can change while a run is in flight., SettingsUpdate

## Knowledge Gaps
- **158 isolated node(s):** `name`, `private`, `version`, `type`, `dev` (+153 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 441 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CLAUDE.md - Technical Notes for LLM Council` connect `CLAUDE.md - Technical Notes for LLM Council` to `test_human_steering.py`, `CouncilSession`, `icons.jsx`, `list_models`?**
  _High betweenness centrality (0.211) - this node is a cross-community bridge._
- **Why does `CouncilRun` connect `CouncilRun` to `CouncilSession`, `get_key_statuses`, `test_thinking_quality_and_deduplication.py`, `test_model_eviction.py`, `caveman.py`, `settings.py`, `.run_stream`, `test_chairman_selection.py`, `council.py`, `backend/main.py`, `test_token_budgeting.py`, `._check_budget_limits`, `_sum_tokens`, `test_hybrid_providers.py`, `test_human_steering.py`, `verify_caveman.py`, `HybridCouncilSession`, `list_models`?**
  _High betweenness centrality (0.206) - this node is a cross-community bridge._
- **Why does `Frontend` connect `icons.jsx` to `CLAUDE.md - Technical Notes for LLM Council`?**
  _High betweenness centrality (0.197) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `CouncilRun` (e.g. with `HybridCouncilSession` and `CouncilSession`) actually correct?**
  _`CouncilRun` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `CouncilSession` (e.g. with `CouncilRun` and `HybridCouncilSession`) actually correct?**
  _`CouncilSession` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _158 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `get_conversation` be split into smaller, more focused modules?**
  _Cohesion score 0.0525879917184265 - nodes in this community are weakly interconnected._