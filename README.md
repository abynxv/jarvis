# JARVIS: Personal AI Agent for Ubuntu

JARVIS is an autonomous yet human-governed personal AI assistant tailored specifically for Ubuntu Linux. It bridges modern Large Language Models (LLMs) with local desktop automation, information retrieval, persistent memory, and voice interaction.

---

## 🧭 Repository Context for Agents & Developers

If you are an AI assistant starting a new session on this project:
1. **Read [PROJECT_STATE.md](file:///home/abynxv/Projects/jarvis/PROJECT_STATE.md)** first to inspect the current milestone, pending tasks, and recent decisions.
2. **Review [docs/ARCHITECTURE.md](file:///home/abynxv/Projects/jarvis/docs/ARCHITECTURE.md)** to understand component relationships and boundaries.
3. **Follow [docs/PHASES.md](file:///home/abynxv/Projects/jarvis/docs/PHASES.md)** for phase deliverables and verification checklists.

---

## 🎯 JARVIS v1 Core Capabilities

1. **Natural LLM Chat:** Context-aware conversations with support for modular LLM backends (Ollama local models, Anthropic Claude, OpenAI, Google Gemini).
2. **Persistent Conversation Memory:** Short-term conversational context + SQLite/Vector-based long-term recall across sessions.
3. **Live Web Search:** Real-time internet queries without API-key friction (DuckDuckGo / SearXNG / Tavily).
4. **Local PDF Ingestion & Summarization:** Fast document extraction, chunking, and contextual Q&A/summarization.
5. **Ubuntu Application Launcher:** Seamlessly launch desktop applications, manage windows, and query installed `.desktop` apps via native Linux utilities.
6. **Safe Approved Terminal Execution:** Execute shell commands with strict Human-in-the-Loop (HITL) approval, command categorization, and risk scoring.
7. **Voice Interaction (Listen & Speak):** Local/offline or low-latency speech-to-text (Whisper/faster-whisper) and natural text-to-speech (Piper/Edge-TTS).

> **Future Evolution (v2+):** Transition to multi-agent architecture (Supervisor, Researcher, System Operator, Voice Assistant) once v1 is robust and reliable.

---

## 📂 Documentation Index

| Document | Purpose |
| :--- | :--- |
| **[PROJECT_STATE.md](file:///home/abynxv/Projects/jarvis/PROJECT_STATE.md)** | **Source of Truth** for agent state, current task, tech stack, and changelog |
| **[docs/ARCHITECTURE.md](file:///home/abynxv/Projects/jarvis/docs/ARCHITECTURE.md)** | Technical design, data flow diagrams, safety architecture, and voice stack |
| **[docs/PHASES.md](file:///home/abynxv/Projects/jarvis/docs/PHASES.md)** | Step-by-step phased roadmap, acceptance tests, and milestone definitions |

---

## 🛠️ Tech Stack Baseline

- **Language:** Python 3.11+
- **Agent Framework / Orchestration:** Clean Modular Python (LangChain/LangGraph or light native tool loop with LangGraph for multi-agent transition)
- **Local Storage / Memory:** SQLite + ChromaDB / sqlite-vec
- **OS Controls:** Ubuntu Linux (`gio`, `xdg-open`, `systemd`, `subprocess`, `/usr/share/applications`)
- **Speech Processing:** `faster-whisper` (STT) + `piper-tts` / `edge-tts` (TTS) + `sounddevice`
- **Document Processing:** `pypdf` / `pymupdf` (fitz)
