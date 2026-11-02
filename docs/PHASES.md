# JARVIS Implementation Phases & Milestones

This document is the execution blueprint for building **JARVIS v1: A Personal AI Agent for Ubuntu**, followed by its multi-agent evolution. Each phase has concrete objectives, deliverables in `backend/app/`, and acceptance criteria.

---

## Roadmap Overview

```
Phase 1: Core Foundation, LLM Engine & Memory ──▶ [Deliverable: Conversational Assistant with Memory]
  │
Phase 2: Information Retrieval (Search & PDF)  ──▶ [Deliverable: Research Agent, Web Search & RAG]
  │
Phase 3: Ubuntu OS & Safe Terminal Control     ──▶ [Deliverable: Computer Agent, App Launcher & HITL]
  │
Phase 4: Multimodal Voice Pipeline (STT/TTS)   ──▶ [Deliverable: Voice Services & Hands-free Loop]
  │
Phase 5: JARVIS v1 Hardening & Validation      ──▶ [Deliverable: Reliable, Tested Backend & CLI]
  │
Phase 6: Multi-Agent Architecture (LangGraph)  ──▶ [Deliverable: Workflows & Planner Agent]
```

---

## Phase 1: Core Foundation, LLM Engine & Memory

### Objectives
- Establish configuration management and LLM provider abstraction in `backend/app/core/`.
- Build persistent SQLite storage in `backend/app/memory/`.
- Implement conversational persona in `backend/app/agents/assistant.py`.
- Provide interactive terminal runner / FastAPI server in `backend/app/main.py`.

### Key Deliverables
- `backend/app/core/config.py`: Environment variable loading via `pydantic-settings`.
- `backend/app/core/llm.py`: Unified LLM client (Ollama, OpenAI, Anthropic, Gemini).
- `backend/app/memory/database.py`: SQLite schema and manager for sessions and messages.
- `backend/app/memory/manager.py`: Context window management and message history trimmer.
- `backend/app/agents/assistant.py`: Primary conversational assistant logic.
- `backend/app/main.py`: FastAPI server + interactive CLI mode.

### Acceptance Criteria
- [ ] User can send prompts and receive natural LLM responses.
- [ ] Conversation persists to SQLite; restarting session retrieves previous chat history.
- [ ] LLM provider can be switched seamlessly via `.env`.

---

## Phase 2: Information Retrieval (Web Search & Local PDF RAG)

### Objectives
- Implement real-time internet search tool in `backend/app/tools/web_search.py`.
- Build PDF extraction and chunking pipeline in `backend/app/rag/`.
- Equip `backend/app/agents/research.py` with dynamic tool dispatch.

### Key Deliverables
- `backend/app/tools/web_search.py`: DuckDuckGo / Tavily search integration.
- `backend/app/rag/extractor.py`: PDF parser (PyMuPDF / pypdf) and chunker.
- `backend/app/rag/summarizer.py`: Map-reduce / targeted summarization.
- `backend/app/agents/research.py`: Agent coordinating searches and document ingestion.

### Acceptance Criteria
- [ ] Prompt: *"What is the latest news about Ubuntu 24.04?"* triggers search tool and cites sources.
- [ ] Prompt: *"Summarize /path/to/paper.pdf"* outputs concise structured summaries.
- [ ] Tool execution errors return clean error messages back to LLM.

---

## Phase 3: Ubuntu Desktop & Safe System Automation

### Objectives
- Implement Ubuntu application launcher in `backend/app/tools/filesystem.py`.
- Implement safe terminal execution with Human-in-the-Loop (HITL) approval in `backend/app/tools/terminal.py` and `backend/app/core/safety.py`.
- Connect actions to `backend/app/agents/computer.py`.

### Key Deliverables
- `backend/app/tools/filesystem.py`: Scans `.desktop` files and launches apps via `gio launch`.
- `backend/app/tools/terminal.py`: Subprocess runner with timeout and output capture.
- `backend/app/core/safety.py`: Risk classifier and interactive approval gate.
- `backend/app/agents/computer.py`: OS operator agent.

### Acceptance Criteria
- [ ] Prompt: *"Open Google Chrome"* fuzzy-matches `.desktop` entry and launches the app.
- [ ] Prompt: *"Check disk usage"* runs `df -h` and reports free space.
- [ ] Modifying command (e.g. `sudo apt update`, `rm`, `git`) triggers approval prompt: `[Approve command? (y/n)]`.
- [ ] Rejected commands abort without executing.

---

## Phase 4: Multimodal Voice Interface (Listen & Speak)

### Objectives
- Build low-latency speech-to-text (STT) and text-to-speech (TTS) services in `backend/app/services/voice/`.
- Support push-to-talk and voice-driven assistant loop.

### Key Deliverables
- `backend/app/services/voice/stt.py`: Local transcription via `faster-whisper`.
- `backend/app/services/voice/tts.py`: Speech synthesis via `edge-tts` / `piper`.
- `backend/app/services/voice/audio_io.py`: Microphone capture and speaker playback.
- `backend/app/api/voice.py`: WebSocket audio streaming endpoint.

### Acceptance Criteria
- [ ] Spoken microphone input is transcribed into text accurately.
- [ ] Spoken audio plays back smoothly while text streams to output.

---

## Phase 5: JARVIS v1 Hardening & Validation

### Objectives
- Run end-to-end integration tests across all capabilities.
- Write test suite in `backend/tests/`.
- Validate performance on Ubuntu 24.04 LTS.

### Key Deliverables
- `backend/tests/test_agents.py`, `backend/tests/test_tools.py`, `backend/tests/test_memory.py`.
- Full health check and self-diagnostic script.

### Acceptance Criteria
- [ ] 100% passing tests for tool schemas, memory, and security gates.
- [ ] Stable backend API and terminal CLI.

---

## Phase 6: Multi-Agent Architecture Transition

### Objectives
- Implement multi-agent collaboration graph in `backend/app/workflows/` using **LangGraph**.
- Enable `backend/app/agents/planner.py` to supervise `research.py`, `computer.py`, and `assistant.py`.

### Key Deliverables
- `backend/app/workflows/supervisor_graph.py`: LangGraph state chart coordinating sub-tasks.
- `backend/app/agents/planner.py`: Multi-step task planner.

### Acceptance Criteria
- [ ] Complex multi-step queries are decomposed and executed across specialist agents autonomously.
