# Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine

![Free LLM Council](header.jpg)

**Free LLM Council** is a 100% free, local-first multi-model consensus and debate platform powered by [OpenCode](https://opencode.ai). Bring any complex decision, architecture dilemma, or design question: every model seated on your council researches the problem with live web tools, **debates peers by name over multiple rounds**, blind peer-reviews each other's arguments, and an intelligent chairman synthesizes a final verdict with tradeoffs, confidence ratings, and dissenting views.

Originally inspired by Andrej Karpathy's experimental concept, **Free LLM Council** completely eliminates the expensive API paywall and rate limits of traditional multi-agent setups. Instead of burning through OpenRouter credits with 30+ model calls per question, you get unlimited, zero-cost deliberations on your local machine — with optional **BYOK (Bring Your Own Key)** support to seat frontier cloud models alongside your free local models whenever desired.

---

## Why Free LLM Council?

Running a true multi-model council across opening positions, multi-round rebuttals, blind scoring, and chairman synthesis takes **25 to 40+ model invocations per question**. On paid API providers or OpenRouter, a single discussion can cost several dollars or instantly trigger `429 Too Many Requests` rate limits.

**Free LLM Council solves this by anchoring natively to OpenCode:**
- 💸 **100% Free & Unlimited:** Drive your locally hosted and free OpenCode models at zero API cost.
- 🔑 **BYOK Hybrid Cloud Seating:** Seat Claude 3.5 Sonnet, GPT-4o, o1, or DeepSeek R1 directly alongside free local models using the in-app key modal.
- 📁 **Studio Workspace:** Group deliberations into Project Folders, move debates between folders, rename inline, or archive completed sessions.
- 🎯 **Human-in-the-Loop Mid-Debate Steering:** Inject operator guidance and reference URLs mid-flight that take effect in subsequent rounds and the final synthesis.
- 📦 **One-Click Deliberation Exports:** Download publication-ready Markdown reports or complete ZIP packages (`report.md`, `conversation.json`, `summary.txt`).
- ⚡ **Caveman Token Compression:** Integrate official Caveman skill compression (`lite`, `full`, `ultra`) for up to ~48% fewer intermediate tokens while keeping full prose in the final report.
- 🎨 **Modern Single-Window UI:** Zero-scroll window layout, live stage progress tracking (RunRail), tool execution traces, and clean Lucide-style vector SVG icons.

---

## Feature Comparison

| Feature | Original Concept | Free LLM Council (OpenCode-Powered) |
|---|---|---|
| **API Cost** | Paid per-token via OpenRouter | **100% Free & Unlimited** via local OpenCode |
| **Frontier Cloud Models** | Locked to OpenRouter | **BYOK Hybrid**: Seat Claude, GPT-4o, DeepSeek R1, Groq via in-app key modal |
| **Workspace Organization** | Flat unstructured list | **Project Folders**: Structured folders, folder migration, inline rename & archive/restore |
| **Deliberation Exports** | None | **1-Click Export**: Standalone Markdown reports + complete ZIP deliberation packages |
| **Human-in-the-Loop** | Static & autonomous | **Live Mid-Debate Steering**: Inject guidance directives and URLs mid-flight |
| **Chairman Selection** | Hardcoded / first model | **Intelligent Capability Matrix**: Context-window & reasoning ranking with auto-failover |
| **Thinking Depth** | Static / uniform | **Granular Controls**: Configurable per-model reasoning depth (`low` to `xhigh`) + presets |
| **Budget & Safety Caps** | Unbounded runtime | **Token & Time Limits**: Early conclusion handoff cleanly preserving review & verdict |
| **Fault Tolerance** | Single failure aborts run | **Model Eviction**: Unresponsive models are evicted; the council continues degraded |
| **Debate Compression** | Baseline text | **Caveman Compression**: Verified ~48% output token savings on intermediate turns |
| **User Interface** | Basic chat layout | **Studio Dashboard**: Single-window non-scrolling UI, live progress rails, unified SVG icons |

---

## How a Deliberation Works

```
Stage 1: Opening Positions  ──►  Stage 2: Named Peer Debate  ──►  Stage 3: Blind Peer Review  ──►  Stage 4: Chairman Verdict
(Independent + Live Web)          (Rebuttal, Concession, Caveman)   (Anonymized Matrix Scoring)       (Synthesis & Tradeoffs)
```

1. **Stage 1 — Independent Opening Positions:** Every seated model independently investigates the prompt using live web search and workspace inspection. No model sees any peer responses, ensuring diverse initial angles.
2. **Stage 2 — Multi-Round Named Debate:** Models see each other's opening positions **by name**. Over multiple rounds, each model must rebut peer arguments, concede points found persuasive, declare whether it is updating or defending its stance, and surface hidden tradeoffs.
3. **Stage 3 — Blind Peer Review:** Opening arguments are anonymized as `Response A`, `Response B`, etc. Models blindly score and rank their peers, generating an aggregate ranking matrix free from brand bias.
4. **Stage 4 — Chairman Synthesis & Verdict:** The highest-capacity chairman analyzes the full deliberation transcript and produces an executive decision with structured **Decision**, **Reasoning**, **Tradeoffs**, **Dissent**, and **Confidence**.

---

## Quickstart & Setup

Anyone with **Python**, **OpenCode**, and **Node.js** can launch Free LLM Council in under two minutes.

### 1. Prerequisites
- **Python 3.11+**
- **Node.js 18+**
- **OpenCode** (Install from [opencode.ai](https://opencode.ai))

### 2. Start OpenCode Service
Start your local OpenCode server and verify configured models:
```bash
opencode service start
opencode models
```

### 3. Clone & Install

```bash
git clone https://github.com/SriSatyaLokesh/llm-council-pro-max.git
cd llm-council-pro-max
```

**Backend:**
```bash
# Using uv (fastest)
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

### 4. Launch the Platform

Run the unified startup script:
```bash
./start.sh
```

Or run manually in two terminals:
- **Backend (Port 8001):** `uv run python -m backend.main`
- **Frontend (Port 5173):** `cd frontend && npm run dev`

Open **`http://localhost:5173`** in your browser.

---

## Configuration & BYOK Cloud Providers

The local OpenCode server is auto-detected at startup. If you want to seat frontier cloud models alongside your free local models, you can paste keys directly into the in-app **Provider Key Modal** or configure them via environment variables:

| Variable | Default | Purpose |
|---|---|---|
| `OPENCODE_SERVER_URL` | Auto-detected (`http://127.0.0.1:4096`) | Local OpenCode service endpoint |
| `OPENCODE_SERVER_PASSWORD` | Auto-detected from `service.json` | Local OpenCode auth token |
| `OPENROUTER_API_KEY` | None | BYOK OpenRouter access (Claude, GPT-4o, DeepSeek R1) |
| `OPENAI_API_KEY` | None | BYOK direct OpenAI API access |
| `ANTHROPIC_API_KEY` | None | BYOK direct Anthropic Claude API access |
| `GROQ_API_KEY` | None | BYOK direct Groq API access (Llama 3.3 70B) |
| `DEEPSEEK_API_KEY` | None | BYOK direct DeepSeek API access |
| `DEBATE_ROUNDS` | `2` | Number of Stage 2 debate rounds |
| `DEBATE_MODE` | `off` | Compression level (`off`, `lite`, `full`, `ultra`) |
| `PER_MODEL_TIMEOUT` | `300` | Per-turn execution timeout in seconds |

---

## Testing & Verification

Free LLM Council includes **62 automated unit and integration tests**:

```bash
# Run full test suite
pytest

# Test specific components
pytest tests/unit/test_projects_and_folders.py
pytest tests/unit/test_human_steering.py
pytest tests/unit/test_exports_and_conversation_id.py
pytest tests/unit/test_hybrid_providers.py
pytest tests/unit/test_caveman_max.py
```

Run live sandbox validation scripts:
```bash
python -m backend.verify_opencode   # Verifies discovery, live web tools, and canary write-block
python -m backend.verify_api        # Full SSE streaming & lifecycle verification
python -m backend.verify_caveman    # Controlled Caveman compression A/B benchmark
```

---

## Tech Stack

- **Backend:** FastAPI, Python 3.13, Async HTTPX, SSE Streaming.
- **Frontend:** React 19, Vite, React Markdown, Custom Lucide-style SVG Vector Icon Pack.
- **Local Engine:** [OpenCode](https://opencode.ai) HTTP API with live web search & read-only workspace sandboxing.
- **Storage:** Atomically written JSON in `data/conversations/` and `data/projects.json` (zero user debates tracked in git).

---

## License

MIT License. See [LICENSE](LICENSE) for details.
