# Graph Report - free-llm-council  (2026-10-07)

## Corpus Check
- 67 files · ~66,353 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 21 file(s) not represented in the graph (top: .css 15, (none) 4, .cff 1)

## Summary
- 881 nodes · 1722 edges · 64 communities (50 shown, 14 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 57 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8970624d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Any
- CouncilSession
- icons.jsx
- council.py
- asyncio
- package.json
- get
- test_hybrid_providers.py
- caveman.py
- test_chairman_selection.py
- test_clean_lifecycle_and_presets.py
- Appendix B - Canonical Sources (read these before reinventing)
- ._ask_all
- test_diagnose_connection_detects_port_conflict
- backend/main.py
- get_conversation
- list_models
- test_model_eviction.py
- opencode_client.py
- storage.py
- provider_keys.py
- asyncio
- verify_caveman.py
- 4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)
- CLAUDE.md - Technical Notes for LLM Council
- create_conversation
- HybridCouncilSession
- Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine
- 4. Component Standards
- OpencodeUnavailable
- ._tighten
- start.sh
- tests/__init__.py
- 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)
- test_conversation_archive_and_rename_api
- tasteskill: Anti-Slop Frontend Skill
- 9. AI TELLS (Forbidden Patterns)
- 11. REDESIGN PROTOCOL
- 3. DEFAULT ARCHITECTURE & CONVENTIONS
- settings.py
- test_model_formatting_preserves_distinct_variants
- 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS
- test_sum_tokens_real_telemetry
- 0. BRIEF INFERENCE (Read the Room Before Anything Else)
- 12. THE BLOCK LIBRARY (Contract - Implementations Land Here Iteratively)
- 5. CONTEXT-AWARE PROACTIVITY
- 8. DARK MODE PROTOCOL
- 7. DIAL DEFINITIONS (Technical Reference)
- test_exports_and_conversation_id.py
- asyncio
- git-workflow.md
- free-llm-council
- Any
- test_human_steering.py
- CouncilRun
- ._open_sessions
- update_conversation
- graphify.js
- React + Vite
- AGENTS.md
- rules/graphify.md
- workflows/graphify.md

## God Nodes (most connected - your core abstractions)
1. `CouncilRun` - 57 edges
2. `CouncilSession` - 27 edges
3. `Sidebar()` - 21 edges
4. `get_conversation()` - 20 edges
5. `react` - 16 edges
6. `list_models()` - 16 edges
7. `tasteskill: Anti-Slop Frontend Skill` - 16 edges
8. `HybridCouncilSession` - 15 edges
9. `Appendix B - Canonical Sources (read these before reinventing)` - 15 edges
10. `ReportModal()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Backend structure` --references--> `CouncilSession`  [INFERRED]
  CLAUDE.md → backend/opencode_client.py
- `Backend structure` --references--> `CouncilRun`  [INFERRED]
  CLAUDE.md → backend/council.py
- `Common gotchas` --references--> `_auth_headers()`  [INFERRED]
  CLAUDE.md → backend/opencode_client.py
- `Backend structure` --references--> `get_server_password()`  [INFERRED]
  CLAUDE.md → backend/opencode_client.py
- `Backend structure` --references--> `calculate_aggregate_rankings()`  [INFERRED]
  CLAUDE.md → backend/council.py

## Import Cycles
- None detected.

## Communities (64 total, 14 thin omitted)

### Community 0 - "Any"
Cohesion: 0.18
Nodes (20): Any, create_project(), delete_project(), ensure_data_dir(), get_project(), get_projects_file(), list_projects(), load_all_projects() (+12 more)

### Community 1 - "CouncilSession"
Cohesion: 0.16
Nodes (14): CouncilSession, _parse_assistant_message(), Any, Flatten an opencode assistant message into text / reasoning / tool calls., One opencode session driven by one council member. The session is reused across…, Create the underlying opencode session., Delete the opencode session so it does not clutter the user's list., Replace this session's permission ruleset mid-run. Used to tighten the sandbox… (+6 more)

### Community 2 - "icons.jsx"
Cohesion: 0.08
Nodes (62): Frontend, B. Workspace Header & Breadcrumbs, api, App(), ChatInterface(), DebateMode(), LEVEL_LABELS, AlertTriangle() (+54 more)

### Community 3 - "council.py"
Cohesion: 0.15
Nodes (19): _aggregate_block(), calculate_aggregate_rankings(), _clip(), _debate_block(), _label(), _positions_block(), Any, Four-stage LLM Council orchestration. Stage 1 Positions - every member answers… (+11 more)

### Community 4 - "asyncio"
Cohesion: 0.22
Nodes (9): asyncio, Verify CouncilRun defaults the Chairman to max thinking and regular members to…, Verify user overrides for thinking quality are honored over defaults., Verify list_models includes variants list and deduplicates identical IDs., Verify CouncilSession includes variant in the model specification object., test_council_run_defaults_chairman_to_max_thinking(), test_council_run_honors_user_thinking_overrides(), test_council_session_transmits_variant_in_payload() (+1 more)

### Community 5 - "package.json"
Cohesion: 0.06
Nodes (36): allowScripts, esbuild@0.25.12, dependencies, react, react-dom, react-markdown, remark-gfm, devDependencies (+28 more)

### Community 6 - "get"
Cohesion: 0.22
Nodes (9): export_conversation_zip_archive(), get_conversation(), get_project(), list_projects(), List all project folders with metadata and debate counts., Get details for a specific project., Get a specific conversation with all its messages., Export the entire council discussion as a downloadable ZIP package containing… (+1 more)

### Community 7 - "test_hybrid_providers.py"
Cohesion: 0.10
Nodes (21): Hybrid Council transport and unified model registry. Seamlessly combines local…, LLM Council backend package., httpx, pytest, Real, non-mocked tests for Phase 5: Caveman Max Mode & Debate Compression.…, Ensure 'max' is recognized as a first-class debate compression level., test_caveman_levels_includes_max(), Real, non-mocked tests for Phase 6: Hybrid Provider & Custom API Key Ingestion.… (+13 more)

### Community 8 - "caveman.py"
Cohesion: 0.12
Nodes (22): build_instruction(), intensity_for(), is_installed(), load_skill(), Path, Official Caveman compression, loaded at runtime from the installed skill.…, Return the text under '## <heading>', up to the next '## '., Pull one level's row out of Caveman's own Intensity table. Keeping this parsed… (+14 more)

### Community 9 - "test_chairman_selection.py"
Cohesion: 0.09
Nodes (28): Any, Intelligent capability scoring matrix for LLM Council Chairman election. Ranks…, Select the highest capability model ID from a list of model dicts or model IDs., Compute an intelligence score (0 to 100+) for a given model dict or model ID…, score_model_capability(), select_best_chairman(), Work out who sits on the council and who chairs it. Defaults to every model…, resolve_roster() (+20 more)

### Community 10 - "test_clean_lifecycle_and_presets.py"
Cohesion: 0.18
Nodes (10): list_conversations(), List all conversations (metadata only)., list_conversations(), List all conversations (metadata only). By default, empty conversations (0…, asyncio, Unit tests for Phase 9: Clean Conversation Lifecycle & Persisted Council…, Verify DELETE /api/conversations/{id} deletes conversation and handles 404 for…, Verify list_conversations does not return phantom empty conversations. (+2 more)

### Community 11 - "Appendix B - Canonical Sources (read these before reinventing)"
Cohesion: 0.09
Nodes (21): APPENDICES - Real Source-Backed Reference Material, Appendix A - Install Commands per Design System, Appendix B - Canonical Sources (read these before reinventing), Appendix C - Apple Liquid Glass: Honest Web Approximation, Apple Liquid Glass (Apple platforms only), Atlassian, Bootstrap, Carbon (+13 more)

### Community 13 - "test_diagnose_connection_detects_port_conflict"
Cohesion: 0.40
Nodes (5): asyncio, If a port is open but occupied by another process (e.g. Kilo on 4096),…, FastAPI /api/health endpoint should report OpenCode connection and diagnostics., test_diagnose_connection_detects_port_conflict(), test_health_endpoint_returns_diagnostics()

### Community 14 - "backend/main.py"
Cohesion: 0.05
Nodes (51): get_active_run(), Retrieve the active CouncilRun for a conversation ID, if any., Conversation, ConversationMetadata, create_conversation(), create_project(), CreateConversationRequest, CreateProjectRequest (+43 more)

### Community 15 - "get_conversation"
Cohesion: 0.13
Nodes (23): Send a message and run the full four-stage council. Returns the complete…, send_message(), add_assistant_message(), add_user_message(), get_conversation(), prune_empty_conversations(), Prune all abandoned conversations that have 0 messages. Args: except_id:…, Add a user message to a conversation. Args: conversation_id: Conversation… (+15 more)

### Community 16 - "list_models"
Cohesion: 0.14
Nodes (19): parse_ranking_from_text(), Extract the ordered labels from a 'FINAL RANKING:' block., ask_many(), _auth_headers(), get_server_url(), list_models(), _location_params(), opencode_request() (+11 more)

### Community 17 - "test_model_eviction.py"
Cohesion: 0.18
Nodes (13): make_mock_session(), asyncio, Unit tests for Phase 2: Dynamic Member Fault-Tolerance & Model Eviction., If a model succeeds in Stage 1 but crashes in Debate Round 1, it must be…, Create a mock CouncilSession that records ask() calls and session lifecycle., If the designated chairman fails during deliberation, the council must promote…, When run_stream is used, an eviction should emit a 'model_evicted' event., If a model fails in Stage 1, it must be evicted immediately and NEVER called… (+5 more)

### Community 18 - "opencode_client.py"
Cohesion: 0.17
Nodes (13): asyncio, Configuration for the LLM Council. The council runs entirely on models that are…, Client for the local opencode server. This module replaces the old OpenRouter…, End-to-end test of the HTTP API, including the SSE streaming path. Creates a…, Verification script for the opencode client and the council sandbox. Run with:…, base64, dotenv, os (+5 more)

### Community 19 - "storage.py"
Cohesion: 0.13
Nodes (20): export_conversation_report(), get_conversation_reports(), Export a council deliberation as a formatted Markdown report document…, Return pre-rendered executive and detailed reports with deliberation metadata…, _clean_table_cell(), export_conversation_zip(), format_conversation_detailed(), format_conversation_executive() (+12 more)

### Community 20 - "provider_keys.py"
Cohesion: 0.12
Nodes (25): list_unified_models(), Return all available models across local OpenCode and configured external…, delete_key(), _get_env_key(), get_key(), get_key_statuses(), _init_from_env(), Any (+17 more)

### Community 21 - "asyncio"
Cohesion: 0.17
Nodes (11): asyncio, Functional test: When cumulative tokens across all models exceed…, Real wall-clock test: When real elapsed time crosses time_limit_seconds, debate…, Integration test: In a 4-round deliberation, when the token budget is capped…, Real HTTP integration test: Verify that FastAPI /api/settings accepts and…, Functional test: When a model exceeds its token_cap_per_model, it must be…, test_council_run_retires_model_exceeding_token_cap(), test_council_run_stops_debate_when_global_budget_exhausted() (+3 more)

### Community 22 - "verify_caveman.py"
Cohesion: 0.26
Nodes (11): council_permissions(), Build the permission ruleset for council members. Allow the research and read…, council_sessions(), main(), _median(), one_shot(), part_one(), part_two() (+3 more)

### Community 23 - "4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)"
Cohesion: 0.17
Nodes (12): 4.10 Quotes & Testimonials, 4.11 Page Theme Lock (Light / Dark Mode Consistency), 4.1 Typography, 4.2 Color Calibration, 4.3 Layout Diversification, 4.4 Materiality, Shadows, Cards, 4.5 Interactive UI States, 4.6 Data & Form Patterns (+4 more)

### Community 24 - "CLAUDE.md - Technical Notes for LLM Council"
Cohesion: 0.18
Nodes (10): parse_verdict(), Split a chairman response into its sections. Falls back to putting everything…, CLAUDE.md - Technical Notes for LLM Council, Custom agents do not work from a project config, graphify, Project overview, Prompt design, Sandbox (+2 more)

### Community 25 - "create_conversation"
Cohesion: 0.17
Nodes (13): delete_conversation(), delete_project(), Delete a project folder and revert its debates to independent mode., Delete a conversation by ID., create_conversation(), delete_conversation(), get_conversation_path(), Get the file path for a conversation. (+5 more)

### Community 26 - "HybridCouncilSession"
Cohesion: 0.22
Nodes (4): HybridCouncilSession, Any, AsyncClient, Unified session wrapper routing to either local OpenCode daemon or direct…

### Community 27 - "Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine"
Cohesion: 0.10
Nodes (20): 1. Prerequisites, 2. Start OpenCode Service, 3. Clone & Install, 4. Launch the Platform, Can I still use commercial models like Claude 3.5 Sonnet, GPT-4o, or DeepSeek R1?, Citation, Comparison: Upstream Concept vs. Free LLM Council, Configuration & BYOK Cloud Providers (+12 more)

### Community 28 - "4. Component Standards"
Cohesion: 0.17
Nodes (11): 1. Dials & Atmosphere, 2. Color Palette & Surface Elevation, 3. Typography & Micro-Hierarchy, 4. Component Standards, 5. Performance, Ergonomics & Fast Handling, A. Left-Hand Sidebar (Workspace Tree), Accents & Signal Colors, C. Live RunRail (Real-Time Progress) (+3 more)

### Community 29 - "OpencodeUnavailable"
Cohesion: 0.20
Nodes (10): diagnose_connection(), get_server_password(), OpencodeUnavailable, Path, Actively inspect the connection to the OpenCode server and return a detailed…, Raised when the local opencode server cannot be reached., Possible locations of opencode's service.json., Resolve the opencode server password. Order: OPENCODE_SERVER_PASSWORD env var,… (+2 more)

### Community 34 - "10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)"
Cohesion: 0.20
Nodes (10): 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know), Animation Library Choice, Cards & Containers, Galleries & Media, Hero Paradigms, Layout & Grids, Micro-Interactions & Effects, Navigation & Menus (+2 more)

### Community 36 - "test_conversation_archive_and_rename_api"
Cohesion: 0.29
Nodes (7): asyncio, Verify creating debate directly in project, moving between projects, and…, Verify HTTP API PATCH endpoint for renaming and archiving conversations., HTTP API integration tests for /api/projects and /api/conversations/{id}., test_conversation_archive_and_rename_api(), test_create_conversation_with_project_and_move_lifecycle(), test_projects_http_api()

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
Nodes (34): get_settings(), Current council settings, plus whether the official Caveman skill is installed.…, get_debate_mode(), get_settings(), get_time_limit_seconds(), get_token_budget_total(), get_token_cap_per_model(), Any (+26 more)

### Community 43 - "6. PERFORMANCE & ACCESSIBILITY GUARDRAILS"
Cohesion: 0.29
Nodes (7): 6.A Hardware Acceleration, 6.B Reduced Motion (mandatory), 6.C Dark Mode (mandatory for any consumer-facing page), 6.D Core Web Vitals Targets, 6.E DOM Cost, 6.F Z-Index Restraint, 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS

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

### Community 50 - "test_exports_and_conversation_id.py"
Cohesion: 0.18
Nodes (8): Live test script executing an end-to-end deliberation across real OpenCode…, io, json, Tests for conversation ID exposure, markdown report export, and zip bundle…, Verify in-memory zip archive packages executive-report.md, detailed-report.md,…, test_export_conversation_zip_archive(), time, zipfile

### Community 51 - "asyncio"
Cohesion: 0.25
Nodes (7): asyncio, HybridCouncilSession dispatches OpenCode models to CouncilSession, and keyed…, If an external keyed model fails with 401 Unauthorized (invalid key/no…, HTTP integration test: GET /api/providers/keys POST /api/providers/keys, test_hybrid_council_session_routing(), test_keyed_model_401_triggers_immediate_eviction(), test_provider_keys_http_api()

### Community 56 - "test_human_steering.py"
Cohesion: 0.06
Nodes (36): generate_conversation_title(), Short title for a conversation, using the fastest available model., Register an ongoing CouncilRun by conversation ID., Unregister an ongoing CouncilRun by conversation ID., register_active_run(), unregister_active_run(), Send a message and stream the council as it runs. Emits Server-Sent Events as…, send_message_stream() (+28 more)

### Community 57 - "CouncilRun"
Cohesion: 0.11
Nodes (13): CouncilRun, emit(), One council deliberation, owning every session it creates., Inject human operator guidance and resources into the ongoing deliberation., Check if any active model has exceeded token_cap_per_model. If exceeded, retire…, Determine if the debate loop should terminate early due to: 1. Total token…, Evict a failing or depleted model immediately and ensure it is never called…, If current chairman is evicted or inactive, fail over to the next highest-… (+5 more)

### Community 58 - "._open_sessions"
Cohesion: 0.33
Nodes (4): _call_make(), AsyncClient, Determine thinking quality / reasoning effort per model: - Honored if…, Create one session per member with resolved thinking quality. Returns the…

### Community 62 - "update_conversation"
Cohesion: 0.29
Nodes (7): Update a project name or description., Update conversation metadata such as title or assigned project folder., update_conversation(), update_project(), assign_conversation_project(), Assign or unassign a conversation to/from a project folder., patch

### Community 66 - "graphify.js"
Cohesion: 0.40
Nodes (3): IMPORTANT: keep the reminder string free of backticks and $(...) constructs., ref_fs, ref_path

### Community 69 - "React + Vite"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

## Knowledge Gaps
- **162 isolated node(s):** `name`, `private`, `version`, `type`, `dev` (+157 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 458 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CLAUDE.md - Technical Notes for LLM Council` connect `CLAUDE.md - Technical Notes for LLM Council` to `list_models`, `caveman.py`, `icons.jsx`, `CouncilSession`?**
  _High betweenness centrality (0.221) - this node is a cross-community bridge._
- **Why does `Frontend` connect `icons.jsx` to `CLAUDE.md - Technical Notes for LLM Council`?**
  _High betweenness centrality (0.208) - this node is a cross-community bridge._
- **Why does `CouncilRun` connect `CouncilRun` to `CouncilSession`, `council.py`, `._open_sessions`, `asyncio`, `test_hybrid_providers.py`, `settings.py`, `test_chairman_selection.py`, `._ask_all`, `backend/main.py`, `list_models`, `test_model_eviction.py`, `asyncio`, `asyncio`, `verify_caveman.py`, `test_human_steering.py`, `HybridCouncilSession`, `._tighten`?**
  _High betweenness centrality (0.204) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `CouncilRun` (e.g. with `HybridCouncilSession` and `CouncilSession`) actually correct?**
  _`CouncilRun` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `CouncilSession` (e.g. with `CouncilRun` and `HybridCouncilSession`) actually correct?**
  _`CouncilSession` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _162 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `icons.jsx` be split into smaller, more focused modules?**
  _Cohesion score 0.07858861267040898 - nodes in this community are weakly interconnected._