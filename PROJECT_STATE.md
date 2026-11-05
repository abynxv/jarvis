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
- **Current Milestone:** **Week 1: Foundation & LLM Integration (FastAPI + Gemini API)**
- **Timeline:** 8 Weeks (November 2 – December 31, 2026)
- **Status:** Scaffolding complete; baseline contracts & docs established; ready to build Week 1 implementation.

---

## 2. 8-Week Milestone Matrix

| Week | Milestone | Status | Key Deliverable |
| :---: | :--- | :---: | :--- |
| **Week 1** | **LLM + FastAPI Foundation** | 🟡 Active | Working text-based assistant with conversation history |
| **Week 2** | **Agent & Tool Calling** | ⚪ Planned | Tool registry, ReAct loop, DateTime, Calc, WebSearch tools |
| **Week 3** | **Persistent Memory** | ⚪ Planned | Database schemas, long-term memory & user preferences |
| **Week 4** | **RAG & Knowledge Assistant** | ⚪ Planned | Qdrant vector store, PDF ingestion & semantic Q&A |
| **Week 5** | **Voice Assistant** | ⚪ Planned | Faster-Whisper (STT), Edge-TTS, WebSocket audio stream |
| **Week 6** | **Ubuntu Desktop Automation** | ⚪ Planned | App launcher (.desktop), safe HITL terminal execution |
| **Week 7** | **Specialized Agents & LangGraph** | ⚪ Planned | Multi-agent collaboration (Research, Computer, Planner) |
| **Week 8** | **Testing, Security & Deployment** | ⚪ Planned | Full test suite, Docker Compose, JARVIS V1 Release |

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
