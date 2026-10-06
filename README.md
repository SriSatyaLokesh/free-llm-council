# LLM Council Pro Max

![llmcouncil](header.jpg)

**LLM Council Pro Max** is a deliberative multi-model consensus and debate engine. Bring any complex decision, architecture dilemma, or design question: every model seated on the council researches the problem with live web tools, **debates peers by name over multiple rounds**, blind peer-reviews each other's reasoning, and an intelligent chairman synthesizes a final verdict with tradeoffs, confidence levels, and dissenting views.

Originally inspired by Andrej Karpathy's experimental concept, **Pro Max** evolves the project into a fault-tolerant, hybrid cloud/local production platform with advanced organizational workflows, mid-flight human steering, and rigorous token economics.

---

## What Pro Max Adds Over the Original Concept

| Capability | Original Council | LLM Council Pro Max |
|---|---|---|
| **Model Providers** | Local OpenCode only | **Hybrid Architecture**: Free local OpenCode + frontier cloud models (OpenRouter, OpenAI, Anthropic, Groq, DeepSeek) |
| **Workspace Organization** | Flat unstructured history | **Project Folders & Debates**: Organize deliberations in folders, move debates between folders, inline rename, and archive/restore |
| **Deliberation Exports** | None | **One-Click Export**: Standalone Markdown reports + full deliberation ZIP bundles (`report.md`, `conversation.json`, `summary.txt`) |
| **Human-in-the-Loop** | Autonomous / non-interactive | **Live Mid-Debate Steering**: Inject domain facts, focus directives, and URLs mid-flight that take effect in subsequent rounds and the verdict |
| **Chairman Selection** | Hardcoded or first model | **Intelligent Selection & Failover**: Automatic reasoning/context capability ranking with dynamic failover if the primary chairman fails |
| **Thinking Depth** | Static / uniform | **Granular Reasoning Controls**: Configurable per-model thinking depth (`low`, `medium`, `high`, `max`, `xhigh`) + preset persistence |
| **Budget & Safety Caps** | Unbounded runtime | **Token & Time Budgeting**: Soft & hard token caps with clean early debate conclusion handed off to review and verdict |
| **Fault Tolerance** | Single model error crashes run | **Automated Model Eviction**: Unresponsive models are evicted; the council continues degraded without crashing |
| **Debate Compression** | Baseline text | **Caveman Compression**: Official Caveman skill integration (`lite`, `full`, `ultra`) with measured token savings |
| **User Interface** | Basic chat layout | **Modern UI System**: Single-window non-scrolling dashboard, live RunRail progress, tool execution traces, zero raw emojis (clean Lucide-style SVG pack) |

---

## How a Deliberation Works

1. **Stage 1 — Independent Opening Positions**
   Every seated member formulates an independent answer with live web search/fetch and read-only workspace access. Members cannot see each other, ensuring uncorrupted, diverse initial perspectives.

2. **Stage 2 — Multi-Round Named Debate**
   Members see each other's opening arguments **by name**. Over configured debate rounds, each member must:
   - Rebut specific peer arguments directly.
   - Concede points they found persuasive.
   - Declare whether they are **updating** or **defending** their thesis.
   - Highlight overlooked tradeoffs or blindspots.

3. **Stage 3 — Blind Peer Review**
   Opening positions are anonymized as `Response A`, `Response B`, etc. Each model evaluates and ranks its peers' work blindly without bias toward specific model names. An aggregate scoring table ranks peer performance.

4. **Stage 4 — Chairman Synthesis & Verdict**
   An intelligent chairman analyzes the complete deliberation transcript and delivers a structured verdict:
   - **Decision**
   - **Reasoning**
   - **Tradeoffs**
   - **Dissent**
   - **Confidence Score**

---

## Key Features

### 1. Hybrid Local + Frontier Cloud Provider Engine
- **Local & Free by Default:** Connects automatically to local [OpenCode](https://opencode.ai) models at zero API cost.
- **Frontier Cloud Seating:** Seat Claude 3.5 Sonnet, GPT-4o, o1, DeepSeek R1, or Groq alongside local models using the in-app Provider Key Modal or environment variables.
- Keys are kept securely in-memory and can be configured or cleared dynamically without restarting the server.

### 2. Workspace Organization & Project Folders
- Group related debates into **Project Folders** (e.g., *Database Architecture*, *Security Reviews*).
- Move debates seamlessly between folders or keep them standalone.
- **Inline Renaming:** Rename any debate directly from the sidebar.
- **Archiving:** Archive concluded deliberations to keep your active workspace clutter-free, with a collapsible drawer to inspect or restore them at any time.

### 3. Human-in-the-Loop Mid-Debate Steering
- Notice a model hallucinating or going down an unproductive rabbit hole?
- Click **Steer Debate** on the live progress rail to inject operator directives and reference URLs.
- Injected guidance is automatically woven into upcoming debate rounds and the chairman's final synthesis.

### 4. Comprehensive Deliberation Exports
- **Markdown Report:** Download a publication-ready Markdown executive report covering the question, verdict, dissent, debate history, and peer reviews.
- **Complete ZIP Archive:** One-click download containing `report.md`, raw `conversation.json`, and an executive `summary.txt`.
- Shareable Conversation IDs with one-click clipboard copying.

### 5. Token Economics & Caveman Compression
- Supports the official [Caveman](https://github.com/JuliusBrussee/caveman) compression skill on intermediate debate rounds:
  - `off`: Standard prose.
  - `lite`: Removes filler and hedging while retaining full sentence structure.
  - `full`: Classic caveman shorthand (~48% fewer output tokens).
  - `ultra`: Minimal unambiguous syntax.
- The chairman automatically expands shorthand back into pristine prose for the final verdict.

---

## Setup & Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- [OpenCode](https://opencode.ai) (optional, if running free local models)

### 1. Clone & Configure Remote
```bash
git clone https://github.com/SriSatyaLokesh/llm-council-pro-max.git
cd llm-council-pro-max
```

### 2. Install Dependencies

**Backend:**
```bash
# Using uv (recommended)
uv sync

# Or using standard pip
pip install -e .
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### 3. Start the Platform

Run the unified start script:
```bash
./start.sh
```

Or launch services manually in two terminals:

**Backend (Port 8001):**
```bash
uv run python -m backend.main
```

**Frontend (Port 5173):**
```bash
cd frontend
npm run dev
```

Open your browser at **`http://localhost:5173`**.

---

## Configuration

All configuration is accessible directly from the UI, but can also be set via environment variables:

| Variable | Default | Description |
|---|---|---|
| `OPENCODE_SERVER_URL` | Auto-detected | Base URL of local OpenCode server |
| `OPENCODE_SERVER_PASSWORD` | Auto-detected | OpenCode authentication password |
| `OPENCODE_WORKSPACE` | Current directory | Read-only workspace path available to council tools |
| `OPENROUTER_API_KEY` | None | Optional OpenRouter API key |
| `OPENAI_API_KEY` | None | Optional OpenAI API key |
| `ANTHROPIC_API_KEY` | None | Optional Anthropic API key |
| `DEBATE_ROUNDS` | `2` | Number of Stage 2 debate rounds |
| `DEBATE_MODE` | `off` | Compression mode (`off`, `lite`, `full`, `ultra`) |
| `PER_MODEL_TIMEOUT` | `300` | Timeout in seconds per model turn |

---

## Verification & Test Suite

LLM Council Pro Max is covered by a suite of **62 automated unit and integration tests**:

```bash
# Run complete test suite
pytest

# Verify specific subsystems
pytest tests/unit/test_projects_and_folders.py
pytest tests/unit/test_human_steering.py
pytest tests/unit/test_exports_and_conversation_id.py
pytest tests/unit/test_hybrid_providers.py
pytest tests/unit/test_chairman_selection.py
```

You can also run standalone verification scripts against live providers:
```bash
python -m backend.verify_opencode   # Discovery, tools, and write-sandbox canary
python -m backend.verify_api        # Full SSE streaming & lifecycle verification
python -m backend.verify_caveman    # Controlled compression A/B benchmark
```

---

## Tech Stack

- **Backend:** FastAPI, Python 3.13, Async HTTPX, Server-Sent Events (SSE).
- **Frontend:** React 19, Vite, React Markdown, Custom Lucide-style SVG Icon Set.
- **Storage:** Atomically-written JSON persistence in `data/conversations/` and `data/projects.json`.
- **Knowledge Graph:** Persistent AST code graph via `graphify`.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
