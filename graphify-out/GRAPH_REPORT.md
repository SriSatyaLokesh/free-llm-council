# Graph Report - free-llm-council  (2026-10-07)

## Corpus Check
- 67 files · ~66,264 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 21 file(s) not represented in the graph (top: .css 15, (none) 4, .cff 1)

## Summary
- 878 nodes · 1719 edges · 63 communities (52 shown, 11 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 57 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `dd37313f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- storage.py
- ._params
- icons.jsx
- council.py
- list_models
- package.json
- post_provider_key
- test_model_eviction.py
- opencode_client.py
- test_chairman_selection.py
- create_conversation
- Appendix B - Canonical Sources (read these before reinventing)
- CouncilRun
- test_diagnose_connection_detects_port_conflict
- backend/main.py
- get_conversation
- CLAUDE.md - Technical Notes for LLM Council
- BaseModel
- post
- Any
- provider_keys.py
- test_token_budgeting.py
- send_message_stream
- 4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)
- CouncilSession
- delete_conversation
- HybridCouncilSession
- Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine
- 4. Component Standards
- _service_config_candidates
- get_server_url
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
- test_human_steering.py
- 0. BRIEF INFERENCE (Read the Room Before Anything Else)
- 12. THE BLOCK LIBRARY (Contract - Implementations Land Here Iteratively)
- 5. CONTEXT-AWARE PROACTIVITY
- 8. DARK MODE PROTOCOL
- 7. DIAL DEFINITIONS (Technical Reference)
- test_exports_and_conversation_id.py
- test_hybrid_providers.py
- git-workflow.md
- free-llm-council
- post_settings
- ask_many
- prompts.py
- list_conversations
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
- `Backend structure` --references--> `calculate_aggregate_rankings()`  [INFERRED]
  CLAUDE.md → backend/council.py
- `Backend structure` --references--> `CouncilRun`  [INFERRED]
  CLAUDE.md → backend/council.py

## Import Cycles
- None detected.

## Communities (63 total, 11 thin omitted)

### Community 0 - "storage.py"
Cohesion: 0.14
Nodes (24): Update a project name or description., update_project(), create_project(), delete_project(), ensure_data_dir(), get_project(), get_projects_file(), list_projects() (+16 more)

### Community 1 - "._params"
Cohesion: 0.21
Nodes (9): _parse_assistant_message(), Any, Flatten an opencode assistant message into text / reasoning / tool calls., Replace this session's permission ruleset mid-run. Used to tighten the sandbox…, Send a prompt and wait for the agent loop to finish. Returns {text, reasoning,…, Read the session's own outcome flag. opencode reports a failed agent loop as…, Stop a runaway agent loop so the session does not keep burning tokens., Read the assistant messages produced since the last prompt. (+1 more)

### Community 2 - "icons.jsx"
Cohesion: 0.08
Nodes (61): Frontend, B. Workspace Header & Breadcrumbs, api, App(), ChatInterface(), DebateMode(), LEVEL_LABELS, AlertTriangle() (+53 more)

### Community 3 - "council.py"
Cohesion: 0.12
Nodes (21): _aggregate_block(), calculate_aggregate_rankings(), _clip(), _debate_block(), _label(), _positions_block(), Any, AsyncClient (+13 more)

### Community 4 - "list_models"
Cohesion: 0.11
Nodes (19): generate_conversation_title(), Short title for a conversation, using the fastest available model., list_models(), OpencodeUnavailable, Fetch the models available inside opencode. This is the council roster -…, Raised when the local opencode server cannot be reached., RuntimeError, asyncio (+11 more)

### Community 5 - "package.json"
Cohesion: 0.06
Nodes (35): allowScripts, esbuild@0.25.12, dependencies, react, react-dom, react-markdown, devDependencies, eslint (+27 more)

### Community 6 - "post_provider_key"
Cohesion: 0.50
Nodes (4): post_provider_key(), ProviderKeyUpdate, Payload to configure or remove a provider API key., Update or remove a provider API key dynamically.

### Community 7 - "test_model_eviction.py"
Cohesion: 0.18
Nodes (13): make_mock_session(), asyncio, Unit tests for Phase 2: Dynamic Member Fault-Tolerance & Model Eviction., If a model succeeds in Stage 1 but crashes in Debate Round 1, it must be…, Create a mock CouncilSession that records ask() calls and session lifecycle., If the designated chairman fails during deliberation, the council must promote…, When run_stream is used, an eviction should emit a 'model_evicted' event., If a model fails in Stage 1, it must be evicted immediately and NEVER called… (+5 more)

### Community 8 - "opencode_client.py"
Cohesion: 0.05
Nodes (51): asyncio, build_instruction(), intensity_for(), is_installed(), load_skill(), Path, Official Caveman compression, loaded at runtime from the installed skill.…, Return the text under '## <heading>', up to the next '## '. (+43 more)

### Community 9 - "test_chairman_selection.py"
Cohesion: 0.10
Nodes (26): Any, Intelligent capability scoring matrix for LLM Council Chairman election. Ranks…, Select the highest capability model ID from a list of model dicts or model IDs., Compute an intelligence score (0 to 100+) for a given model dict or model ID…, score_model_capability(), select_best_chairman(), Work out who sits on the council and who chairs it. Defaults to every model…, resolve_roster() (+18 more)

### Community 10 - "create_conversation"
Cohesion: 0.15
Nodes (16): create_conversation(), delete_conversation(), get_conversation_path(), Get the file path for a conversation., Create a new conversation. Args: conversation_id: Unique identifier for the…, Permanently delete a conversation from storage. Returns: True if the file was…, asyncio, Unit tests for Phase 9: Clean Conversation Lifecycle & Persisted Council… (+8 more)

### Community 11 - "Appendix B - Canonical Sources (read these before reinventing)"
Cohesion: 0.09
Nodes (21): APPENDICES - Real Source-Backed Reference Material, Appendix A - Install Commands per Design System, Appendix B - Canonical Sources (read these before reinventing), Appendix C - Apple Liquid Glass: Honest Web Approximation, Apple Liquid Glass (Apple platforms only), Atlassian, Bootstrap, Carbon (+13 more)

### Community 12 - "CouncilRun"
Cohesion: 0.10
Nodes (14): CouncilRun, _call_make(), emit(), One council deliberation, owning every session it creates., Inject human operator guidance and resources into the ongoing deliberation., Determine thinking quality / reasoning effort per model: - Honored if…, Check if any active model has exceeded token_cap_per_model. If exceeded, retire…, Determine if the debate loop should terminate early due to: 1. Total token… (+6 more)

### Community 13 - "test_diagnose_connection_detects_port_conflict"
Cohesion: 0.40
Nodes (5): asyncio, If a port is open but occupied by another process (e.g. Kilo on 4096),…, FastAPI /api/health endpoint should report OpenCode connection and diagnostics., test_diagnose_connection_detects_port_conflict(), test_health_endpoint_returns_diagnostics()

### Community 14 - "backend/main.py"
Cohesion: 0.11
Nodes (22): get_conversation(), get_models(), get_project(), get_provider_keys(), list_conversations(), list_projects(), FastAPI backend for LLM Council., Health check endpoint. (+14 more)

### Community 15 - "get_conversation"
Cohesion: 0.16
Nodes (22): Update conversation metadata such as title or assigned project folder., Send a message and run the full four-stage council. Returns the complete…, send_message(), update_conversation(), add_assistant_message(), add_user_message(), assign_conversation_project(), get_conversation() (+14 more)

### Community 16 - "CLAUDE.md - Technical Notes for LLM Council"
Cohesion: 0.15
Nodes (12): Caveman compression, CLAUDE.md - Technical Notes for LLM Council, Custom agents do not work from a project config, graphify, Measuring it, Project overview, Sandbox, Tool suppression is enforced, not requested (+4 more)

### Community 17 - "BaseModel"
Cohesion: 0.18
Nodes (11): Conversation, ConversationMetadata, Full conversation with all messages., Request to update a project., Request to update a conversation (project assignment, title, or archive status)., Request to send a message in a conversation., Conversation metadata for list view., SendMessageRequest (+3 more)

### Community 18 - "post"
Cohesion: 0.18
Nodes (11): create_conversation(), create_project(), CreateConversationRequest, CreateProjectRequest, prune_empty_conversations(), Create a new project workspace folder., Create a new conversation., Prune all empty abandoned conversations (0 messages). (+3 more)

### Community 19 - "Any"
Cohesion: 0.12
Nodes (21): export_conversation_report(), export_conversation_zip_archive(), get_conversation_reports(), Export a council deliberation as a formatted Markdown report document…, Return pre-rendered executive and detailed reports with deliberation metadata…, Export the entire council discussion as a downloadable ZIP package containing…, _clean_table_cell(), export_conversation_zip() (+13 more)

### Community 20 - "provider_keys.py"
Cohesion: 0.23
Nodes (11): _get_env_key(), get_key(), get_key_statuses(), _init_from_env(), Any, Secure in-memory and environment-backed provider API key management. Supports…, Retrieve key from environment variables including known aliases., Retrieve the raw secret key for a provider. (+3 more)

### Community 21 - "test_token_budgeting.py"
Cohesion: 0.13
Nodes (17): asyncio, Real, non-mocked tests for Phase 3: Token & Time Budgeting Engine. Tests verify…, Functional test: When cumulative tokens across all models exceed…, Real wall-clock test: When real elapsed time crosses time_limit_seconds, debate…, Integration test: In a 4-round deliberation, when the token budget is capped…, Real HTTP integration test: Verify that FastAPI /api/settings accepts and…, Verify token summation logic against realistic OpenCode token telemetry: input…, Verify that CouncilRun properly initializes token and time tracking structures. (+9 more)

### Community 22 - "send_message_stream"
Cohesion: 0.22
Nodes (10): Register an ongoing CouncilRun by conversation ID., Unregister an ongoing CouncilRun by conversation ID., register_active_run(), unregister_active_run(), Send a message and stream the council as it runs. Emits Server-Sent Events as…, send_message_stream(), emit(), event_generator() (+2 more)

### Community 23 - "4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)"
Cohesion: 0.17
Nodes (12): 4.10 Quotes & Testimonials, 4.11 Page Theme Lock (Light / Dark Mode Consistency), 4.1 Typography, 4.2 Color Calibration, 4.3 Layout Diversification, 4.4 Materiality, Shadows, Cards, 4.5 Interactive UI States, 4.6 Data & Form Patterns (+4 more)

### Community 24 - "CouncilSession"
Cohesion: 0.24
Nodes (6): AsyncClient, CouncilSession, One opencode session driven by one council member. The session is reused across…, Create the underlying opencode session., Delete the opencode session so it does not clutter the user's list., Common gotchas

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

### Community 29 - "_service_config_candidates"
Cohesion: 0.67
Nodes (3): Path, Possible locations of opencode's service.json., _service_config_candidates()

### Community 30 - "get_server_url"
Cohesion: 0.10
Nodes (24): parse_ranking_from_text(), Extract the ordered labels from a 'FINAL RANKING:' block., health(), Detailed health check validating connection to OpenCode and BYOK readiness., _auth_headers(), diagnose_connection(), get_server_password(), get_server_url() (+16 more)

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
Nodes (34): get_settings(), Current council settings, plus whether the official Caveman skill is installed.…, get_debate_mode(), get_settings(), get_time_limit_seconds(), get_token_budget_total(), get_token_cap_per_model(), Any (+26 more)

### Community 42 - "get_active_run"
Cohesion: 0.33
Nodes (6): get_active_run(), Retrieve the active CouncilRun for a conversation ID, if any., Inject human operator guidance and resources into an ongoing deliberation., Request to inject human operator guidance into an ongoing debate., steer_conversation(), SteerRequest

### Community 43 - "6. PERFORMANCE & ACCESSIBILITY GUARDRAILS"
Cohesion: 0.29
Nodes (7): 6.A Hardware Acceleration, 6.B Reduced Motion (mandatory), 6.C Dark Mode (mandatory for any consumer-facing page), 6.D Core Web Vitals Targets, 6.E DOM Cost, 6.F Z-Index Restraint, 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS

### Community 44 - "test_human_steering.py"
Cohesion: 0.28
Nodes (7): asyncio, Unit and integration tests for Phase 11: Human-in-the-Loop Mid-Debate Steering…, Verify that steering injected into a CouncilRun appears in debate prompt, queue…, Verify HTTP POST /api/conversations/{id}/steer behavior., test_council_run_incorporates_steering_in_debate_and_verdict(), make_mock(), test_steer_http_api_endpoints()

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
Cohesion: 0.22
Nodes (8): io, asyncio, Tests for conversation ID exposure, markdown report export, and zip bundle…, Verify HTTP GET endpoints for report and zip downloads., Verify in-memory zip archive packages executive-report.md, detailed-report.md,…, test_export_conversation_zip_archive(), test_export_endpoints_http(), zipfile

### Community 51 - "test_hybrid_providers.py"
Cohesion: 0.08
Nodes (31): list_unified_models(), Hybrid Council transport and unified model registry. Seamlessly combines local…, Return all available models across local OpenCode and configured external…, LLM Council backend package., delete_key(), Store or clear a key for a provider., Delete a key for a provider., set_key() (+23 more)

### Community 54 - "post_settings"
Cohesion: 0.50
Nodes (4): post_settings(), Change live council settings. Takes effect on the next debate round., Live settings the user can change while a run is in flight., SettingsUpdate

### Community 56 - "prompts.py"
Cohesion: 0.10
Nodes (20): debate_prompt(), parse_verdict(), position_prompt(), Prompts for the four council stages. Kept in one place so the wording of each…, Stage 3: blind, anonymized scoring of the positions., Stage 4: the chairman's decision. Never compressed - a human reads this., Stage 1: independent first opinion. Never compressed - a human reads this., Split a chairman response into its sections. Falls back to putting everything… (+12 more)

### Community 66 - "graphify.js"
Cohesion: 0.40
Nodes (3): IMPORTANT: keep the reminder string free of backticks and $(...) constructs., ref_fs, ref_path

### Community 69 - "React + Vite"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

## Knowledge Gaps
- **161 isolated node(s):** `name`, `private`, `version`, `type`, `dev` (+156 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 456 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CLAUDE.md - Technical Notes for LLM Council` connect `CLAUDE.md - Technical Notes for LLM Council` to `CouncilSession`, `icons.jsx`, `prompts.py`, `get_server_url`?**
  _High betweenness centrality (0.220) - this node is a cross-community bridge._
- **Why does `Frontend` connect `icons.jsx` to `CLAUDE.md - Technical Notes for LLM Council`?**
  _High betweenness centrality (0.207) - this node is a cross-community bridge._
- **Why does `CouncilRun` connect `CouncilRun` to `council.py`, `list_models`, `test_model_eviction.py`, `opencode_client.py`, `settings.py`, `test_chairman_selection.py`, `test_human_steering.py`, `backend/main.py`, `test_hybrid_providers.py`, `test_token_budgeting.py`, `send_message_stream`, `CouncilSession`, `HybridCouncilSession`, `get_server_url`?**
  _High betweenness centrality (0.204) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `CouncilRun` (e.g. with `HybridCouncilSession` and `CouncilSession`) actually correct?**
  _`CouncilRun` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `CouncilSession` (e.g. with `CouncilRun` and `HybridCouncilSession`) actually correct?**
  _`CouncilSession` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _161 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `storage.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14333333333333334 - nodes in this community are weakly interconnected._