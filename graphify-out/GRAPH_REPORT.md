# Graph Report - free-llm-council  (2026-10-07)

## Corpus Check
- 67 files · ~68,350 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 21 file(s) not represented in the graph (top: .css 15, (none) 4, .cff 1)

## Summary
- 894 nodes · 1749 edges · 59 communities (47 shown, 12 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 55 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `df424ca3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Any
- CouncilSession
- icons.jsx
- CouncilRun
- list_models
- package.json
- get
- test_human_steering.py
- caveman.py
- test_chairman_selection.py
- create_conversation
- Appendix B - Canonical Sources (read these before reinventing)
- opencode_client.py
- ._pipeline
- backend/main.py
- get_conversation
- council.py
- verify_caveman.py
- ._open_sessions
- storage.py
- provider_keys.py
- test_token_budgeting.py
- ._tighten
- 4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)
- get_server_url
- delete_conversation
- HybridCouncilSession
- Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine
- 4. Component Standards
- Any
- get_server_password
- start.sh
- tests/__init__.py
- 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)
- test_projects_and_folders.py
- tasteskill: Anti-Slop Frontend Skill
- 9. AI TELLS (Forbidden Patterns)
- 11. REDESIGN PROTOCOL
- 3. DEFAULT ARCHITECTURE & CONVENTIONS
- settings.py
- asyncio
- 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS
- 0. BRIEF INFERENCE (Read the Room Before Anything Else)
- 12. THE BLOCK LIBRARY (Contract - Implementations Land Here Iteratively)
- 5. CONTEXT-AWARE PROACTIVITY
- 8. DARK MODE PROTOCOL
- 7. DIAL DEFINITIONS (Technical Reference)
- test_caveman_max.py
- test_hybrid_providers.py
- git-workflow.md
- free-llm-council
- CLAUDE.md - Technical Notes for LLM Council
- graphify.js
- React + Vite
- AGENTS.md
- rules/graphify.md
- workflows/graphify.md

## God Nodes (most connected - your core abstractions)
1. `CouncilRun` - 56 edges
2. `CouncilSession` - 27 edges
3. `get_conversation()` - 22 edges
4. `Sidebar()` - 21 edges
5. `list_models()` - 16 edges
6. `react` - 16 edges
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
- `Backend structure` --references--> `list_models()`  [INFERRED]
  CLAUDE.md → backend/opencode_client.py
- `Frontend` --references--> `ProcessPanel()`  [INFERRED]
  CLAUDE.md → frontend/src/components/ProcessPanel.jsx

## Import Cycles
- None detected.

## Communities (59 total, 12 thin omitted)

### Community 0 - "Any"
Cohesion: 0.15
Nodes (23): Any, Update a project name or description., update_project(), create_project(), delete_project(), ensure_data_dir(), get_project(), get_projects_file() (+15 more)

### Community 1 - "CouncilSession"
Cohesion: 0.14
Nodes (15): AsyncClient, CouncilSession, _parse_assistant_message(), Any, Flatten an opencode assistant message into text / reasoning / tool calls., One opencode session driven by one council member. The session is reused across…, Create the underlying opencode session., Delete the opencode session so it does not clutter the user's list. (+7 more)

### Community 2 - "icons.jsx"
Cohesion: 0.08
Nodes (61): B. Workspace Header & Breadcrumbs, api, App(), ChatInterface(), DebateMode(), LEVEL_LABELS, AlertTriangle(), Archive() (+53 more)

### Community 3 - "CouncilRun"
Cohesion: 0.13
Nodes (11): CouncilRun, emit(), One council deliberation, owning every session it creates., Inject human operator guidance and resources into the ongoing deliberation., Check if any active model has exceeded token_cap_per_model. If exceeded, retire…, Determine if the debate loop should terminate early due to: 1. Total token…, Evict a failing or depleted model immediately and ensure it is never called…, If current chairman is evicted or inactive, fail over to the next highest-… (+3 more)

### Community 4 - "list_models"
Cohesion: 0.13
Nodes (17): list_models(), OpencodeUnavailable, Fetch the models available inside opencode. This is the council roster -…, Raised when the local opencode server cannot be reached., RuntimeError, asyncio, Unit tests for Phase 8: Per-Model Thinking Quality & Model Deduplication., Verify distinct models like ling 3.1 and ling 3.0 fin are not collapsed to the… (+9 more)

### Community 5 - "package.json"
Cohesion: 0.06
Nodes (36): allowScripts, esbuild@0.25.12, dependencies, react, react-dom, react-markdown, remark-gfm, devDependencies (+28 more)

### Community 6 - "get"
Cohesion: 0.13
Nodes (15): export_conversation_html(), export_conversation_pdf(), export_conversation_report(), export_conversation_zip_archive(), get_conversation(), get_project(), list_projects(), List all project folders with metadata and debate counts. (+7 more)

### Community 7 - "test_human_steering.py"
Cohesion: 0.08
Nodes (30): Register an ongoing CouncilRun by conversation ID., Unregister an ongoing CouncilRun by conversation ID., register_active_run(), unregister_active_run(), Send a message and stream the council as it runs. Emits Server-Sent Events as…, send_message_stream(), emit(), event_generator() (+22 more)

### Community 8 - "caveman.py"
Cohesion: 0.15
Nodes (19): build_instruction(), intensity_for(), is_installed(), load_skill(), Path, Official Caveman compression, loaded at runtime from the installed skill.…, Return the text under '## <heading>', up to the next '## '., Pull one level's row out of Caveman's own Intensity table. Keeping this parsed… (+11 more)

### Community 9 - "test_chairman_selection.py"
Cohesion: 0.10
Nodes (26): Any, Intelligent capability scoring matrix for LLM Council Chairman election. Ranks…, Select the highest capability model ID from a list of model dicts or model IDs., Compute an intelligence score (0 to 100+) for a given model dict or model ID…, score_model_capability(), select_best_chairman(), Work out who sits on the council and who chairs it. Defaults to every model…, resolve_roster() (+18 more)

### Community 10 - "create_conversation"
Cohesion: 0.11
Nodes (22): list_conversations(), List all conversations (metadata only)., create_conversation(), delete_conversation(), get_conversation_path(), list_conversations(), prune_empty_conversations(), Prune all abandoned conversations that have 0 messages. Args: except_id:… (+14 more)

### Community 11 - "Appendix B - Canonical Sources (read these before reinventing)"
Cohesion: 0.09
Nodes (21): APPENDICES - Real Source-Backed Reference Material, Appendix A - Install Commands per Design System, Appendix B - Canonical Sources (read these before reinventing), Appendix C - Apple Liquid Glass: Honest Web Approximation, Apple Liquid Glass (Apple platforms only), Atlassian, Bootstrap, Carbon (+13 more)

### Community 12 - "opencode_client.py"
Cohesion: 0.14
Nodes (17): asyncio, Configuration for the LLM Council. The council runs entirely on models that are…, Client for the local opencode server. This module replaces the old OpenRouter…, council_sessions(), main(), post(), End-to-end test of the HTTP API, including the SSE streaming path. Creates a…, Council sessions currently left in the user's opencode session list. (+9 more)

### Community 13 - "._pipeline"
Cohesion: 0.19
Nodes (11): _aggregate_block(), calculate_aggregate_rankings(), _clip(), _debate_block(), _positions_block(), Any, Ask the chairman for the final decision. Always uncompressed, whatever the…, Average each model's rank position across every peer review. (+3 more)

### Community 14 - "backend/main.py"
Cohesion: 0.06
Nodes (47): get_active_run(), Retrieve the active CouncilRun for a conversation ID, if any., Conversation, ConversationMetadata, create_conversation(), create_project(), CreateConversationRequest, CreateProjectRequest (+39 more)

### Community 15 - "get_conversation"
Cohesion: 0.16
Nodes (20): Update conversation metadata such as title or assigned project folder., update_conversation(), add_assistant_message(), add_user_message(), assign_conversation_project(), get_conversation(), Add a user message to a conversation. Args: conversation_id: Conversation…, Add an assistant message holding a complete council run. The whole run is… (+12 more)

### Community 16 - "council.py"
Cohesion: 0.15
Nodes (11): _label(), Four-stage LLM Council orchestration. Stage 1 Positions - every member answers…, 0 -> 'A', 1 -> 'B', ... 'Z', then 'AA'., Resolve the roster, then run the full four-stage council., Total the token counts opencode reported for a set of entries. opencode returns…, Token totals per stage, so the toggle's effect is visible rather than promised.…, run_full_council(), _sum_tokens() (+3 more)

### Community 17 - "verify_caveman.py"
Cohesion: 0.26
Nodes (11): council_permissions(), Build the permission ruleset for council members. Allow the research and read…, council_sessions(), main(), _median(), one_shot(), part_one(), part_two() (+3 more)

### Community 18 - "._open_sessions"
Cohesion: 0.33
Nodes (4): _call_make(), AsyncClient, Determine thinking quality / reasoning effort per model: - Honored if…, Create one session per member with resolved thinking quality. Returns the…

### Community 19 - "storage.py"
Cohesion: 0.11
Nodes (26): get_conversation_reports(), Return pre-rendered executive and detailed reports with deliberation metadata…, _clean_table_cell(), export_conversation_zip(), find_headless_browser(), format_conversation_detailed(), format_conversation_executive(), format_conversation_markdown() (+18 more)

### Community 20 - "provider_keys.py"
Cohesion: 0.13
Nodes (19): get_provider_keys(), health(), Detailed health check validating connection to OpenCode and BYOK readiness., Get status and redacted preview of configured provider API keys., _get_env_key(), get_key(), get_key_statuses(), _init_from_env() (+11 more)

### Community 21 - "test_token_budgeting.py"
Cohesion: 0.15
Nodes (15): asyncio, Real, non-mocked tests for Phase 3: Token & Time Budgeting Engine. Tests verify…, Functional test: When cumulative tokens across all models exceed…, Real wall-clock test: When real elapsed time crosses time_limit_seconds, debate…, Integration test: In a 4-round deliberation, when the token budget is capped…, Real HTTP integration test: Verify that FastAPI /api/settings accepts and…, Verify that CouncilRun properly initializes token and time tracking structures., Functional test: When a model exceeds its token_cap_per_model, it must be… (+7 more)

### Community 23 - "4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)"
Cohesion: 0.17
Nodes (12): 4.10 Quotes & Testimonials, 4.11 Page Theme Lock (Light / Dark Mode Consistency), 4.1 Typography, 4.2 Color Calibration, 4.3 Layout Diversification, 4.4 Materiality, Shadows, Cards, 4.5 Interactive UI States, 4.6 Data & Form Patterns (+4 more)

### Community 24 - "get_server_url"
Cohesion: 0.14
Nodes (16): parse_ranking_from_text(), Extract the ordered labels from a 'FINAL RANKING:' block., ask_many(), _auth_headers(), get_server_url(), opencode_request(), AsyncClient, Resolve the opencode server base URL. Order: OPENCODE_SERVER_URL env var,… (+8 more)

### Community 25 - "delete_conversation"
Cohesion: 0.40
Nodes (5): delete_conversation(), delete_project(), Delete a project folder and revert its debates to independent mode., Delete a conversation by ID., delete

### Community 26 - "HybridCouncilSession"
Cohesion: 0.29
Nodes (3): HybridCouncilSession, Any, Unified session wrapper routing to either local OpenCode daemon or direct…

### Community 27 - "Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine"
Cohesion: 0.10
Nodes (20): 1. Prerequisites, 2. Start OpenCode Service, 3. Clone & Install, 4. Launch the Platform, Can I still use commercial models like Claude 3.5 Sonnet, GPT-4o, or DeepSeek R1?, Citation, Comparison: Upstream Concept vs. Free LLM Council, Configuration & BYOK Cloud Providers (+12 more)

### Community 28 - "4. Component Standards"
Cohesion: 0.17
Nodes (11): 1. Dials & Atmosphere, 2. Color Palette & Surface Elevation, 3. Typography & Micro-Hierarchy, 4. Component Standards, 5. Performance, Ergonomics & Fast Handling, A. Left-Hand Sidebar (Workspace Tree), Accents & Signal Colors, C. Live RunRail (Real-Time Progress) (+3 more)

### Community 30 - "get_server_password"
Cohesion: 0.15
Nodes (13): diagnose_connection(), get_server_password(), _location_params(), Path, Every opencode call is scoped to the council's workspace directory., Actively inspect the connection to the OpenCode server and return a detailed…, Possible locations of opencode's service.json., Resolve the opencode server password. Order: OPENCODE_SERVER_PASSWORD env var,… (+5 more)

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
Cohesion: 0.07
Nodes (36): get_settings(), Current council settings, plus whether the official Caveman skill is installed.…, Send a message and run the full four-stage council. Returns the complete…, send_message(), get_debate_mode(), get_settings(), get_time_limit_seconds(), get_token_budget_total() (+28 more)

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

### Community 50 - "test_caveman_max.py"
Cohesion: 0.10
Nodes (19): Live test script executing an end-to-end deliberation across real OpenCode…, httpx, io, json, pytest, Real, non-mocked tests for Phase 5: Caveman Max Mode & Debate Compression.…, Ensure 'max' is recognized as a first-class debate compression level., test_caveman_levels_includes_max() (+11 more)

### Community 51 - "test_hybrid_providers.py"
Cohesion: 0.12
Nodes (20): list_unified_models(), Hybrid Council transport and unified model registry. Seamlessly combines local…, Return all available models across local OpenCode and configured external…, LLM Council backend package., delete_key(), Delete a key for a provider., asyncio, Real, non-mocked tests for Phase 6: Hybrid Provider & Custom API Key Ingestion.… (+12 more)

### Community 56 - "CLAUDE.md - Technical Notes for LLM Council"
Cohesion: 0.06
Nodes (35): generate_conversation_title(), Short title for a conversation, using the fastest available model., debate_prompt(), parse_verdict(), position_prompt(), Prompts for the four council stages. Kept in one place so the wording of each…, Stage 3: blind, anonymized scoring of the positions., Stage 4: the chairman's decision. Never compressed - a human reads this. (+27 more)

### Community 66 - "graphify.js"
Cohesion: 0.40
Nodes (3): IMPORTANT: keep the reminder string free of backticks and $(...) constructs., ref_fs, ref_path

### Community 69 - "React + Vite"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

## Knowledge Gaps
- **162 isolated node(s):** `free-llm-council`, `Appendix A - Install Commands per Design System`, `Apple Liquid Glass (Apple platforms only)`, `Atlassian`, `Bootstrap` (+157 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 463 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CLAUDE.md - Technical Notes for LLM Council` connect `CLAUDE.md - Technical Notes for LLM Council` to `get_server_url`, `CouncilSession`?**
  _High betweenness centrality (0.219) - this node is a cross-community bridge._
- **Why does `Frontend` connect `CLAUDE.md - Technical Notes for LLM Council` to `icons.jsx`?**
  _High betweenness centrality (0.206) - this node is a cross-community bridge._
- **Why does `CouncilRun` connect `CouncilRun` to `CouncilSession`, `list_models`, `test_human_steering.py`, `settings.py`, `test_chairman_selection.py`, `._pipeline`, `backend/main.py`, `council.py`, `verify_caveman.py`, `._open_sessions`, `test_caveman_max.py`, `test_hybrid_providers.py`, `test_token_budgeting.py`, `._tighten`, `get_server_url`, `HybridCouncilSession`?**
  _High betweenness centrality (0.199) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `CouncilRun` (e.g. with `HybridCouncilSession` and `CouncilSession`) actually correct?**
  _`CouncilRun` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `CouncilSession` (e.g. with `CouncilRun` and `HybridCouncilSession`) actually correct?**
  _`CouncilSession` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `free-llm-council`, `Appendix A - Install Commands per Design System`, `Apple Liquid Glass (Apple platforms only)` to the rest of the system?**
  _162 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `CouncilSession` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._