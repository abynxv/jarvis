# JARVIS Project State & Context

> **CRITICAL FOR ALL AI AGENTS & DEVELOPERS:**
> This document is the **Single Source of Truth** for current project status, active phase, architectural decisions, and next steps.
> Whenever a new chat session begins or an agent is summoned, **read this file first** to immediately align with current project state without relying on chat memory.

---

## 1. Project Identification
- **Project Name:** JARVIS (v1)
- **Target OS:** Ubuntu Linux (x86_64 / arm64)
- **Primary Language:** Python 3.12+ / FastAPI / LangGraph
- **Project Directory:** `/home/abynxv/Projects/jarvis`
- **Current Milestone:** **Phase 1: Foundation, LLM Engine & Persistent Memory**
- **Status:** Scaffolding complete; project tree established according to target layout; ready to implement Phase 1.

---

## 2. Capability Matrix (v1 Baseline)

| Capability | Phase | Status | Primary Component |
| :--- | :---: | :---: | :--- |
| **1. Natural LLM Chat** | Phase 1 | 🟡 Ready for Dev | `backend/app/core/llm.py` & `backend/app/agents/assistant.py` |
| **2. Persistent Memory** | Phase 1 | 🟡 Ready for Dev | `backend/app/memory/` (SQLite + Context Manager) |
| **3. Web Search** | Phase 2 | ⚪ Planned | `backend/app/tools/web_search.py` & `backend/app/agents/research.py` |
| **4. PDF Reader & Summarizer** | Phase 2 | ⚪ Planned | `backend/app/rag/` (PyMuPDF / RAG extractor) |
| **5. Ubuntu App Launcher** | Phase 3 | ⚪ Planned | `backend/app/tools/filesystem.py` & `backend/app/agents/computer.py` |
| **6. Approved Terminal Commands** | Phase 3 | ⚪ Planned | `backend/app/tools/terminal.py` + HITL Approval Gate |
| **7. Voice (Listen & Speak)** | Phase 4 | ⚪ Planned | `backend/app/services/voice/` (`faster-whisper` + `edge-tts`) |
| **8. Multi-Agent Architecture** | Phase 6 | ⚪ Planned (v2) | `backend/app/workflows/` & `backend/app/agents/planner.py` (LangGraph) |

*Status Legend: ⚪ Planned | 🟡 Ready for Dev / In Progress | 🟢 Complete & Verified*

---

## 3. Standard Project Directory Layout

```text
jarvis/
├── backend/
│   ├── app/
│   │   ├── api/                  # REST and WebSocket endpoints
│   │   ├── agents/               # Specialist & supervisor agents
│   │   │   ├── assistant.py      # Conversational agent (v1 default)
│   │   │   ├── research.py       # Web search & document research
│   │   │   ├── computer.py       # Ubuntu desktop & terminal operator
│   │   │   └── planner.py        # Task decomposition & supervisor (v2)
│   │   ├── core/                 # Config loader, LLM abstraction, safety gates
│   │   ├── tools/                # Modular tools
│   │   │   ├── terminal.py       # Safe HITL bash execution
│   │   │   ├── filesystem.py     # Filesystem & .desktop app launcher
│   │   │   ├── web_search.py     # DuckDuckGo / Tavily integration
│   │   │   └── email.py          # Notification / email tooling
│   │   ├── memory/               # SQLite history & session state
│   │   ├── rag/                  # PDF parsing, chunking, and vector Q&A
│   │   ├── workflows/            # LangGraph multi-agent orchestration
│   │   ├── services/             # Audio/Voice pipeline & system daemons
│   │   └── main.py               # FastAPI entrypoint
│   ├── tests/                    # Unit and integration test suite
│   ├── Dockerfile                # Backend container definition
│   └── requirements.txt          # Python backend dependencies
├── frontend/                     # Web / Desktop user interface
├── infrastructure/               # Systemd units, Docker Compose, Ubuntu setup scripts
├── docs/                         # Architecture, roadmap, and guidelines
│   ├── ARCHITECTURE.md           # System design & data flow diagrams
│   ├── BACKEND_SPEC.md           # Backend module contracts & API specs
│   └── PHASES.md                 # Implementation roadmap & acceptance criteria
├── PROJECT_STATE.md              # Living state & agent handoff doc (THIS FILE)
├── README.md                     # Project overview & documentation index
├── .env.example                  # Environment configuration template
└── .gitignore                    # Git ignore rules
```

---

## 4. Architectural Decision Records (ADR)

- **ADR-001 (Agentic Workflow Documentation):** Adopt markdown-based persistent project state (`PROJECT_STATE.md`, `ARCHITECTURE.md`, `PHASES.md`) so any agent in any session can immediately pick up where previous work concluded.
- **ADR-002 (Human-in-the-Loop Terminal Safety):** Shell commands are strictly tiered. Destructive or state-altering commands (e.g. `apt`, `rm`, `systemctl`, `cp`, `mv`) require interactive terminal/API confirmation (`[y/N]`) before execution.
- **ADR-003 (Backend / Frontend Separation):** House backend logic in `backend/app/` with FastAPI service interfaces, enabling CLI, desktop, and web frontend access via unified REST/WebSocket channels.
- **ADR-004 (Modular Agents & Tools):** Tools in `backend/app/tools/` and agents in `backend/app/agents/` are decoupled from specific LLM providers.
- **ADR-005 (Evolution to Multi-Agent Workflows):** `backend/app/workflows/` will house LangGraph state charts connecting `planner.py`, `research.py`, and `computer.py` once single-agent v1 is stabilized.

---

## 5. Next Immediate Steps (Phase 1 Execution)

1. **Core Configuration & Base Models:**
   - Implement `backend/app/core/config.py` using `pydantic-settings` to load `.env`.
   - Implement `backend/app/core/llm.py` providing unified client wrapper for Ollama, OpenAI, Anthropic, and Gemini.
2. **Persistent Conversation Store:**
   - Implement `backend/app/memory/database.py` for SQLite session and message storage.
   - Implement `backend/app/memory/manager.py` for context window trimming and session switching.
3. **Conversational Assistant & CLI Runner:**
   - Complete `backend/app/agents/assistant.py`.
   - Provide CLI launcher in `backend/app/cli.py` or terminal REPL.
4. **Verification:**
   - Verify Phase 1 acceptance tests (chatting, session persistence, resumption after restart).
