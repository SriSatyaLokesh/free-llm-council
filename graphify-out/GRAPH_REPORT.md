# Graph Report - free-llm-council  (2026-10-12)

## Corpus Check
- 75 files · ~85,097 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 24 file(s) not represented in the graph (top: .css 17, (none) 4, .cff 1)

## Summary
- 974 nodes · 1945 edges · 67 communities (55 shown, 12 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 61 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `19a5f532`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- storage.py
- CouncilSession
- icons.jsx
- council.py
- create_project
- frontend/package.json
- test_opencode_discovery.py
- test_security_hardening.py
- verify_caveman.py
- test_chairman_selection.py
- delete_conversation
- Appendix B - Canonical Sources (read these before reinventing)
- _auth_headers
- test_human_steering.py
- backend/main.py
- get_conversation
- landing/package.json
- BaseModel
- settings.py
- format_conversation_detailed
- test_hybrid_providers.py
- test_token_budgeting.py
- .__init__
- 4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)
- list_models
- get_active_run
- post
- Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine
- 4. Component Standards
- test_exports_and_conversation_id.py
- start.sh script
- tests/__init__.py
- 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)
- test_projects_and_folders.py
- tasteskill: Anti-Slop Frontend Skill
- 9. AI TELLS (Forbidden Patterns)
- 11. REDESIGN PROTOCOL
- 3. DEFAULT ARCHITECTURE & CONVENTIONS
- HybridCouncilSession
- value_error_handler
- 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS
- test_clean_lifecycle_and_presets.py
- 0. BRIEF INFERENCE (Read the Room Before Anything Else)
- 12. THE BLOCK LIBRARY (Contract - Implementations Land Here Iteratively)
- 5. CONTEXT-AWARE PROACTIVITY
- 8. DARK MODE PROTOCOL
- 7. DIAL DEFINITIONS (Technical Reference)
- get
- git-workflow.md
- free-llm-council
- list_conversations
- verify_api.py
- post_settings
- opencode_client.py
- test_non_reporting_agents.py
- update_project
- test_caveman_max.py
- graphify.js
- CouncilRun
- React + Vite
- AGENTS.md
- rules/graphify.md
- workflows/graphify.md

## God Nodes (most connected - your core abstractions)
1. `CouncilRun` - 60 edges
2. `CouncilSession` - 27 edges
3. `ChatInterface()` - 23 edges
4. `get_conversation()` - 22 edges
5. `Sidebar()` - 21 edges
6. `react` - 18 edges
7. `ReportPage()` - 17 edges
8. `list_models()` - 17 edges
9. `tasteskill: Anti-Slop Frontend Skill` - 16 edges
10. `HybridCouncilSession` - 15 edges

## Surprising Connections (you probably didn't know these)
- `Backend structure` --references--> `CouncilSession`  [INFERRED]
  CLAUDE.md → backend/opencode_client.py
- `Common gotchas` --references--> `CouncilSession`  [INFERRED]
  CLAUDE.md → backend/opencode_client.py
- `Backend structure` --references--> `CouncilRun`  [INFERRED]
  CLAUDE.md → backend/council.py
- `Backend structure` --references--> `parse_verdict()`  [INFERRED]
  CLAUDE.md → backend/prompts.py
- `Frontend` --references--> `ProcessPanel()`  [INFERRED]
  CLAUDE.md → frontend/src/components/ProcessPanel.jsx

## Import Cycles
- None detected.

## Communities (67 total, 12 thin omitted)

### Community 0 - "storage.py"
Cohesion: 0.14
Nodes (27): create_project(), delete_project(), ensure_data_dir(), get_project(), get_projects_file(), list_projects(), load_all_projects(), prune_empty_conversations() (+19 more)

### Community 1 - "CouncilSession"
Cohesion: 0.16
Nodes (13): CouncilSession, _parse_assistant_message(), Any, Flatten an opencode assistant message into text / reasoning / tool calls., One opencode session driven by one council member. The session is reused across…, Create the underlying opencode session., Delete the opencode session so it does not clutter the user's list., Replace this session's permission ruleset mid-run. Used to tighten the sandbox… (+5 more)

### Community 2 - "icons.jsx"
Cohesion: 0.07
Nodes (71): B. Workspace Header & Breadcrumbs, api, App(), ChatInterface(), DebateMode(), LEVEL_LABELS, ErrorBoundary, AlertTriangle() (+63 more)

### Community 3 - "council.py"
Cohesion: 0.12
Nodes (20): _aggregate_block(), calculate_aggregate_rankings(), _clip(), _debate_block(), _label(), _positions_block(), Any, Four-stage LLM Council orchestration. Stage 1 Positions - every member answers… (+12 more)

### Community 4 - "create_project"
Cohesion: 0.50
Nodes (4): create_project(), CreateProjectRequest, Create a new project workspace folder., Request to create a new project workspace folder.

### Community 5 - "frontend/package.json"
Cohesion: 0.06
Nodes (37): allowScripts, esbuild@0.25.12, dependencies, react, react-dom, react-markdown, remark-gfm, devDependencies (+29 more)

### Community 6 - "test_opencode_discovery.py"
Cohesion: 0.12
Nodes (16): asyncio, Unit tests for OpenCode discovery, port resilience, and health diagnostics., If opencode is not responding, ensure_opencode_running runs opencode service…, OPENCODE_SERVER_URL env var should override all detection., Dynamic port from 'opencode service status' should be extracted cleanly., Password should be resolved from service.json candidate directories., When no service.json exists, an informative OpencodeUnavailable error is raised., If a port is open but occupied by another process (e.g. Kilo on 4096),… (+8 more)

### Community 7 - "test_security_hardening.py"
Cohesion: 0.07
Nodes (30): make_mock_session(), asyncio, Unit tests for Phase 2: Dynamic Member Fault-Tolerance & Model Eviction., If a model succeeds in Stage 1 but crashes in Debate Round 1, it must be…, Create a mock CouncilSession that records ask() calls and session lifecycle., If the designated chairman fails during deliberation, the council must promote…, When run_stream is used, an eviction should emit a 'model_evicted' event., If a model fails in Stage 1, it must be evicted immediately and NEVER called… (+22 more)

### Community 8 - "verify_caveman.py"
Cohesion: 0.06
Nodes (43): build_instruction(), intensity_for(), is_installed(), load_skill(), Path, Official Caveman compression, loaded at runtime from the installed skill.…, Return the text under '## <heading>', up to the next '## '., Pull one level's row out of Caveman's own Intensity table. Keeping this parsed… (+35 more)

### Community 9 - "test_chairman_selection.py"
Cohesion: 0.09
Nodes (28): Any, Intelligent capability scoring matrix for LLM Council Chairman election. Ranks…, Select the highest capability model ID from a list of model dicts or model IDs., Compute an intelligence score (0 to 100+) for a given model dict or model ID…, score_model_capability(), select_best_chairman(), Work out who sits on the council and who chairs it. Defaults to every model…, resolve_roster() (+20 more)

### Community 10 - "delete_conversation"
Cohesion: 0.40
Nodes (5): delete_conversation(), delete_project(), Delete a project folder and revert its debates to independent mode., Delete a conversation by ID., delete

### Community 11 - "Appendix B - Canonical Sources (read these before reinventing)"
Cohesion: 0.09
Nodes (21): APPENDICES - Real Source-Backed Reference Material, Appendix A - Install Commands per Design System, Appendix B - Canonical Sources (read these before reinventing), Appendix C - Apple Liquid Glass: Honest Web Approximation, Apple Liquid Glass (Apple platforms only), Atlassian, Bootstrap, Carbon (+13 more)

### Community 12 - "_auth_headers"
Cohesion: 0.50
Nodes (3): _auth_headers(), AsyncClient, Common gotchas

### Community 13 - "test_human_steering.py"
Cohesion: 0.06
Nodes (39): generate_conversation_title(), Short title for a conversation, using the fastest available model., Register an ongoing CouncilRun by conversation ID., Unregister an ongoing CouncilRun by conversation ID., register_active_run(), unregister_active_run(), Send a message and stream the council as it runs. Emits Server-Sent Events as…, send_message_stream() (+31 more)

### Community 14 - "backend/main.py"
Cohesion: 0.12
Nodes (16): get_provider_keys(), health(), lifespan(), FastAPI backend for LLM Council., Health check endpoint., Detailed health check validating connection to OpenCode and BYOK readiness., Get status and redacted preview of configured provider API keys., Lifecycle hook: automatically starts and verifies OpenCode service on server… (+8 more)

### Community 15 - "get_conversation"
Cohesion: 0.10
Nodes (35): Update conversation metadata such as title or assigned project folder., update_conversation(), add_assistant_message(), add_user_message(), assign_conversation_project(), create_conversation(), delete_conversation(), get_conversation() (+27 more)

### Community 16 - "landing/package.json"
Cohesion: 0.17
Nodes (11): devDependencies, vite, vite, name, private, scripts, build, dev (+3 more)

### Community 17 - "BaseModel"
Cohesion: 0.18
Nodes (11): Conversation, ConversationMetadata, Conversation metadata for list view., Full conversation with all messages., Request to update a project., Request to update a conversation (project assignment, title, or archive status)., Request to send a message in a conversation., SendMessageRequest (+3 more)

### Community 18 - "settings.py"
Cohesion: 0.07
Nodes (36): get_settings(), Current council settings, plus whether the official Caveman skill is installed.…, Send a message and run the full four-stage council. Returns the complete…, send_message(), get_debate_mode(), get_settings(), get_time_limit_seconds(), get_token_budget_total() (+28 more)

### Community 19 - "format_conversation_detailed"
Cohesion: 0.11
Nodes (24): export_conversation_html(), export_conversation_report(), get_conversation_reports(), Export a council deliberation as a formatted Markdown report document…, Export a council deliberation as a standalone publication-grade HTML report., Return pre-rendered executive and detailed reports with deliberation metadata…, _clean_table_cell(), _extract_non_reporting_models() (+16 more)

### Community 20 - "test_hybrid_providers.py"
Cohesion: 0.08
Nodes (36): list_unified_models(), Hybrid Council transport and unified model registry. Seamlessly combines local…, Return all available models across local OpenCode and configured external…, LLM Council backend package., delete_key(), _get_env_key(), get_key(), get_key_statuses() (+28 more)

### Community 21 - "test_token_budgeting.py"
Cohesion: 0.13
Nodes (17): asyncio, Real, non-mocked tests for Phase 3: Token & Time Budgeting Engine. Tests verify…, Functional test: When cumulative tokens across all models exceed…, Real wall-clock test: When real elapsed time crosses time_limit_seconds, debate…, Integration test: In a 4-round deliberation, when the token budget is capped…, Real HTTP integration test: Verify that FastAPI /api/settings accepts and…, Verify token summation logic against realistic OpenCode token telemetry: input…, Verify that CouncilRun properly initializes token and time tracking structures. (+9 more)

### Community 23 - "4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)"
Cohesion: 0.17
Nodes (12): 4.10 Quotes & Testimonials, 4.11 Page Theme Lock (Light / Dark Mode Consistency), 4.1 Typography, 4.2 Color Calibration, 4.3 Layout Diversification, 4.4 Materiality, Shadows, Cards, 4.5 Interactive UI States, 4.6 Data & Form Patterns (+4 more)

### Community 24 - "list_models"
Cohesion: 0.15
Nodes (18): parse_ranking_from_text(), Extract the ordered labels from a 'FINAL RANKING:' block., ask_many(), ensure_opencode_running(), get_server_url(), is_opencode_responding(), list_models(), opencode_request() (+10 more)

### Community 25 - "get_active_run"
Cohesion: 0.33
Nodes (6): get_active_run(), Retrieve the active CouncilRun for a conversation ID, if any., Inject human operator guidance and resources into an ongoing deliberation., Request to inject human operator guidance into an ongoing debate., steer_conversation(), SteerRequest

### Community 26 - "post"
Cohesion: 0.18
Nodes (11): create_conversation(), CreateConversationRequest, post_provider_key(), ProviderKeyUpdate, prune_empty_conversations(), Payload to configure or remove a provider API key., Update or remove a provider API key dynamically., Create a new conversation. (+3 more)

### Community 27 - "Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine"
Cohesion: 0.10
Nodes (20): 1. Prerequisites, 2. Start OpenCode Service, 3. Clone & Install, 4. Launch the Platform, Can I still use commercial models like Claude 3.5 Sonnet, GPT-4o, or DeepSeek R1?, Citation, Comparison: Upstream Concept vs. Free LLM Council, Configuration & BYOK Cloud Providers (+12 more)

### Community 28 - "4. Component Standards"
Cohesion: 0.17
Nodes (11): 1. Dials & Atmosphere, 2. Color Palette & Surface Elevation, 3. Typography & Micro-Hierarchy, 4. Component Standards, 5. Performance, Ergonomics & Fast Handling, A. Left-Hand Sidebar (Workspace Tree), Accents & Signal Colors, C. Live RunRail (Real-Time Progress) (+3 more)

### Community 30 - "test_exports_and_conversation_id.py"
Cohesion: 0.20
Nodes (7): Live test script executing an end-to-end deliberation across real OpenCode…, io, json, Tests for conversation ID exposure, markdown report export, and zip bundle…, Verify in-memory zip archive packages executive-report.md, detailed-report.md,…, test_export_conversation_zip_archive(), zipfile

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

### Community 41 - "HybridCouncilSession"
Cohesion: 0.15
Nodes (7): _call_make(), AsyncClient, Determine thinking quality / reasoning effort per model: - Honored if…, Create one session per member with resolved thinking quality. Returns the…, HybridCouncilSession, Any, Unified session wrapper routing to either local OpenCode daemon or direct…

### Community 42 - "value_error_handler"
Cohesion: 0.50
Nodes (4): Convert validation and path traversal ValueErrors to clean HTTP 400 responses., value_error_handler(), exception_handler, ValueError

### Community 43 - "6. PERFORMANCE & ACCESSIBILITY GUARDRAILS"
Cohesion: 0.29
Nodes (7): 6.A Hardware Acceleration, 6.B Reduced Motion (mandatory), 6.C Dark Mode (mandatory for any consumer-facing page), 6.D Core Web Vitals Targets, 6.E DOM Cost, 6.F Z-Index Restraint, 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS

### Community 44 - "test_clean_lifecycle_and_presets.py"
Cohesion: 0.40
Nodes (4): asyncio, Unit tests for Phase 9: Clean Conversation Lifecycle & Persisted Council…, Verify DELETE /api/conversations/{id} deletes conversation and handles 404 for…, test_delete_conversation_http_api()

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

### Community 51 - "get"
Cohesion: 0.12
Nodes (17): export_conversation_pdf(), export_conversation_zip_archive(), get_conversation(), get_project(), list_projects(), List all project folders with metadata and debate counts., Get details for a specific project., Get a specific conversation with all its messages. (+9 more)

### Community 54 - "list_conversations"
Cohesion: 0.50
Nodes (4): list_conversations(), List all conversations (metadata only)., list_conversations(), List all conversations (metadata only). By default, empty conversations (0…

### Community 55 - "verify_api.py"
Cohesion: 0.16
Nodes (12): asyncio, Configuration for the LLM Council. The council runs entirely on models that are…, council_sessions(), main(), End-to-end test of the HTTP API, including the SSE streaming path. Creates a…, Council sessions currently left in the user's opencode session list., Verification script for the opencode client and the council sandbox. Run with:…, dotenv (+4 more)

### Community 57 - "post_settings"
Cohesion: 0.50
Nodes (4): post_settings(), Live settings the user can change while a run is in flight., Change live council settings. Takes effect on the next debate round., SettingsUpdate

### Community 58 - "opencode_client.py"
Cohesion: 0.15
Nodes (16): diagnose_connection(), get_server_password(), _location_params(), OpencodeUnavailable, Path, Client for the local opencode server. This module replaces the old OpenRouter…, Every opencode call is scoped to the council's workspace directory., Actively inspect the connection to the OpenCode server and return a detailed… (+8 more)

### Community 59 - "test_non_reporting_agents.py"
Cohesion: 0.29
Nodes (8): make_mock_session(), asyncio, Unit tests for non-reporting agents, upfront report notices, and Phase 1…, If a member cannot initialize session, it is registered as evicted and excluded…, If a member times out in Phase 1, it quits before debate and is excluded from…, test_phase_1_dropout_quits_debate_and_excluded_from_prompts(), test_session_init_failure_evicts_non_reporting_member(), fake_make()

### Community 60 - "update_project"
Cohesion: 0.67
Nodes (3): Update a project name or description., update_project(), patch

### Community 62 - "test_caveman_max.py"
Cohesion: 0.12
Nodes (16): pytest, Real, non-mocked tests for Phase 5: Caveman Max Mode & Debate Compression.…, Ensure 'max' is recognized as a first-class debate compression level., test_caveman_levels_includes_max(), asyncio, Unit tests for Phase 8: Per-Model Thinking Quality & Model Deduplication., Verify distinct models like ling 3.1 and ling 3.0 fin are not collapsed to the…, Verify CouncilRun defaults the Chairman to max thinking and regular members to… (+8 more)

### Community 66 - "graphify.js"
Cohesion: 0.40
Nodes (3): IMPORTANT: keep the reminder string free of backticks and $(...) constructs., ref_fs, ref_path

### Community 68 - "CouncilRun"
Cohesion: 0.11
Nodes (12): CouncilRun, emit(), One council deliberation, owning every session it creates., Inject human operator guidance and resources into the ongoing deliberation., Check if any active model has exceeded token_cap_per_model. If exceeded, retire…, Determine if the debate loop should terminate early due to: 1. Total token…, Evict a failing or depleted model immediately and ensure it is never called…, If current chairman is evicted or inactive, fail over to the next highest-… (+4 more)

### Community 69 - "React + Vite"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

## Knowledge Gaps
- **172 isolated node(s):** `Appendix A - Install Commands per Design System`, `Apple Liquid Glass (Apple platforms only)`, `Atlassian`, `Bootstrap`, `Carbon` (+167 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 505 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CLAUDE.md - Technical Notes for LLM Council` connect `verify_caveman.py` to `list_models`, `_auth_headers`, `test_human_steering.py`?**
  _High betweenness centrality (0.226) - this node is a cross-community bridge._
- **Why does `Frontend` connect `verify_caveman.py` to `icons.jsx`?**
  _High betweenness centrality (0.214) - this node is a cross-community bridge._
- **Why does `CouncilRun` connect `CouncilRun` to `CouncilSession`, `council.py`, `test_security_hardening.py`, `verify_caveman.py`, `HybridCouncilSession`, `test_chairman_selection.py`, `test_human_steering.py`, `backend/main.py`, `settings.py`, `test_hybrid_providers.py`, `test_token_budgeting.py`, `list_models`, `test_non_reporting_agents.py`, `test_caveman_max.py`?**
  _High betweenness centrality (0.203) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `CouncilRun` (e.g. with `HybridCouncilSession` and `CouncilSession`) actually correct?**
  _`CouncilRun` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `CouncilSession` (e.g. with `CouncilRun` and `HybridCouncilSession`) actually correct?**
  _`CouncilSession` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Appendix A - Install Commands per Design System`, `Apple Liquid Glass (Apple platforms only)`, `Atlassian` to the rest of the system?**
  _172 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `storage.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._