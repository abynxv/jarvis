# JARVIS – 8-Week Development & Learning Roadmap

- **Project:** JARVIS: Personal Agentic AI System for Ubuntu
- **Duration:** 8 Weeks (60 Days)
- **Primary Language:** Python 3.12+
- **Platform:** Ubuntu Linux Desktop
- **Architecture:** Hybrid (Cloud AI Backend + Local Computer Agent)
- **Primary Goal:** Learn modern Agentic AI, FastAPI, LangGraph, RAG, and OS automation while building a robust, production-grade personal assistant.

---

## 📅 Roadmap Overview

```
Week 1: Foundation & LLM Integration (FastAPI + Gemini API + Chat Endpoint)
   │
Week 2: Agent Architecture & Tool Calling (Schemas, Planners, Execution Loop)
   │
Week 3: Memory Management (PostgreSQL/SQLite, Long-term & Episodic Memory)
   │
Week 4: RAG & Personal Knowledge Assistant (Qdrant/Vector, PyMuPDF, Embeddings)
   │
Week 5: Voice Assistant (Faster-Whisper STT, Edge-TTS, WebSockets)
   │
Week 6: Ubuntu Desktop Automation (Subprocess, gio, App Launcher, HITL Terminal)
   │
Week 7: Specialized Agents & Integrations (LangGraph, Multi-Agent Teams, APIs)
   │
Week 8: Testing, Security, Docker Deployment & Final Integration (JARVIS V1)
```

---

## Week 1 – Foundation & LLM Integration
**Goal:** Build a clean, modular text-based AI assistant using FastAPI and the Google Gemini API.

### 🧠 Concepts to Learn
- **FastAPI Fundamentals:** ASGI, asynchronous request handling, dependency injection (`Depends`), and middleware.
- **LLM API Integration:** Understanding Google Gemini API (`google-genai`), API authentication, model selection (`gemini-2.0-flash`, `gemini-1.5-flash`), temperature, and safety settings.
- **Prompt Engineering:** System instructions vs. developer prompts vs. user prompts.
- **Conversation State & Context Windows:** Token counts, context window limits, and message sequencing (`user` -> `model`).
- **Pydantic v2 Validation:** `BaseModel`, type annotations, input validation, and automatic schema documentation.
- **Error Handling & HTTP Statuses:** RFC 7807 compliant error responses and graceful API exception handlers.
- **Automated Testing:** Pytest and `httpx.AsyncClient` for testing asynchronous endpoints.

### 🛠️ Implementation Checklist
- [ ] 1. Configure Python environment & install dependencies (`fastapi`, `uvicorn`, `pydantic-settings`, `google-genai`, `pytest`).
- [ ] 2. Implement configuration loader (`backend/app/core/config.py`) reading `.env`.
- [ ] 3. Create Gemini LLM client wrapper (`backend/app/core/llm.py`).
- [ ] 4. Implement in-memory / SQLite conversation history store (`backend/app/memory/manager.py`).
- [ ] 5. Build `POST /api/v1/chat` endpoint matching contract:
  ```json
  POST /api/v1/chat
  {
    "conversation_id": "string",
    "message": "string"
  }
  ```
- [ ] 6. Implement structured Pydantic schemas for request and response.
- [ ] 7. Add centralized exception handlers for API key errors, quota limits, and timeouts.
- [ ] 8. Write Pytest test suite in `backend/tests/test_chat.py`.
- [ ] 9. Verify with interactive tests and curl / CLI.

**Deliverable:** A tested, responsive text-based AI assistant running locally on FastAPI.

---

## Week 2 – Agent Architecture & Tool Calling
**Goal:** Transform the conversational assistant into an AI agent capable of using tools.

### 🧠 Concepts to Learn
- What is an AI Agent? (Perception -> Planning -> Tool Execution -> Verification).
- ReAct (Reason + Act) loops and Function Calling mechanisms in LLMs.
- Defining tool schemas using JSON Schema / Pydantic.
- Safety boundaries, execution limits, and tool error handling with retries.

### 🛠️ Implementation Checklist
- [ ] 1. Build tool registry and base tool interface (`backend/app/tools/`).
- [ ] 2. Implement initial tools: `DateTime`, `Calculator`, `WebSearch` (DuckDuckGo), `Notes`.
- [ ] 3. Implement LLM tool calling dispatch loop in `backend/app/agents/assistant.py`.
- [ ] 4. Add tool execution timeout and failure recovery.
- [ ] 5. Add structured tool execution logs.

**Deliverable:** JARVIS understands requests, selects tools, runs them, and synthesizes answers.

---

## Week 3 – Memory Management
**Goal:** Give JARVIS persistent recall across conversations and sessions.

### 🧠 Concepts to Learn
- Memory Taxonomy: Short-term (buffer), Working memory, Episodic memory, Semantic memory.
- Database Schema Design: Tables for users, conversations, messages, preferences, and notes.
- Automatic preference and fact extraction from user conversations.

### 🛠️ Implementation Checklist
- [ ] 1. Set up database (PostgreSQL / SQLite).
- [ ] 2. Design tables: `users`, `conversations`, `messages`, `user_preferences`, `notes`.
- [ ] 3. Implement conversation persistence and retrieval.
- [ ] 4. Build background fact/preference extractor.
- [ ] 5. Inject relevant past context into prompt context windows.

**Deliverable:** Persistent assistant that remembers user preferences across sessions.

---

## Week 4 – RAG & Personal Knowledge Assistant
**Goal:** Enable JARVIS to ingest, index, and answer questions using personal PDF documents.

### 🧠 Concepts to Learn
- Retrieval-Augmented Generation (RAG) architecture.
- Document parsing (PyMuPDF) and recursive character chunking.
- Dense text embeddings (Hugging Face / Gemini embeddings).
- Vector databases (Qdrant) and similarity search (Cosine / Dot product).

### 🛠️ Implementation Checklist
- [ ] 1. Create document upload endpoint `POST /api/v1/documents/upload`.
- [ ] 2. Build text extraction & chunking pipeline (`backend/app/rag/`).
- [ ] 3. Set up Qdrant vector database.
- [ ] 4. Generate embeddings and store vectors with metadata.
- [ ] 5. Implement semantic search and context injection into prompts.

**Deliverable:** Personal knowledge assistant with document citations.

---

## Week 5 – Voice Assistant
**Goal:** Add natural, low-latency hands-free voice interaction.

### 🧠 Concepts to Learn
- Audio pipelines: sampling rate, PCM encoding, VAD (Voice Activity Detection).
- Speech-to-Text (STT) with `faster-whisper`.
- Text-to-Speech (TTS) with `edge-tts`.
- Full-duplex audio streaming over WebSockets.

### 🛠️ Implementation Checklist
- [ ] 1. Capture microphone input via `sounddevice` or browser audio.
- [ ] 2. Build STT transcription service (`backend/app/services/stt.py`).
- [ ] 3. Build TTS speech synthesis service (`backend/app/services/tts.py`).
- [ ] 4. Implement WebSocket endpoint `/api/v1/voice/ws`.
- [ ] 5. Test real-time spoken conversation loop.

**Deliverable:** Working voice-enabled JARVIS on Ubuntu.

---

## Week 6 – Ubuntu Desktop Automation
**Goal:** Control Ubuntu applications and run approved terminal commands safely.

### 🧠 Concepts to Learn
- Linux process management and `subprocess.run`.
- FreeDesktop standards (`.desktop` application entries and `gio launch`).
- Human-in-the-Loop (HITL) approval protocols for destructive shell actions.
- Sandboxing, timeouts, and output capture.

### 🛠️ Implementation Checklist
- [ ] 1. Build application launcher scanning `/usr/share/applications` (`backend/app/tools/filesystem.py`).
- [ ] 2. Implement approved bash runner (`backend/app/tools/terminal.py`).
- [ ] 3. Implement command risk classifier & HITL approval gate (`backend/app/core/safety.py`).
- [ ] 4. Add system resource monitoring (CPU, RAM, disk via `psutil`).

**Deliverable:** Controlled, safe system automation on Ubuntu.

---

## Week 7 – Specialized Agents & Integrations
**Goal:** Evolve into a multi-agent system using LangGraph.

### 🧠 Concepts to Learn
- Multi-Agent Orchestration: Supervisor/Router pattern vs. Peer-to-peer networks.
- LangGraph State Graphs: Nodes, Edges, State Reducers, Conditional Branching.
- External API integrations (Google Calendar, Gmail, Slack).

### 🛠️ Implementation Checklist
- [ ] 1. Define global multi-agent state schema (`backend/app/workflows/state.py`).
- [ ] 2. Implement specialized agents: Research, System/Computer, Knowledge, Planner.
- [ ] 3. Build supervisor routing graph (`backend/app/workflows/supervisor.py`).
- [ ] 4. Integrate external services with approval steps.

**Deliverable:** Multi-workflow assistant with specialized agent delegation.

---

## Week 8 – Testing, Security, Deployment & Final Integration
**Goal:** Harden, evaluate, containerize, and ship JARVIS V1.

### 🧠 Concepts to Learn
- End-to-end integration testing and LLM agent evaluation.
- Docker multi-stage builds and Docker Compose for AI applications.
- Structured logging (`structlog`), audit trails, and monitoring.

### 🛠️ Implementation Checklist
- [ ] 1. Complete unit, integration, and E2E test suites in `backend/tests/`.
- [ ] 2. Set up Docker Compose for Backend + Qdrant + DB.
- [ ] 3. Implement rate limiting and security guardrails.
- [ ] 4. Perform full end-to-end user workflow test (Voice -> Plan -> Tool -> Voice Response).
- [ ] 5. Tag and publish JARVIS V1.

**Deliverable:** JARVIS V1 – A reliable, production-ready personal AI system.
