# Graph Report - free-llm-council  (2026-10-09)

## Corpus Check
- 72 files · ~74,547 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 23 file(s) not represented in the graph (top: .css 16, (none) 4, .cff 1)

## Summary
- 953 nodes · 1928 edges · 72 communities (60 shown, 12 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 61 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `92aff4a6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Any
- CouncilSession
- icons.jsx
- ._pipeline
- .run_stream
- package.json
- get
- test_model_eviction.py
- caveman.py
- test_chairman_selection.py
- test_clean_lifecycle_and_presets.py
- Appendix B - Canonical Sources (read these before reinventing)
- asyncio
- test_human_steering.py
- backend/main.py
- get_conversation
- verify_caveman.py
- generate_report_pdf
- update_settings
- storage.py
- test_hybrid_providers.py
- asyncio
- ._check_budget_limits
- 4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)
- list_models
- send_message
- post
- Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine
- 4. Component Standards
- test_council_run_records_max_caveman_mode
- asyncio
- start.sh script
- tests/__init__.py
- 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)
- test_projects_and_folders.py
- tasteskill: Anti-Slop Frontend Skill
- 9. AI TELLS (Forbidden Patterns)
- 11. REDESIGN PROTOCOL
- 3. DEFAULT ARCHITECTURE & CONVENTIONS
- create_project
- value_error_handler
- 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS
- _sum_tokens
- 0. BRIEF INFERENCE (Read the Room Before Anything Else)
- 12. THE BLOCK LIBRARY (Contract - Implementations Land Here Iteratively)
- 5. CONTEXT-AWARE PROACTIVITY
- 8. DARK MODE PROTOCOL
- 7. DIAL DEFINITIONS (Technical Reference)
- test_exports_and_conversation_id.py
- git-workflow.md
- free-llm-council
- council.py
- opencode_client.py
- reconcile_council_preset
- test_api_conversation_endpoints_reject_path_traversal
- BaseModel
- test_non_reporting_agents.py
- delete_conversation
- ._open_sessions
- test_security_hardening.py
- test_model_formatting_preserves_distinct_variants
- post_settings
- graphify.js
- ._ask_all
- CouncilRun
- React + Vite
- AGENTS.md
- rules/graphify.md
- workflows/graphify.md

## God Nodes (most connected - your core abstractions)
1. `CouncilRun` - 60 edges
2. `CouncilSession` - 27 edges
3. `get_conversation()` - 22 edges
4. `ChatInterface()` - 22 edges
5. `Sidebar()` - 21 edges
6. `list_models()` - 17 edges
7. `react` - 17 edges
8. `ReportPage()` - 17 edges
9. `tasteskill: Anti-Slop Frontend Skill` - 16 edges
10. `HybridCouncilSession` - 15 edges

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

## Communities (72 total, 12 thin omitted)

### Community 0 - "Any"
Cohesion: 0.13
Nodes (27): Update a project name or description., update_project(), create_project(), delete_project(), ensure_data_dir(), get_project(), get_projects_file(), list_projects() (+19 more)

### Community 1 - "CouncilSession"
Cohesion: 0.06
Nodes (33): HybridCouncilSession, Any, AsyncClient, Unified session wrapper routing to either local OpenCode daemon or direct…, ask_many(), CouncilSession, _parse_assistant_message(), Any (+25 more)

### Community 2 - "icons.jsx"
Cohesion: 0.08
Nodes (72): Frontend, B. Workspace Header & Breadcrumbs, api, App(), ChatInterface(), DebateMode(), LEVEL_LABELS, AlertTriangle() (+64 more)

### Community 3 - "._pipeline"
Cohesion: 0.19
Nodes (12): _aggregate_block(), calculate_aggregate_rankings(), _clip(), _debate_block(), _label(), _positions_block(), Any, Ask the chairman for the final decision. Always uncompressed, whatever the… (+4 more)

### Community 4 - ".run_stream"
Cohesion: 0.33
Nodes (3): Execute all four stages and return the full result. On any failure that is not…, Execute all four stages, optionally emitting progress as it goes. `queue`…, Queue

### Community 5 - "package.json"
Cohesion: 0.06
Nodes (35): allowScripts, esbuild@0.25.12, dependencies, react, react-dom, react-markdown, remark-gfm, devDependencies (+27 more)

### Community 6 - "get"
Cohesion: 0.15
Nodes (13): get_conversation(), get_project(), list_conversations(), list_projects(), Health check endpoint., List all project folders with metadata and debate counts., Get details for a specific project., List all conversations (metadata only). (+5 more)

### Community 7 - "test_model_eviction.py"
Cohesion: 0.18
Nodes (13): make_mock_session(), asyncio, Unit tests for Phase 2: Dynamic Member Fault-Tolerance & Model Eviction., If a model succeeds in Stage 1 but crashes in Debate Round 1, it must be…, Create a mock CouncilSession that records ask() calls and session lifecycle., If the designated chairman fails during deliberation, the council must promote…, When run_stream is used, an eviction should emit a 'model_evicted' event., If a model fails in Stage 1, it must be evicted immediately and NEVER called… (+5 more)

### Community 8 - "caveman.py"
Cohesion: 0.13
Nodes (21): build_instruction(), intensity_for(), is_installed(), load_skill(), Path, Official Caveman compression, loaded at runtime from the installed skill.…, Return the text under '## <heading>', up to the next '## '., Pull one level's row out of Caveman's own Intensity table. Keeping this parsed… (+13 more)

### Community 9 - "test_chairman_selection.py"
Cohesion: 0.10
Nodes (26): Any, Intelligent capability scoring matrix for LLM Council Chairman election. Ranks…, Select the highest capability model ID from a list of model dicts or model IDs., Compute an intelligence score (0 to 100+) for a given model dict or model ID…, score_model_capability(), select_best_chairman(), Work out who sits on the council and who chairs it. Defaults to every model…, resolve_roster() (+18 more)

### Community 10 - "test_clean_lifecycle_and_presets.py"
Cohesion: 0.40
Nodes (4): asyncio, Unit tests for Phase 9: Clean Conversation Lifecycle & Persisted Council…, Verify DELETE /api/conversations/{id} deletes conversation and handles 404 for…, test_delete_conversation_http_api()

### Community 11 - "Appendix B - Canonical Sources (read these before reinventing)"
Cohesion: 0.09
Nodes (21): APPENDICES - Real Source-Backed Reference Material, Appendix A - Install Commands per Design System, Appendix B - Canonical Sources (read these before reinventing), Appendix C - Apple Liquid Glass: Honest Web Approximation, Apple Liquid Glass (Apple platforms only), Atlassian, Bootstrap, Carbon (+13 more)

### Community 12 - "asyncio"
Cohesion: 0.29
Nodes (7): asyncio, Verify CouncilRun defaults the Chairman to max thinking and regular members to…, Verify user overrides for thinking quality are honored over defaults., Verify CouncilSession includes variant in the model specification object., test_council_run_defaults_chairman_to_max_thinking(), test_council_run_honors_user_thinking_overrides(), test_council_session_transmits_variant_in_payload()

### Community 13 - "test_human_steering.py"
Cohesion: 0.06
Nodes (35): Register an ongoing CouncilRun by conversation ID., Unregister an ongoing CouncilRun by conversation ID., register_active_run(), unregister_active_run(), Send a message and stream the council as it runs. Emits Server-Sent Events as…, send_message_stream(), emit(), event_generator() (+27 more)

### Community 14 - "backend/main.py"
Cohesion: 0.09
Nodes (25): Configuration for the LLM Council. The council runs entirely on models that are…, get_active_run(), Retrieve the active CouncilRun for a conversation ID, if any., get_models(), get_provider_keys(), health(), lifespan(), FastAPI backend for LLM Council. (+17 more)

### Community 15 - "get_conversation"
Cohesion: 0.09
Nodes (39): Update conversation metadata such as title or assigned project folder., update_conversation(), add_assistant_message(), add_user_message(), assign_conversation_project(), create_conversation(), delete_conversation(), get_conversation() (+31 more)

### Community 16 - "verify_caveman.py"
Cohesion: 0.27
Nodes (10): council_permissions(), Build the permission ruleset for council members. Allow the research and read…, main(), _median(), one_shot(), part_one(), part_two(), Measures what the Caveman levels actually do, on this council. python -m… (+2 more)

### Community 17 - "generate_report_pdf"
Cohesion: 0.25
Nodes (8): export_conversation_pdf(), Export a council deliberation as a publication-grade PDF document., find_headless_browser(), generate_report_pdf(), Detect an available headless browser executable (Edge, Chrome, Chromium) on the…, Generate a publication-grade PDF document using an available headless browser.…, Verify generate_report_pdf includes --disable-javascript and --disable-local-…, test_generate_report_pdf_includes_sandboxing_flags()

### Community 18 - "update_settings"
Cohesion: 0.25
Nodes (8): get_settings(), Current council settings, plus whether the official Caveman skill is installed.…, get_debate_mode(), get_settings(), Apply a partial update. Unknown keys and bad values are ignored., update_settings(), Verify backend.settings accepts and returns 'max' debate mode., test_settings_module_accepts_max_mode()

### Community 19 - "storage.py"
Cohesion: 0.11
Nodes (23): get_conversation_reports(), Return pre-rendered executive and detailed reports with deliberation metadata…, _clean_table_cell(), _extract_non_reporting_models(), format_conversation_detailed(), format_conversation_executive(), _generate_ascii_deliberation_flow(), prune_empty_conversations() (+15 more)

### Community 20 - "test_hybrid_providers.py"
Cohesion: 0.09
Nodes (34): list_unified_models(), Hybrid Council transport and unified model registry. Seamlessly combines local…, Return all available models across local OpenCode and configured external…, delete_key(), _get_env_key(), get_key(), get_key_statuses(), _init_from_env() (+26 more)

### Community 21 - "asyncio"
Cohesion: 0.17
Nodes (11): asyncio, Functional test: When cumulative tokens across all models exceed…, Real wall-clock test: When real elapsed time crosses time_limit_seconds, debate…, Integration test: In a 4-round deliberation, when the token budget is capped…, Real HTTP integration test: Verify that FastAPI /api/settings accepts and…, Functional test: When a model exceeds its token_cap_per_model, it must be…, test_council_run_retires_model_exceeding_token_cap(), test_council_run_stops_debate_when_global_budget_exhausted() (+3 more)

### Community 22 - "._check_budget_limits"
Cohesion: 0.22
Nodes (5): emit(), Check if any active model has exceeded token_cap_per_model. If exceeded, retire…, Determine if the debate loop should terminate early due to: 1. Total token…, Evict a failing or depleted model immediately and ensure it is never called…, If current chairman is evicted or inactive, fail over to the next highest-…

### Community 23 - "4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)"
Cohesion: 0.17
Nodes (12): 4.10 Quotes & Testimonials, 4.11 Page Theme Lock (Light / Dark Mode Consistency), 4.1 Typography, 4.2 Color Calibration, 4.3 Layout Diversification, 4.4 Materiality, Shadows, Cards, 4.5 Interactive UI States, 4.6 Data & Form Patterns (+4 more)

### Community 24 - "list_models"
Cohesion: 0.11
Nodes (28): _auth_headers(), diagnose_connection(), ensure_opencode_running(), get_server_password(), get_server_url(), is_opencode_responding(), list_models(), _location_params() (+20 more)

### Community 25 - "send_message"
Cohesion: 0.39
Nodes (8): Send a message and run the full four-stage council. Returns the complete…, send_message(), get_time_limit_seconds(), get_token_budget_total(), get_token_cap_per_model(), Any, Verify /api/settings handles both retrieval and updates for debate mode and…, test_settings_api_supports_budget_controls()

### Community 26 - "post"
Cohesion: 0.18
Nodes (11): create_conversation(), CreateConversationRequest, post_provider_key(), ProviderKeyUpdate, prune_empty_conversations(), Payload to configure or remove a provider API key., Update or remove a provider API key dynamically., Create a new conversation. (+3 more)

### Community 27 - "Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine"
Cohesion: 0.10
Nodes (20): 1. Prerequisites, 2. Start OpenCode Service, 3. Clone & Install, 4. Launch the Platform, Can I still use commercial models like Claude 3.5 Sonnet, GPT-4o, or DeepSeek R1?, Citation, Comparison: Upstream Concept vs. Free LLM Council, Configuration & BYOK Cloud Providers (+12 more)

### Community 28 - "4. Component Standards"
Cohesion: 0.17
Nodes (11): 1. Dials & Atmosphere, 2. Color Palette & Surface Elevation, 3. Typography & Micro-Hierarchy, 4. Component Standards, 5. Performance, Ergonomics & Fast Handling, A. Left-Hand Sidebar (Workspace Tree), Accents & Signal Colors, C. Live RunRail (Real-Time Progress) (+3 more)

### Community 29 - "test_council_run_records_max_caveman_mode"
Cohesion: 0.33
Nodes (5): asyncio, Functional test: When debateMode is 'max', CouncilRun marks…, HTTP integration test: FastAPI POST /api/settings accepts debateMode='max'., test_council_run_records_max_caveman_mode(), test_settings_api_accepts_max_mode()

### Community 30 - "asyncio"
Cohesion: 0.25
Nodes (7): asyncio, Verify CouncilRun captures evicted_models, retired_models, and emits early…, Verify /api/health provides all fields required by the frontend Sidebar health…, Verify /api/providers/keys endpoints support modal interactions: list, update,…, test_council_session_budget_and_eviction_telemetry(), test_health_api_contract_matches_frontend(), test_provider_keys_api_integration()

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

### Community 41 - "create_project"
Cohesion: 0.50
Nodes (4): create_project(), CreateProjectRequest, Create a new project workspace folder., Request to create a new project workspace folder.

### Community 42 - "value_error_handler"
Cohesion: 0.50
Nodes (4): Convert validation and path traversal ValueErrors to clean HTTP 400 responses., value_error_handler(), exception_handler, ValueError

### Community 43 - "6. PERFORMANCE & ACCESSIBILITY GUARDRAILS"
Cohesion: 0.29
Nodes (7): 6.A Hardware Acceleration, 6.B Reduced Motion (mandatory), 6.C Dark Mode (mandatory for any consumer-facing page), 6.D Core Web Vitals Targets, 6.E DOM Cost, 6.F Z-Index Restraint, 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS

### Community 44 - "_sum_tokens"
Cohesion: 0.33
Nodes (5): Total the token counts opencode reported for a set of entries. opencode returns…, Token totals per stage, so the toggle's effect is visible rather than promised.…, _sum_tokens(), Verify token summation logic against realistic OpenCode token telemetry: input…, test_sum_tokens_real_telemetry()

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

### Community 51 - "test_exports_and_conversation_id.py"
Cohesion: 0.10
Nodes (21): export_conversation_html(), export_conversation_report(), export_conversation_zip_archive(), Export a council deliberation as a formatted Markdown report document…, Export a council deliberation as a standalone publication-grade HTML report., Export the entire council discussion as a downloadable ZIP package containing…, export_conversation_zip(), format_conversation_markdown() (+13 more)

### Community 54 - "council.py"
Cohesion: 0.09
Nodes (19): generate_conversation_title(), parse_ranking_from_text(), Four-stage LLM Council orchestration. Stage 1 Positions - every member answers…, Short title for a conversation, using the fastest available model., Extract the ordered labels from a 'FINAL RANKING:' block., OpencodeUnavailable, Raised when the local opencode server cannot be reached., Live, mutable council settings. These are deliberately process-global rather… (+11 more)

### Community 55 - "opencode_client.py"
Cohesion: 0.08
Nodes (27): asyncio, LLM Council backend package., Client for the local opencode server. This module replaces the old OpenRouter…, main(), End-to-end test of the HTTP API, including the SSE streaming path. Creates a…, Verification script for the opencode client and the council sandbox. Run with:…, base64, json (+19 more)

### Community 56 - "reconcile_council_preset"
Cohesion: 0.50
Nodes (4): Reconciles a saved council preset against currently available OpenCode models.…, reconcile_council_preset(), Verify preset reconciliation logic: If a saved model is missing from OpenCode,…, test_preset_auto_reconciliation()

### Community 57 - "test_api_conversation_endpoints_reject_path_traversal"
Cohesion: 0.67
Nodes (3): asyncio, Verify FastAPI conversation endpoints safely handle path traversal sequences…, test_api_conversation_endpoints_reject_path_traversal()

### Community 58 - "BaseModel"
Cohesion: 0.18
Nodes (11): Conversation, ConversationMetadata, Conversation metadata for list view., Full conversation with all messages., Request to update a project., Request to update a conversation (project assignment, title, or archive status)., Request to send a message in a conversation., SendMessageRequest (+3 more)

### Community 59 - "test_non_reporting_agents.py"
Cohesion: 0.29
Nodes (8): make_mock_session(), asyncio, Unit tests for non-reporting agents, upfront report notices, and Phase 1…, If a member cannot initialize session, it is registered as evicted and excluded…, If a member times out in Phase 1, it quits before debate and is excluded from…, test_phase_1_dropout_quits_debate_and_excluded_from_prompts(), test_session_init_failure_evicts_non_reporting_member(), fake_make()

### Community 60 - "delete_conversation"
Cohesion: 0.40
Nodes (5): delete_conversation(), delete_project(), Delete a project folder and revert its debates to independent mode., Delete a conversation by ID., delete

### Community 61 - "._open_sessions"
Cohesion: 0.33
Nodes (4): _call_make(), AsyncClient, Determine thinking quality / reasoning effort per model: - Honored if…, Create one session per member with resolved thinking quality. Returns the…

### Community 62 - "test_security_hardening.py"
Cohesion: 0.29
Nodes (6): pytest, Security hardening regression tests for path traversal, stored XSS, and…, Unit tests for Phase 8: Per-Model Thinking Quality & Model Deduplication., Verify list_models includes variants list and deduplicates identical IDs., test_list_models_extracts_variants_and_deduplicates(), unittest_mock

### Community 64 - "post_settings"
Cohesion: 0.50
Nodes (4): post_settings(), Live settings the user can change while a run is in flight., Change live council settings. Takes effect on the next debate round., SettingsUpdate

### Community 66 - "graphify.js"
Cohesion: 0.40
Nodes (3): IMPORTANT: keep the reminder string free of backticks and $(...) constructs., ref_fs, ref_path

### Community 68 - "CouncilRun"
Cohesion: 0.17
Nodes (8): CouncilRun, Resolve the roster, then run the full four-stage council., One council deliberation, owning every session it creates., Inject human operator guidance and resources into the ongoing deliberation., Re-scope every member's permissions, ignoring individual failures., run_full_council(), Verify that CouncilRun properly initializes token and time tracking structures., test_council_run_token_budget_initialization()

### Community 69 - "React + Vite"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

## Knowledge Gaps
- **162 isolated node(s):** `name`, `private`, `version`, `type`, `dev` (+157 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 488 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CLAUDE.md - Technical Notes for LLM Council` connect `CouncilSession` to `list_models`, `icons.jsx`, `test_human_steering.py`?**
  _High betweenness centrality (0.224) - this node is a cross-community bridge._
- **Why does `Frontend` connect `icons.jsx` to `CouncilSession`?**
  _High betweenness centrality (0.212) - this node is a cross-community bridge._
- **Why does `CouncilRun` connect `CouncilRun` to `CouncilSession`, `._pipeline`, `.run_stream`, `test_model_eviction.py`, `caveman.py`, `test_chairman_selection.py`, `asyncio`, `test_human_steering.py`, `backend/main.py`, `verify_caveman.py`, `test_hybrid_providers.py`, `asyncio`, `._check_budget_limits`, `list_models`, `test_council_run_records_max_caveman_mode`, `asyncio`, `_sum_tokens`, `council.py`, `test_non_reporting_agents.py`, `._open_sessions`, `test_security_hardening.py`, `._ask_all`?**
  _High betweenness centrality (0.208) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `CouncilRun` (e.g. with `HybridCouncilSession` and `CouncilSession`) actually correct?**
  _`CouncilRun` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `CouncilSession` (e.g. with `CouncilRun` and `HybridCouncilSession`) actually correct?**
  _`CouncilSession` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _162 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Any` be split into smaller, more focused modules?**
  _Cohesion score 0.12535612535612536 - nodes in this community are weakly interconnected._