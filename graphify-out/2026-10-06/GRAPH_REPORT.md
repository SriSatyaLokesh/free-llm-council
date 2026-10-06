# Graph Report - llm-council  (2026-10-06)

## Corpus Check
- 66 files · ~62,836 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 20 file(s) not represented in the graph (top: .css 14, (none) 4, .cff 1)

## Summary
- 855 nodes · 1653 edges · 57 communities (47 shown, 10 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 57 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `deaf02ea`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- storage.py
- CouncilSession
- icons.jsx
- verify_caveman.py
- build_instruction
- package.json
- post_provider_key
- test_thinking_quality_and_deduplication.py
- caveman.py
- test_chairman_selection.py
- generate_conversation_title
- Appendix B - Canonical Sources (read these before reinventing)
- CouncilRun
- test_token_budgeting.py
- backend/main.py
- CLAUDE.md - Technical Notes for LLM Council
- ask_many
- BaseModel
- post
- debate_prompt
- 4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)
- opencode_client.py
- delete_conversation
- Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine
- 4. Component Standards
- _service_config_candidates
- list_models
- start.sh
- tests/__init__.py
- 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)
- prompts.py
- tasteskill: Anti-Slop Frontend Skill
- 9. AI TELLS (Forbidden Patterns)
- 11. REDESIGN PROTOCOL
- 3. DEFAULT ARCHITECTURE & CONVENTIONS
- settings.py
- get_active_run
- 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS
- Caveman compression
- 0. BRIEF INFERENCE (Read the Room Before Anything Else)
- 12. THE BLOCK LIBRARY (Contract - Implementations Land Here Iteratively)
- 5. CONTEXT-AWARE PROACTIVITY
- 8. DARK MODE PROTOCOL
- 7. DIAL DEFINITIONS (Technical Reference)
- create_project
- test_hybrid_providers.py
- git-workflow.md
- free-llm-council
- test_human_steering.py
- test_caveman_max.py
- graphify.js
- React + Vite
- AGENTS.md
- rules/graphify.md
- workflows/graphify.md

## God Nodes (most connected - your core abstractions)
1. `CouncilRun` - 57 edges
2. `CouncilSession` - 27 edges
3. `Sidebar()` - 20 edges
4. `get_conversation()` - 19 edges
5. `list_models()` - 16 edges
6. `tasteskill: Anti-Slop Frontend Skill` - 16 edges
7. `HybridCouncilSession` - 15 edges
8. `react` - 15 edges
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

## Communities (57 total, 10 thin omitted)

### Community 0 - "storage.py"
Cohesion: 0.05
Nodes (79): export_conversation_report(), export_conversation_zip_archive(), Update a project name or description., Update conversation metadata such as title or assigned project folder., Export a council deliberation as a formatted Markdown report document., Export the entire council discussion as a downloadable ZIP package containing…, update_conversation(), update_project() (+71 more)

### Community 1 - "CouncilSession"
Cohesion: 0.16
Nodes (14): CouncilSession, _parse_assistant_message(), Any, Flatten an opencode assistant message into text / reasoning / tool calls., One opencode session driven by one council member. The session is reused across…, Create the underlying opencode session., Delete the opencode session so it does not clutter the user's list., Replace this session's permission ruleset mid-run. Used to tighten the sandbox… (+6 more)

### Community 2 - "icons.jsx"
Cohesion: 0.09
Nodes (55): Frontend, B. Workspace Header & Breadcrumbs, api, App(), ChatInterface(), DebateMode(), LEVEL_LABELS, AlertTriangle() (+47 more)

### Community 3 - "verify_caveman.py"
Cohesion: 0.27
Nodes (10): council_permissions(), Build the permission ruleset for council members. Allow the research and read…, main(), _median(), one_shot(), part_one(), part_two(), Measures what the Caveman levels actually do, on this council. python -m… (+2 more)

### Community 4 - "build_instruction"
Cohesion: 0.40
Nodes (6): build_instruction(), intensity_for(), Return the text under '## <heading>', up to the next '## '., Pull one level's row out of Caveman's own Intensity table. Keeping this parsed…, Build the Caveman instruction for a level, or None for "off". Returns None when…, _section()

### Community 5 - "package.json"
Cohesion: 0.06
Nodes (35): allowScripts, esbuild@0.25.12, dependencies, react, react-dom, react-markdown, devDependencies, eslint (+27 more)

### Community 6 - "post_provider_key"
Cohesion: 0.50
Nodes (4): post_provider_key(), ProviderKeyUpdate, Payload to configure or remove a provider API key., Update or remove a provider API key dynamically.

### Community 7 - "test_thinking_quality_and_deduplication.py"
Cohesion: 0.09
Nodes (27): pytest, make_mock_session(), asyncio, Unit tests for Phase 2: Dynamic Member Fault-Tolerance & Model Eviction., If a model succeeds in Stage 1 but crashes in Debate Round 1, it must be…, Create a mock CouncilSession that records ask() calls and session lifecycle., If the designated chairman fails during deliberation, the council must promote…, When run_stream is used, an eviction should emit a 'model_evicted' event. (+19 more)

### Community 8 - "caveman.py"
Cohesion: 0.20
Nodes (12): Intelligent capability scoring matrix for LLM Council Chairman election. Ranks…, is_installed(), load_skill(), Path, Official Caveman compression, loaded at runtime from the installed skill.…, What the UI needs to render the mode picker honestly., Read the installed SKILL.md, cached against the file's mtime. Returns None when…, skill_path() (+4 more)

### Community 9 - "test_chairman_selection.py"
Cohesion: 0.11
Nodes (25): Any, Select the highest capability model ID from a list of model dicts or model IDs., Compute an intelligence score (0 to 100+) for a given model dict or model ID…, score_model_capability(), select_best_chairman(), Work out who sits on the council and who chairs it. Defaults to every model…, resolve_roster(), default_chairman() (+17 more)

### Community 10 - "generate_conversation_title"
Cohesion: 0.25
Nodes (8): generate_conversation_title(), Short title for a conversation, using the fastest available model., Send a message and stream the council as it runs. Emits Server-Sent Events as…, Request to send a message in a conversation., send_message_stream(), emit(), event_generator(), SendMessageRequest

### Community 11 - "Appendix B - Canonical Sources (read these before reinventing)"
Cohesion: 0.09
Nodes (21): APPENDICES - Real Source-Backed Reference Material, Appendix A - Install Commands per Design System, Appendix B - Canonical Sources (read these before reinventing), Appendix C - Apple Liquid Glass: Honest Web Approximation, Apple Liquid Glass (Apple platforms only), Atlassian, Bootstrap, Carbon (+13 more)

### Community 12 - "CouncilRun"
Cohesion: 0.07
Nodes (36): _aggregate_block(), calculate_aggregate_rankings(), _clip(), CouncilRun, _call_make(), emit(), _debate_block(), _label() (+28 more)

### Community 13 - "test_token_budgeting.py"
Cohesion: 0.05
Nodes (41): Live test script executing an end-to-end deliberation across real OpenCode…, httpx, io, json, Tests for conversation ID exposure, markdown report export, and zip bundle…, Verify markdown generator produces structured sections., Verify in-memory zip archive packages report.md, conversation.json, and…, test_export_conversation_zip_archive() (+33 more)

### Community 14 - "backend/main.py"
Cohesion: 0.10
Nodes (24): get_conversation(), get_models(), get_project(), get_provider_keys(), health(), list_conversations(), list_projects(), FastAPI backend for LLM Council. (+16 more)

### Community 15 - "CLAUDE.md - Technical Notes for LLM Council"
Cohesion: 0.18
Nodes (10): parse_verdict(), Split a chairman response into its sections. Falls back to putting everything…, CLAUDE.md - Technical Notes for LLM Council, Custom agents do not work from a project config, graphify, Project overview, Prompt design, Sandbox (+2 more)

### Community 17 - "BaseModel"
Cohesion: 0.22
Nodes (9): Conversation, ConversationMetadata, Full conversation with all messages., Request to update a project., Request to update a conversation (project assignment, title, or archive status)., Conversation metadata for list view., UpdateConversationRequest, UpdateProjectRequest (+1 more)

### Community 18 - "post"
Cohesion: 0.18
Nodes (11): create_conversation(), CreateConversationRequest, post_settings(), prune_empty_conversations(), Change live council settings. Takes effect on the next debate round., Create a new conversation., Prune all empty abandoned conversations (0 messages)., Request to create a new conversation. (+3 more)

### Community 20 - "debate_prompt"
Cohesion: 0.20
Nodes (10): debate_prompt(), Stage 4: the chairman's decision. Never compressed - a human reads this., Stage 2: named cross-examination, one round at a time. `caveman_instruction` is…, verdict_prompt(), Verify that verdict_prompt alerts the chairman to expand compressed debate…, Verify that debate_prompt embeds the Caveman max instruction cleanly., test_chairman_prompt_contains_expansion_directive_for_max(), test_prompts_integrate_max_contract() (+2 more)

### Community 23 - "4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)"
Cohesion: 0.17
Nodes (12): 4.10 Quotes & Testimonials, 4.11 Page Theme Lock (Light / Dark Mode Consistency), 4.1 Typography, 4.2 Color Calibration, 4.3 Layout Diversification, 4.4 Materiality, Shadows, Cards, 4.5 Interactive UI States, 4.6 Data & Form Patterns (+4 more)

### Community 24 - "opencode_client.py"
Cohesion: 0.13
Nodes (17): asyncio, Configuration for the LLM Council. The council runs entirely on models that are…, LLM Council backend package., Client for the local opencode server. This module replaces the old OpenRouter…, council_sessions(), main(), End-to-end test of the HTTP API, including the SSE streaming path. Creates a…, Council sessions currently left in the user's opencode session list. (+9 more)

### Community 25 - "delete_conversation"
Cohesion: 0.40
Nodes (5): delete_conversation(), delete_project(), Delete a project folder and revert its debates to independent mode., Delete a conversation by ID., delete

### Community 27 - "Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine"
Cohesion: 0.10
Nodes (20): 1. Prerequisites, 2. Start OpenCode Service, 3. Clone & Install, 4. Launch the Platform, Can I still use commercial models like Claude 3.5 Sonnet, GPT-4o, or DeepSeek R1?, Citation, Comparison: Upstream Concept vs. Free LLM Council, Configuration & BYOK Cloud Providers (+12 more)

### Community 28 - "4. Component Standards"
Cohesion: 0.17
Nodes (11): 1. Dials & Atmosphere, 2. Color Palette & Surface Elevation, 3. Typography & Micro-Hierarchy, 4. Component Standards, 5. Performance, Ergonomics & Fast Handling, A. Left-Hand Sidebar (Workspace Tree), Accents & Signal Colors, C. Live RunRail (Real-Time Progress) (+3 more)

### Community 29 - "_service_config_candidates"
Cohesion: 0.67
Nodes (3): Path, Possible locations of opencode's service.json., _service_config_candidates()

### Community 30 - "list_models"
Cohesion: 0.14
Nodes (22): parse_ranking_from_text(), Extract the ordered labels from a 'FINAL RANKING:' block., _auth_headers(), diagnose_connection(), get_server_password(), get_server_url(), list_models(), _location_params() (+14 more)

### Community 34 - "10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)"
Cohesion: 0.20
Nodes (10): 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know), Animation Library Choice, Cards & Containers, Galleries & Media, Hero Paradigms, Layout & Grids, Micro-Interactions & Effects, Navigation & Menus (+2 more)

### Community 36 - "prompts.py"
Cohesion: 0.25
Nodes (7): position_prompt(), Prompts for the four council stages. Kept in one place so the wording of each…, Stage 3: blind, anonymized scoring of the positions., Stage 1: independent first opinion. Never compressed - a human reads this., Short conversation title., review_prompt(), title_prompt()

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
Cohesion: 0.08
Nodes (31): get_settings(), Current council settings, plus whether the official Caveman skill is installed.…, Send a message and run the full four-stage council. Returns the complete…, send_message(), get_debate_mode(), get_settings(), get_time_limit_seconds(), get_token_budget_total() (+23 more)

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

### Community 51 - "test_hybrid_providers.py"
Cohesion: 0.07
Nodes (38): HybridCouncilSession, list_unified_models(), Any, AsyncClient, Hybrid Council transport and unified model registry. Seamlessly combines local…, Return all available models across local OpenCode and configured external…, Unified session wrapper routing to either local OpenCode daemon or direct…, delete_key() (+30 more)

### Community 56 - "test_human_steering.py"
Cohesion: 0.17
Nodes (13): Register an ongoing CouncilRun by conversation ID., Unregister an ongoing CouncilRun by conversation ID., register_active_run(), unregister_active_run(), asyncio, Unit and integration tests for Phase 11: Human-in-the-Loop Mid-Debate Steering…, Verify active run registration and steering injection on CouncilRun., Verify that steering injected into a CouncilRun appears in debate prompt, queue… (+5 more)

### Community 57 - "test_caveman_max.py"
Cohesion: 0.18
Nodes (10): asyncio, Real, non-mocked tests for Phase 5: Caveman Max Mode & Debate Compression.…, Functional test: When debateMode is 'max', CouncilRun marks…, Ensure 'max' is recognized as a first-class debate compression level., Verify that build_instruction('max') emits the ultra-dense claim-and-evidence…, HTTP integration test: FastAPI POST /api/settings accepts debateMode='max'., test_build_instruction_max_structure_and_contract(), test_caveman_levels_includes_max() (+2 more)

### Community 66 - "graphify.js"
Cohesion: 0.40
Nodes (3): IMPORTANT: keep the reminder string free of backticks and $(...) constructs., ref_fs, ref_path

### Community 69 - "React + Vite"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

## Knowledge Gaps
- **161 isolated node(s):** `name`, `private`, `version`, `type`, `dev` (+156 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 446 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CLAUDE.md - Technical Notes for LLM Council` connect `CLAUDE.md - Technical Notes for LLM Council` to `CouncilSession`, `icons.jsx`, `Caveman compression`, `list_models`?**
  _High betweenness centrality (0.211) - this node is a cross-community bridge._
- **Why does `CouncilRun` connect `CouncilRun` to `CouncilSession`, `verify_caveman.py`, `test_thinking_quality_and_deduplication.py`, `test_chairman_selection.py`, `generate_conversation_title`, `settings.py`, `test_token_budgeting.py`, `backend/main.py`, `test_hybrid_providers.py`, `test_human_steering.py`, `test_caveman_max.py`, `list_models`?**
  _High betweenness centrality (0.205) - this node is a cross-community bridge._
- **Why does `Frontend` connect `icons.jsx` to `CLAUDE.md - Technical Notes for LLM Council`?**
  _High betweenness centrality (0.197) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `CouncilRun` (e.g. with `HybridCouncilSession` and `CouncilSession`) actually correct?**
  _`CouncilRun` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `CouncilSession` (e.g. with `CouncilRun` and `HybridCouncilSession`) actually correct?**
  _`CouncilSession` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _161 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `storage.py` be split into smaller, more focused modules?**
  _Cohesion score 0.051791629027401385 - nodes in this community are weakly interconnected._