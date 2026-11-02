# JARVIS: Personal AI Agent for Ubuntu

JARVIS is an autonomous yet human-governed personal AI assistant built natively for Ubuntu Linux. It combines modern Large Language Models (LLMs) with local desktop automation, real-time information retrieval, persistent memory, and multimodal voice interaction.

---

## 🧭 Repository Context for Agents & Developers

If you are an AI assistant starting a new session on this project:
1. **Read [PROJECT_STATE.md](file:///home/abynxv/Projects/jarvis/PROJECT_STATE.md)** first to inspect the current milestone, pending tasks, and recent decisions.
2. **Review [docs/ARCHITECTURE.md](file:///home/abynxv/Projects/jarvis/docs/ARCHITECTURE.md)** to understand component relationships and boundaries.
3. **Follow [docs/PHASES.md](file:///home/abynxv/Projects/jarvis/docs/PHASES.md)** for phase deliverables and verification checklists.

---

## 🏗️ Project Architecture & Directory Structure

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
│   └── PHASES.md                 # Implementation roadmap & acceptance criteria
├── PROJECT_STATE.md              # Living state & agent handoff doc
├── README.md                     # Project overview & documentation index
├── .env.example                  # Environment configuration template
└── .gitignore                    # Git ignore rules
```

---

## 🎯 JARVIS v1 Core Capabilities

1. **Natural LLM Chat:** Context-aware conversations with support for modular LLM backends (Ollama, Claude, OpenAI, Gemini).
2. **Persistent Conversation Memory:** Short-term conversational context + SQLite persistent history across sessions.
3. **Live Web Search:** Real-time internet queries without API-key friction (DuckDuckGo / Tavily).
4. **Local PDF Ingestion & Summarization:** Fast document extraction, chunking, and contextual Q&A/summarization.
5. **Ubuntu Application Launcher:** Seamlessly launch desktop applications via native Linux `.desktop` and `gio` utilities.
6. **Safe Approved Terminal Execution:** Execute shell commands with strict Human-in-the-Loop (HITL) approval.
7. **Voice Interaction (Listen & Speak):** Speech-to-text (`faster-whisper`) and natural text-to-speech (`edge-tts`).
8. **Multi-Agent Architecture (v2):** Coordinated team of specialized agents (`planner`, `research`, `computer`, `assistant`) orchestrated with LangGraph.

---

## 📂 Documentation Index

| Document | Purpose |
| :--- | :--- |
| **[PROJECT_STATE.md](file:///home/abynxv/Projects/jarvis/PROJECT_STATE.md)** | **Source of Truth** for agent state, current task, tech stack, and changelog |
| **[docs/ARCHITECTURE.md](file:///home/abynxv/Projects/jarvis/docs/ARCHITECTURE.md)** | Technical design, data flow diagrams, safety architecture, and voice stack |
| **[docs/BACKEND_SPEC.md](file:///home/abynxv/Projects/jarvis/docs/BACKEND_SPEC.md)** | Backend internal module contracts, external integrations, and REST/WebSocket API endpoints |
| **[docs/PHASES.md](file:///home/abynxv/Projects/jarvis/docs/PHASES.md)** | Step-by-step phased roadmap, acceptance tests, and milestone definitions |
