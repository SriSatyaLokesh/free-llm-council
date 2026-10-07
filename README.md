# Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Cost: 100% Free](https://img.shields.io/badge/Cost-100%25_Free_Unlimited-brightgreen.svg)](#why-free-llm-council)
[![Engine: OpenCode](https://img.shields.io/badge/Engine-OpenCode_Native-blue.svg)](https://opencode.ai)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://python.org)
[![Frontend: React 19](https://img.shields.io/badge/Frontend-React_19_%2B_Vite-61dafb.svg)](https://vitejs.dev)
[![Tests: 62 Passing](https://img.shields.io/badge/Tests-62_Passing-success.svg)](#testing--verification)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/SriSatyaLokesh/llm-council-pro-max/pulls)

![Free LLM Council](header.jpg)

**Free LLM Council** (also known as *OpenCode LLM Council*) is a 100% free, local-first multi-model consensus and AI debate platform powered natively by [OpenCode](https://opencode.ai). 

Bring any complex decision, architecture dilemma, or technical question: every model seated on your council researches the problem using live web tools, **debates peers by name over multiple rounds**, blind peer-reviews each other's reasoning, and an intelligent chairman synthesizes a structured executive verdict with tradeoffs, confidence ratings, and dissenting perspectives.

Originally inspired by Andrej Karpathy's experimental concept, **Free LLM Council** removes the prohibitive paywalls and rate limits of cloud-only multi-agent systems. Instead of burning through OpenRouter credits with 30+ model calls per question, you get unlimited, zero-cost deliberations on your local machine — with optional **BYOK (Bring Your Own Key)** support to seat frontier cloud models alongside your local free models whenever needed.

---

## TL;DR: Why Free LLM Council?

Running a true multi-model deliberative council across opening statements, multi-round rebuttals, blind scoring, and chairman synthesis generates **25 to 40+ model invocations per question**. On paid API providers or OpenRouter, a single council discussion can cost multiple dollars or immediately trigger `429 Too Many Requests` rate limits.

**Free LLM Council solves this by anchoring directly to OpenCode:**
- 💸 **100% Free & Unlimited:** Drive your locally hosted and free OpenCode models at zero API cost.
- 🔑 **BYOK Hybrid Cloud Seating:** Seat Claude 3.5 Sonnet, GPT-4o, o1, or DeepSeek R1 directly alongside free local models via the in-app key modal.
- 📁 **Studio Workspace:** Group deliberations into Project Folders, move debates between folders, rename inline, or archive completed sessions.
- 🎯 **Human-in-the-Loop Mid-Debate Steering:** Inject operator guidance and reference URLs mid-flight that take effect in subsequent rounds and the final synthesis.
- 📦 **Dual Deliberation Reports & Interactive Viewer:** Toggle between **Executive Summary** and **Deep-Dive Technical Matrix** reports with comparative model tables, ASCII deliberation flow diagrams, and "The Why" strategic trade-off matrices. One-click copy, direct `.md` / `.zip` downloads, and publication-grade Print/PDF export.
- ⚡ **Caveman Token Compression:** Integrate official Caveman skill compression (`lite`, `full`, `ultra`) for up to ~48% fewer intermediate tokens while keeping full prose in the final report.
- 🎨 **Modern Single-Window UI:** Zero-scroll window layout, live stage progress tracking (RunRail), tool execution traces, and clean Lucide-style vector SVG icons.

---

## Comparison: Upstream Concept vs. Free LLM Council

| Capability | Original Karpathy Concept | Free LLM Council (OpenCode-Powered) |
|---|---|---|
| **API Cost & Limits** | Paid per-token via OpenRouter (Rate limits & fees) | **100% Free & Unlimited** via local OpenCode |
| **Frontier Cloud Models** | Locked to OpenRouter | **BYOK Hybrid**: Seat Claude, GPT-4o, DeepSeek R1, Groq via in-app key modal |
| **Workspace Organization** | Flat unstructured conversation list | **Project Folders**: Structured hierarchy, folder migration, inline rename & archive/restore |
| **Deliberation Reports** | None | **Dual Reports & In-App Viewer**: Executive Brief + Deep-Dive Matrix with ASCII diagrams, comparative tables, and Print/PDF export |
| **Human-in-the-Loop** | Autonomous / non-interactive | **Live Mid-Debate Steering**: Inject guidance directives and URLs mid-flight |
| **Chairman Selection** | Hardcoded or first model | **Intelligent Capability Matrix**: Context-window & reasoning ranking with auto-failover |
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

1. **Stage 1 — Independent Opening Positions:** Every seated model independently investigates the prompt using live web search and workspace inspection. No model sees peer responses, ensuring diverse initial angles.
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

## Frequently Asked Questions (FAQ)

### How is Free LLM Council 100% free?
Free LLM Council runs on top of [OpenCode](https://opencode.ai), which connects to local and free AI models hosted on your machine or through zero-cost endpoints. By running locally, you never incur API token fees, credit card charges, or rate-limit blocks regardless of how many debate rounds or models you configure.

### Can I still use commercial models like Claude 3.5 Sonnet, GPT-4o, or DeepSeek R1?
Yes. With our **BYOK (Bring Your Own Key)** hybrid architecture, you can click the **Provider Keys** button in the sidebar and enter your API keys for OpenRouter, OpenAI, Anthropic, Groq, or DeepSeek. These models will seat alongside your free OpenCode models in the roster. Keys are kept securely in-memory and can be cleared at any time.

### How does this differ from Andrej Karpathy's original `llm-council`?
Andrej Karpathy's prototype was an experimental script coupled to OpenRouter that lacked persistence, folders, exports, steering, error recovery, and cost controls. Free LLM Council transforms that idea into a complete production platform with local OpenCode integration, mid-debate human steering, project hierarchy, full ZIP/Markdown exports, Caveman token compression, automatic failover, and a modern single-window UI.

### Does Free LLM Council send my code or files to external servers?
No. Local OpenCode deliberations run completely within your environment. Furthermore, council members operate in a strict read-only sandbox: they can inspect files to answer technical questions but are cryptographically blocked by canaries from writing or modifying your workspace.

### What is Caveman Compression and why does it matter?
Caveman compression applies the official [Caveman](https://github.com/JuliusBrussee/caveman) skill to model-to-model debate rounds (Stage 2). Because humans only read the final verdict, intermediate rounds are compressed to eliminate conversational filler, saving up to **~48% of output tokens** while instructing the chairman to expand findings back into complete, polished prose for the final verdict.

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
- **Standards:** Compliant with `llms.txt` specification for AI crawlers, agentic indexers, and LLM search engines.

---

## Citation

If you use Free LLM Council in your research, technical blogs, or applications, please cite:

```bibtex
@software{free_llm_council,
  author = {Satya K},
  title = {Free LLM Council: OpenCode-Powered Multi-Model Deliberation Engine},
  year = {2026},
  url = {https://github.com/SriSatyaLokesh/llm-council-pro-max}
}
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.
