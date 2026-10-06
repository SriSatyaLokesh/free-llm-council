# Graph Report - llm-council  (2026-10-06)

## Corpus Check
- 65 files · ~61,272 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 20 file(s) not represented in the graph (top: .css 14, (none) 4, .cff 1)

## Summary
- 847 nodes · 1634 edges · 70 communities (58 shown, 12 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 57 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `27b4b558`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- storage.py
- CouncilSession
- icons.jsx
- verify_caveman.py
- create_conversation
- package.json
- test_thinking_quality_and_deduplication.py
- test_model_eviction.py
- status
- test_chairman_selection.py
- generate_conversation_title
- Appendix B - Canonical Sources (read these before reinventing)
- ._pipeline
- asyncio
- backend/main.py
- CLAUDE.md - Technical Notes for LLM Council
- ._check_budget_limits
- BaseModel
- post
- _sum_tokens
- debate_prompt
- test_opencode_discovery.py
- CouncilRun
- 4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)
- opencode_client.py
- delete_conversation
- ._open_sessions
- Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine
- 4. Component Standards
- OpencodeUnavailable
- list_models
- start.sh
- tests/__init__.py
- 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)
- prompts.py
- tasteskill: Anti-Slop Frontend Skill
- 9. AI TELLS (Forbidden Patterns)
- 11. REDESIGN PROTOCOL
- 3. DEFAULT ARCHITECTURE & CONVENTIONS
- test_ui_controls_telemetry.py
- get_active_run
- 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS
- Caveman compression
- 0. BRIEF INFERENCE (Read the Room Before Anything Else)
- 12. THE BLOCK LIBRARY (Contract - Implementations Land Here Iteratively)
- 5. CONTEXT-AWARE PROACTIVITY
- 8. DARK MODE PROTOCOL
- 7. DIAL DEFINITIONS (Technical Reference)
- create_project
- provider_keys.py
- git-workflow.md
- free-llm-council
- get_conversation
- test_projects_and_folders.py
- test_human_steering.py
- council.py
- test_model_formatting_preserves_distinct_variants
- build_instruction
- post_provider_key
- test_exports_and_conversation_id.py
- ._ask_all
- ._tighten
- update_project
- graphify.js
- React + Vite
- AGENTS.md
- rules/graphify.md
- workflows/graphify.md

## God Nodes (most connected - your core abstractions)
1. `CouncilRun` - 57 edges
2. `CouncilSession` - 28 edges
3. `Sidebar()` - 20 edges
4. `get_conversation()` - 19 edges
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
- `Backend structure` --references--> `parse_ranking_from_text()`  [INFERRED]
  CLAUDE.md → backend/council.py
- `Backend structure` --references--> `calculate_aggregate_rankings()`  [INFERRED]
  CLAUDE.md → backend/council.py

## Import Cycles
- None detected.

## Communities (70 total, 12 thin omitted)

### Community 0 - "storage.py"
Cohesion: 0.16
Nodes (24): create_project(), delete_project(), ensure_data_dir(), get_project(), get_projects_file(), list_conversations(), list_projects(), load_all_projects() (+16 more)

### Community 1 - "CouncilSession"
Cohesion: 0.09
Nodes (20): HybridCouncilSession, Any, AsyncClient, Unified session wrapper routing to either local OpenCode daemon or direct…, ask_many(), CouncilSession, _parse_assistant_message(), Any (+12 more)

### Community 2 - "icons.jsx"
Cohesion: 0.09
Nodes (53): B. Workspace Header & Breadcrumbs, api, App(), ChatInterface(), DebateMode(), LEVEL_LABELS, AlertTriangle(), Archive() (+45 more)

### Community 3 - "verify_caveman.py"
Cohesion: 0.12
Nodes (18): Intelligent capability scoring matrix for LLM Council Chairman election. Ranks…, Official Caveman compression, loaded at runtime from the installed skill.…, council_permissions(), Build the permission ruleset for council members. Allow the research and read…, Live, mutable council settings. These are deliberately process-global rather…, Note which mode a stage ran in., record_stage_mode(), main() (+10 more)

### Community 4 - "create_conversation"
Cohesion: 0.14
Nodes (19): Reconciles a saved council preset against currently available OpenCode models.…, reconcile_council_preset(), create_conversation(), delete_conversation(), get_conversation_path(), Get the file path for a conversation., Create a new conversation. Args: conversation_id: Unique identifier for the…, Permanently delete a conversation from storage. Returns: True if the file was… (+11 more)

### Community 5 - "package.json"
Cohesion: 0.06
Nodes (35): allowScripts, esbuild@0.25.12, dependencies, react, react-dom, react-markdown, devDependencies, eslint (+27 more)

### Community 6 - "test_thinking_quality_and_deduplication.py"
Cohesion: 0.21
Nodes (11): asyncio, Unit tests for Phase 8: Per-Model Thinking Quality & Model Deduplication., Verify CouncilRun defaults the Chairman to max thinking and regular members to…, Verify user overrides for thinking quality are honored over defaults., Verify list_models includes variants list and deduplicates identical IDs., Verify CouncilSession includes variant in the model specification object., test_council_run_defaults_chairman_to_max_thinking(), test_council_run_honors_user_thinking_overrides() (+3 more)

### Community 7 - "test_model_eviction.py"
Cohesion: 0.18
Nodes (13): make_mock_session(), asyncio, Unit tests for Phase 2: Dynamic Member Fault-Tolerance & Model Eviction., If a model succeeds in Stage 1 but crashes in Debate Round 1, it must be…, Create a mock CouncilSession that records ask() calls and session lifecycle., If the designated chairman fails during deliberation, the council must promote…, When run_stream is used, an eviction should emit a 'model_evicted' event., If a model fails in Stage 1, it must be evicted immediately and NEVER called… (+5 more)

### Community 8 - "status"
Cohesion: 0.29
Nodes (8): is_installed(), load_skill(), Path, What the UI needs to render the mode picker honestly., Read the installed SKILL.md, cached against the file's mtime. Returns None when…, skill_path(), status(), It is the upstream implementation, not a local imitation

### Community 9 - "test_chairman_selection.py"
Cohesion: 0.12
Nodes (23): Any, Select the highest capability model ID from a list of model dicts or model IDs., Compute an intelligence score (0 to 100+) for a given model dict or model ID…, score_model_capability(), select_best_chairman(), Work out who sits on the council and who chairs it. Defaults to every model…, resolve_roster(), default_chairman() (+15 more)

### Community 10 - "generate_conversation_title"
Cohesion: 0.25
Nodes (8): generate_conversation_title(), Short title for a conversation, using the fastest available model., Send a message and stream the council as it runs. Emits Server-Sent Events as…, Request to send a message in a conversation., send_message_stream(), emit(), event_generator(), SendMessageRequest

### Community 11 - "Appendix B - Canonical Sources (read these before reinventing)"
Cohesion: 0.09
Nodes (21): APPENDICES - Real Source-Backed Reference Material, Appendix A - Install Commands per Design System, Appendix B - Canonical Sources (read these before reinventing), Appendix C - Apple Liquid Glass: Honest Web Approximation, Apple Liquid Glass (Apple platforms only), Atlassian, Bootstrap, Carbon (+13 more)

### Community 12 - "._pipeline"
Cohesion: 0.17
Nodes (15): _aggregate_block(), calculate_aggregate_rankings(), _clip(), _debate_block(), _label(), parse_ranking_from_text(), _positions_block(), Any (+7 more)

### Community 13 - "asyncio"
Cohesion: 0.17
Nodes (11): asyncio, Functional test: When cumulative tokens across all models exceed…, Real wall-clock test: When real elapsed time crosses time_limit_seconds, debate…, Integration test: In a 4-round deliberation, when the token budget is capped…, Real HTTP integration test: Verify that FastAPI /api/settings accepts and…, Functional test: When a model exceeds its token_cap_per_model, it must be…, test_council_run_retires_model_exceeding_token_cap(), test_council_run_stops_debate_when_global_budget_exhausted() (+3 more)

### Community 14 - "backend/main.py"
Cohesion: 0.11
Nodes (22): get_conversation(), get_project(), get_provider_keys(), health(), list_conversations(), list_projects(), FastAPI backend for LLM Council., Health check endpoint. (+14 more)

### Community 15 - "CLAUDE.md - Technical Notes for LLM Council"
Cohesion: 0.22
Nodes (8): CLAUDE.md - Technical Notes for LLM Council, Custom agents do not work from a project config, Frontend, graphify, Project overview, Sandbox, Transport: why opencode sessions, Verification

### Community 16 - "._check_budget_limits"
Cohesion: 0.22
Nodes (5): emit(), Check if any active model has exceeded token_cap_per_model. If exceeded, retire…, Determine if the debate loop should terminate early due to: 1. Total token…, Evict a failing or depleted model immediately and ensure it is never called…, If current chairman is evicted or inactive, fail over to the next highest-…

### Community 17 - "BaseModel"
Cohesion: 0.22
Nodes (9): Conversation, ConversationMetadata, Full conversation with all messages., Request to update a project., Request to update a conversation (project assignment, title, or archive status)., Conversation metadata for list view., UpdateConversationRequest, UpdateProjectRequest (+1 more)

### Community 18 - "post"
Cohesion: 0.18
Nodes (11): create_conversation(), CreateConversationRequest, post_settings(), prune_empty_conversations(), Change live council settings. Takes effect on the next debate round., Create a new conversation., Prune all empty abandoned conversations (0 messages)., Request to create a new conversation. (+3 more)

### Community 19 - "_sum_tokens"
Cohesion: 0.33
Nodes (5): Total the token counts opencode reported for a set of entries. opencode returns…, Token totals per stage, so the toggle's effect is visible rather than promised.…, _sum_tokens(), Verify token summation logic against realistic OpenCode token telemetry: input…, test_sum_tokens_real_telemetry()

### Community 20 - "debate_prompt"
Cohesion: 0.20
Nodes (10): debate_prompt(), Stage 4: the chairman's decision. Never compressed - a human reads this., Stage 2: named cross-examination, one round at a time. `caveman_instruction` is…, verdict_prompt(), Verify that verdict_prompt alerts the chairman to expand compressed debate…, Verify that debate_prompt embeds the Caveman max instruction cleanly., test_chairman_prompt_contains_expansion_directive_for_max(), test_prompts_integrate_max_contract() (+2 more)

### Community 21 - "test_opencode_discovery.py"
Cohesion: 0.11
Nodes (16): Live test script executing an end-to-end deliberation across real OpenCode…, json, asyncio, Unit tests for OpenCode discovery, port resilience, and health diagnostics., OPENCODE_SERVER_URL env var should override all detection., Dynamic port from 'opencode service status' should be extracted cleanly., Password should be resolved from service.json candidate directories., When no service.json exists, an informative OpencodeUnavailable error is raised. (+8 more)

### Community 22 - "CouncilRun"
Cohesion: 0.13
Nodes (12): CouncilRun, Resolve the roster, then run the full four-stage council., One council deliberation, owning every session it creates., Inject human operator guidance and resources into the ongoing deliberation., Execute all four stages and return the full result. On any failure that is not…, Execute all four stages, optionally emitting progress as it goes. `queue`…, run_full_council(), Queue (+4 more)

### Community 23 - "4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)"
Cohesion: 0.17
Nodes (12): 4.10 Quotes & Testimonials, 4.11 Page Theme Lock (Light / Dark Mode Consistency), 4.1 Typography, 4.2 Color Calibration, 4.3 Layout Diversification, 4.4 Materiality, Shadows, Cards, 4.5 Interactive UI States, 4.6 Data & Form Patterns (+4 more)

### Community 24 - "opencode_client.py"
Cohesion: 0.13
Nodes (16): asyncio, Configuration for the LLM Council. The council runs entirely on models that are…, Path, Client for the local opencode server. This module replaces the old OpenRouter…, Possible locations of opencode's service.json., _service_config_candidates(), main(), End-to-end test of the HTTP API, including the SSE streaming path. Creates a… (+8 more)

### Community 25 - "delete_conversation"
Cohesion: 0.40
Nodes (5): delete_conversation(), delete_project(), Delete a project folder and revert its debates to independent mode., Delete a conversation by ID., delete

### Community 26 - "._open_sessions"
Cohesion: 0.33
Nodes (3): _call_make(), Determine thinking quality / reasoning effort per model: - Honored if…, Create one session per member with resolved thinking quality. Returns the…

### Community 27 - "Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine"
Cohesion: 0.10
Nodes (20): 1. Prerequisites, 2. Start OpenCode Service, 3. Clone & Install, 4. Launch the Platform, Can I still use commercial models like Claude 3.5 Sonnet, GPT-4o, or DeepSeek R1?, Citation, Comparison: Upstream Concept vs. Free LLM Council, Configuration & BYOK Cloud Providers (+12 more)

### Community 28 - "4. Component Standards"
Cohesion: 0.17
Nodes (11): 1. Dials & Atmosphere, 2. Color Palette & Surface Elevation, 3. Typography & Micro-Hierarchy, 4. Component Standards, 5. Performance, Ergonomics & Fast Handling, A. Left-Hand Sidebar (Workspace Tree), Accents & Signal Colors, C. Live RunRail (Real-Time Progress) (+3 more)

### Community 29 - "OpencodeUnavailable"
Cohesion: 0.40
Nodes (5): get_models(), The council roster, read live from OpenCode and configured custom providers., OpencodeUnavailable, Raised when the local opencode server cannot be reached., RuntimeError

### Community 30 - "list_models"
Cohesion: 0.18
Nodes (19): _auth_headers(), diagnose_connection(), get_server_password(), get_server_url(), list_models(), _location_params(), opencode_request(), AsyncClient (+11 more)

### Community 34 - "10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)"
Cohesion: 0.20
Nodes (10): 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know), Animation Library Choice, Cards & Containers, Galleries & Media, Hero Paradigms, Layout & Grids, Micro-Interactions & Effects, Navigation & Menus (+2 more)

### Community 36 - "prompts.py"
Cohesion: 0.18
Nodes (10): parse_verdict(), position_prompt(), Prompts for the four council stages. Kept in one place so the wording of each…, Stage 3: blind, anonymized scoring of the positions., Stage 1: independent first opinion. Never compressed - a human reads this., Split a chairman response into its sections. Falls back to putting everything…, Short conversation title., review_prompt() (+2 more)

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

### Community 41 - "test_ui_controls_telemetry.py"
Cohesion: 0.08
Nodes (29): get_settings(), Current council settings, plus whether the official Caveman skill is installed.…, Send a message and run the full four-stage council. Returns the complete…, send_message(), get_debate_mode(), get_settings(), get_time_limit_seconds(), get_token_budget_total() (+21 more)

### Community 42 - "get_active_run"
Cohesion: 0.33
Nodes (6): get_active_run(), Retrieve the active CouncilRun for a conversation ID, if any., Inject human operator guidance and resources into an ongoing deliberation., Request to inject human operator guidance into an ongoing debate., steer_conversation(), SteerRequest

### Community 43 - "6. PERFORMANCE & ACCESSIBILITY GUARDRAILS"
Cohesion: 0.29
Nodes (7): 6.A Hardware Acceleration, 6.B Reduced Motion (mandatory), 6.C Dark Mode (mandatory for any consumer-facing page), 6.D Core Web Vitals Targets, 6.E DOM Cost, 6.F Z-Index Restraint, 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS

### Community 44 - "Caveman compression"
Cohesion: 0.40
Nodes (5): Caveman compression, Measuring it, Tool suppression is enforced, not requested, What the numbers looked like, Why not the proxy or the middleware

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

### Community 51 - "provider_keys.py"
Cohesion: 0.10
Nodes (21): delete_key(), get_key(), get_key_statuses(), Any, Secure in-memory and environment-backed provider API key management. Supports…, Retrieve the raw secret key for a provider., Store or clear a key for a provider., Delete a key for a provider. (+13 more)

### Community 54 - "get_conversation"
Cohesion: 0.18
Nodes (18): Update conversation metadata such as title or assigned project folder., update_conversation(), add_assistant_message(), add_user_message(), assign_conversation_project(), get_conversation(), Add a user message to a conversation. Args: conversation_id: Conversation…, Add an assistant message holding a complete council run. The whole run is… (+10 more)

### Community 55 - "test_projects_and_folders.py"
Cohesion: 0.28
Nodes (8): asyncio, Unit and integration tests for Phase 10: Projects & Workspace Folder Hierarchy., Verify creating debate directly in project, moving between projects, and…, Verify HTTP API PATCH endpoint for renaming and archiving conversations., HTTP API integration tests for /api/projects and /api/conversations/{id}., test_conversation_archive_and_rename_api(), test_create_conversation_with_project_and_move_lifecycle(), test_projects_http_api()

### Community 56 - "test_human_steering.py"
Cohesion: 0.17
Nodes (13): Register an ongoing CouncilRun by conversation ID., Unregister an ongoing CouncilRun by conversation ID., register_active_run(), unregister_active_run(), asyncio, Unit and integration tests for Phase 11: Human-in-the-Loop Mid-Debate Steering…, Verify active run registration and steering injection on CouncilRun., Verify that steering injected into a CouncilRun appears in debate prompt, queue… (+5 more)

### Community 57 - "council.py"
Cohesion: 0.15
Nodes (16): Four-stage LLM Council orchestration. Stage 1 Positions - every member answers…, list_unified_models(), Hybrid Council transport and unified model registry. Seamlessly combines local…, Return all available models across local OpenCode and configured external…, LLM Council backend package., collections, httpx, pytest (+8 more)

### Community 59 - "build_instruction"
Cohesion: 0.29
Nodes (8): build_instruction(), intensity_for(), Return the text under '## <heading>', up to the next '## '., Pull one level's row out of Caveman's own Intensity table. Keeping this parsed…, Build the Caveman instruction for a level, or None for "off". Returns None when…, _section(), Verify that build_instruction('max') emits the ultra-dense claim-and-evidence…, test_build_instruction_max_structure_and_contract()

### Community 60 - "post_provider_key"
Cohesion: 0.50
Nodes (4): post_provider_key(), ProviderKeyUpdate, Payload to configure or remove a provider API key., Update or remove a provider API key dynamically.

### Community 61 - "test_exports_and_conversation_id.py"
Cohesion: 0.11
Nodes (18): export_conversation_report(), export_conversation_zip_archive(), Export a council deliberation as a formatted Markdown report document., Export the entire council discussion as a downloadable ZIP package containing…, export_conversation_zip(), format_conversation_markdown(), Format a complete council deliberation into a clean, comprehensive Markdown…, Build an in-memory zip archive containing: - report.md (human-readable… (+10 more)

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
- **159 isolated node(s):** `name`, `private`, `version`, `type`, `dev` (+154 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 443 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CLAUDE.md - Technical Notes for LLM Council` connect `CLAUDE.md - Technical Notes for LLM Council` to `CouncilSession`, `Caveman compression`, `list_models`, `prompts.py`?**
  _High betweenness centrality (0.211) - this node is a cross-community bridge._
- **Why does `CouncilRun` connect `CouncilRun` to `CouncilSession`, `verify_caveman.py`, `test_thinking_quality_and_deduplication.py`, `test_model_eviction.py`, `test_chairman_selection.py`, `generate_conversation_title`, `._pipeline`, `asyncio`, `backend/main.py`, `._check_budget_limits`, `_sum_tokens`, `._open_sessions`, `list_models`, `test_ui_controls_telemetry.py`, `provider_keys.py`, `test_human_steering.py`, `council.py`, `._ask_all`, `._tighten`?**
  _High betweenness centrality (0.205) - this node is a cross-community bridge._
- **Why does `Frontend` connect `CLAUDE.md - Technical Notes for LLM Council` to `icons.jsx`?**
  _High betweenness centrality (0.197) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `CouncilRun` (e.g. with `HybridCouncilSession` and `CouncilSession`) actually correct?**
  _`CouncilRun` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `CouncilSession` (e.g. with `CouncilRun` and `HybridCouncilSession`) actually correct?**
  _`CouncilSession` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _159 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `CouncilSession` be split into smaller, more focused modules?**
  _Cohesion score 0.09388335704125178 - nodes in this community are weakly interconnected._