# JARVIS Project State & Context

> **CRITICAL FOR ALL AI AGENTS & DEVELOPERS:**
> This document is the **Single Source of Truth** for current project status, active phase, architectural decisions, and next steps.
> Whenever a new chat session begins or an agent is summoned, **read this file first** to immediately align with current project state without relying on chat memory.

---

## 1. Project Identification
- **Project Name:** JARVIS (v1)
- **Target OS:** Ubuntu Linux (x86_64 / arm64)
- **Primary Language:** Python 3.11+
- **Project Directory:** `/home/abynxv/Projects/jarvis`
- **Current Milestone:** **Phase 1: Foundation, LLM Engine & Persistent Memory**
- **Status:** Initialized documentation & architecture specifications; ready to scaffold codebase and start Phase 1.

---

## 2. Capability Matrix (v1 Baseline)

| Capability | Phase | Status | Primary Component |
| :--- | :---: | :---: | :--- |
| **1. Natural LLM Chat** | Phase 1 | 🟡 Ready for Dev | `jarvis.core.llm` (Ollama, OpenAI, Claude, Gemini) |
| **2. Persistent Memory** | Phase 1 | 🟡 Ready for Dev | `jarvis.memory` (SQLite + Session Store) |
| **3. Web Search** | Phase 2 | ⚪ Planned | `jarvis.tools.web_search` (DuckDuckGo / Tavily) |
| **4. PDF Reader & Summarizer** | Phase 2 | ⚪ Planned | `jarvis.tools.pdf_reader` (PyMuPDF / pypdf) |
| **5. Ubuntu App Launcher** | Phase 3 | ⚪ Planned | `jarvis.tools.app_manager` (`.desktop` / `gio`) |
| **6. Approved Terminal Commands** | Phase 3 | ⚪ Planned | `jarvis.tools.terminal_runner` + HITL Safety Gate |
| **7. Voice (Listen & Speak)** | Phase 4 | ⚪ Planned | `jarvis.voice` (`faster-whisper` + `piper`/`edge-tts`) |
| **8. Multi-Agent Architecture** | Phase 6 | ⚪ Planned (v2) | `jarvis.agents` (LangGraph Multi-Agent Team) |

*Status Legend: ⚪ Planned | 🟡 Ready for Dev / In Progress | 🟢 Complete & Verified*

---

## 3. Directory Layout

```text
/home/abynxv/Projects/jarvis/
├── README.md               # Overview and documentation index
├── PROJECT_STATE.md        # Living project context for agentic workflows (THIS FILE)
├── docs/
│   ├── ARCHITECTURE.md     # System architecture, data flows, and component specs
│   └── PHASES.md           # Implementation roadmap, milestones, and acceptance criteria
├── data/                   # Persistent local storage (gitignored: sqlite db, chroma data)
├── jarvis/                 # Core Python package (to be scaffolded)
│   ├── __init__.py
│   ├── cli/                # Terminal interface & interactive REPL
│   ├── core/               # Configuration, LLM client abstraction, agent loop, safety gate
│   ├── memory/             # SQLite conversation store & vector memory
│   ├── tools/              # Tools (web_search, pdf_reader, app_manager, terminal_runner)
│   └── voice/              # Audio capture, STT (Whisper), TTS (Piper/Edge-TTS)
├── tests/                  # Automated test suite
├── .env.example            # Template for environment variables and API keys
├── requirements.txt        # Python dependency manifest
└── pyproject.toml          # Package configuration
```

---

## 4. Architectural Decision Records (ADR)

- **ADR-001 (Agentic Workflow Documentation):** Adopt markdown-based persistent project state (`PROJECT_STATE.md`, `ARCHITECTURE.md`, `PHASES.md`) committed to the repository so any subsequent agent or chat session can immediately resume with full context.
- **ADR-002 (Human-in-the-Loop Terminal Safety):** Shell commands are strictly tiered. Destructive or state-altering commands (e.g. `apt`, `rm`, `systemctl`, `cp`, `mv`) require interactive terminal confirmation (`[y/N]`) before execution.
- **ADR-003 (Pluggable LLM Abstraction):** Build a unified `BaseLLMClient` that supports local models (via Ollama for complete offline privacy) as well as cloud API providers (OpenAI, Anthropic Claude, Google Gemini).
- **ADR-004 (Native Ubuntu App Dispatch):** Launch desktop applications using Ubuntu's FreeDesktop standard by inspecting `.desktop` files in `/usr/share/applications` and invoking through `gio launch` / `gtk-launch` to ensure proper environment detachment.
- **ADR-005 (Voice Stack Selection):** Use `faster-whisper` for local CPU/GPU speech-to-text, and `edge-tts` / `piper-tts` for responsive neural voice synthesis.

---

## 5. Next Immediate Steps (Phase 1 Execution)

1. Scaffold the project environment:
   - Create `pyproject.toml` and `requirements.txt`.
   - Create `.env.example` with supported provider keys (`OLLAMA_BASE_URL`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, etc.).
2. Implement Core Foundation:
   - Config loader (`jarvis/core/config.py`).
   - SQLite database schema & manager for conversation sessions (`jarvis/memory/database.py`).
   - LLM abstraction layer (`jarvis/core/llm.py`).
3. Build CLI REPL:
   - Interactive terminal chat (`jarvis/cli/main.py`) with session resumption.
4. Verify Phase 1 acceptance criteria.
