# JARVIS Backend & API Specification

This document defines the internal module contracts, external API integrations, and REST/WebSocket endpoints for the JARVIS backend. Any AI agent or developer implementing or modifying backend code must adhere to these specifications.

---

## 1. Internal Module Architecture & Interfaces

The backend is organized into decoupled layers:

```
[API Layer (api/)] ──▶ [Agents Layer (agents/)] ──▶ [Workflows (workflows/)]
                              │
               ┌──────────────┼──────────────┐
               ▼              ▼              ▼
       [Core Engine]    [Tools Layer]   [Memory & RAG]
       (core/llm.py)    (tools/)        (memory/ & rag/)
```

### 1.1 Agent Registry & Interface (`backend/app/agents/`)

All agents implement the unified agent interface and are registered as follows:

| Agent File | Class | Primary Role | Phase |
| :--- | :--- | :--- | :---: |
| **`assistant.py`** | `AssistantAgent` | Conversational persona, intent routing, user dialogue | Phase 1 |
| **`research.py`** | `ResearchAgent` | Web search, PDF extraction, multi-source synthesis | Phase 2 |
| **`computer.py`** | `ComputerAgent` | Ubuntu app launcher, bash terminal runner | Phase 3 |
| **`planner.py`** | `PlannerAgent` | Goal decomposition, multi-agent supervisor | Phase 6 |

```python
from typing import AsyncGenerator, Dict, Any, List, Optional
from pydantic import BaseModel

class AgentResponse(BaseModel):
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    citations: Optional[List[str]] = None
    requires_approval: bool = False
    pending_command: Optional[str] = None

class BaseAgent:
    async def process(self, prompt: str, session_id: str, **kwargs) -> AgentResponse:
        """Process user message and return structured response."""
        ...

    async def process_stream(self, prompt: str, session_id: str, **kwargs) -> AsyncGenerator[str, None]:
        """Stream token-by-token response."""
        ...
```

### 1.2 Tool Registry & Interface (`backend/app/tools/`)

All tools expose self-describing JSON schemas for LLM function calling:

| Tool File | Class | Description | Phase |
| :--- | :--- | :--- | :---: |
| **`terminal.py`** | `TerminalTool` | Safe bash execution with HITL approval gate | Phase 3 |
| **`filesystem.py`** | `FilesystemTool` | Ubuntu .desktop launcher (`gio`) & file operations | Phase 3 |
| **`web_search.py`** | `WebSearchTool` | Real-time web queries via DuckDuckGo / Tavily | Phase 2 |
| **`email.py`** | `EmailTool` | Email drafting and dispatch | Future |

```python
from typing import Dict, Any
from pydantic import BaseModel

class ToolResult(BaseModel):
    success: bool
    data: Any
    error: Optional[str] = None
    requires_approval: bool = False

class BaseTool:
    name: str
    description: str
    parameters: Dict[str, Any]  # JSON Schema format

    async def execute(self, **kwargs) -> ToolResult:
        ...
```

### 1.3 Memory Interface (`backend/app/memory/`)
Manages short-term context windows and SQLite persistence:
- **`save_message(session_id, role, content, tool_calls)`**
- **`get_history(session_id, limit=20)`**
- **`create_session(title)`**
- **`list_sessions()`**

---

## 2. External Service Integrations

| Service / Provider | Purpose | Default Protocol / Library | Fallback / Alternatives |
| :--- | :--- | :--- | :--- |
| **Ollama** | Local offline LLM reasoning | HTTP `http://localhost:11434` (`ollama` client) | OpenAI / Anthropic / Gemini |
| **OpenAI / Claude / Gemini** | Cloud LLM fallback | Official SDKs / HTTP async clients | Local Ollama |
| **DuckDuckGo** | Live web search | `duckduckgo-search` Python package | Tavily API |
| **faster-whisper** | Speech-to-Text (STT) | Local CTranslate2 model | OpenAI Whisper API |
| **edge-tts / piper** | Text-to-Speech (TTS) | Local websocket / Python bindings | System `espeak-ng` |
| **Ubuntu Desktop (gio)** | Launching apps | `subprocess.run(["gio", "launch", app_id])` | `gtk-launch` / `xdg-open` |

---

## 3. REST & WebSocket API Contracts

Base URL: `http://localhost:8000/api/v1`

### 3.1 Health & Diagnostics
- **`GET /health`**
  - **Response:**
    ```json
    {
      "status": "healthy",
      "version": "1.0.0",
      "llm_provider": "ollama",
      "llm_model": "llama3.2",
      "voice_enabled": false
    }
    ```

### 3.2 Sessions & History
- **`GET /api/v1/sessions`**
  - Returns list of conversation sessions.
- **`POST /api/v1/sessions`**
  - Request: `{"title": "Research Ubuntu kernel"}`
  - Response: `{"session_id": "uuid-v4", "created_at": "..."}`
- **`GET /api/v1/sessions/{session_id}/messages`**
  - Returns chronological message history for the session.

### 3.3 Chat & Reasoning (REST & Streaming)
- **`POST /api/v1/chat`**
  - **Request Payload:**
    ```json
    {
      "session_id": "uuid-v4",
      "message": "Open Firefox and search for Ubuntu 24.04 release notes",
      "stream": false
    }
    ```
  - **Response Payload:**
    ```json
    {
      "message_id": "msg-001",
      "role": "assistant",
      "content": "Opening Firefox and searching for the release notes.",
      "tool_calls": [
        {
          "tool": "filesystem",
          "action": "launch_application",
          "args": {"app_name": "firefox"}
        }
      ],
      "requires_approval": false
    }
    ```
- **`POST /api/v1/chat/stream`**
  - Server-Sent Events (SSE) streaming tokens as they are generated by the LLM.

### 3.4 Human-in-the-Loop (HITL) Command Approval
When a modifying terminal command or sensitive action is proposed by an agent:
- **`POST /api/v1/approvals/{approval_id}`**
  - **Request Payload:**
    ```json
    {
      "approval_id": "appr-12345",
      "approved": true,
      "modified_command": null
    }
    ```
  - **Response Payload:**
    ```json
    {
      "status": "executed",
      "output": "Command output logs...",
      "exit_code": 0
    }
    ```

### 3.5 Real-Time Voice Streaming (WebSocket)
- **`WS /api/v1/voice/ws`**
  - **Client sends:** Binary PCM audio chunks from microphone.
  - **Server receives:** Transcribes via `faster-whisper` -> Passes to Agent -> Synthesizes via `edge-tts`.
  - **Server sends:** Audio byte stream + JSON transcription events.

---

## 4. Error Handling Standards

All API errors return RFC 7807 compliant JSON:

```json
{
  "error": {
    "code": "TOOL_EXECUTION_ERROR",
    "message": "Failed to launch application 'unknown_app'",
    "details": "No matching .desktop file found in /usr/share/applications",
    "retryable": false
  }
}
```
