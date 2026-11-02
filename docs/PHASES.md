# JARVIS Implementation Phases & Milestones

This document is the execution blueprint for building **JARVIS v1: A Personal AI Agent for Ubuntu**, followed by its multi-agent evolution. Each phase has concrete objectives, deliverables, and acceptance criteria.

---

## Roadmap Overview

```
Phase 1: Core Foundation, LLM Engine & Memory ──▶ [Deliverable: Conversational CLI with Memory]
  │
Phase 2: Information Retrieval (Search & PDF)  ──▶ [Deliverable: Web Search & PDF Summarizer]
  │
Phase 3: Ubuntu OS & Safe Terminal Control     ──▶ [Deliverable: App Launcher & HITL Terminal]
  │
Phase 4: Multimodal Voice Pipeline (STT/TTS)   ──▶ [Deliverable: Hands-free Voice Interaction]
  │
Phase 5: JARVIS v1 Hardening & Validation      ──▶ [Deliverable: Reliable, Tested v1 Assistant]
  │
Phase 6: Multi-Agent Architecture (LangGraph)  ──▶ [Deliverable: Distributed Specialized Agents]
```

---

## Phase 1: Core Foundation, LLM Engine & Memory

### Objectives
- Establish a clean, modular Python project structure with environment configuration.
- Implement an LLM provider abstraction supporting local (Ollama) and cloud APIs (OpenAI, Anthropic, Gemini).
- Build a persistent conversation store in SQLite (short-term history and cross-session persistence).
- Provide an interactive terminal CLI interface.

### Key Deliverables
- `jarvis/core/config.py`: Environment variable loading, configuration management.
- `jarvis/core/llm.py`: Pluggable LLM interface with unified streaming and tool-calling support.
- `jarvis/memory/database.py`: SQLite schema and manager for sessions, messages, and metadata.
- `jarvis/memory/manager.py`: Context window management, message trimming, and conversation retrieval.
- `jarvis/cli/main.py`: Interactive CLI with formatted markdown output.

### Acceptance Criteria
- [ ] User can initiate a chat session, type messages, and receive natural LLM responses.
- [ ] User can close the terminal, reopen JARVIS, and resume previous conversations by session ID.
- [ ] LLM provider can be switched via `.env` without modifying business logic.

---

## Phase 2: Information Retrieval (Web Search & Local PDF Ingestion)

### Objectives
- Enable JARVIS to query the live internet for up-to-date facts.
- Enable JARVIS to inspect, read, and summarize local PDF files on Ubuntu.
- Equip the LLM engine with dynamic function/tool calling.

### Key Deliverables
- `jarvis/tools/base.py`: Base tool definition interface with schema generator.
- `jarvis/tools/web_search.py`: DuckDuckGo / Tavily search integration with snippet and link parsing.
- `jarvis/tools/pdf_reader.py`: PDF text extraction (PyMuPDF / pypdf), document chunking, and summarizer.
- `jarvis/core/agent.py`: Agent loop that detects tool calls, dispatches execution, and returns responses.

### Acceptance Criteria
- [ ] Prompt: *"What is the latest news about Ubuntu 24.04 LTS?"* triggers web search tool and cites sources.
- [ ] Prompt: *"Summarize the file /path/to/sample.pdf"* parses text and delivers a structured summary.
- [ ] Tool execution errors are handled gracefully without crashing the chat session.

---

## Phase 3: Ubuntu Desktop & Safe System Automation

### Objectives
- Enable JARVIS to inspect and launch installed desktop applications on Ubuntu.
- Provide terminal command execution with strict Human-in-the-Loop (HITL) approval to guarantee safety.

### Key Deliverables
- `jarvis/tools/app_manager.py`:
  - Scans `/usr/share/applications` and `~/.local/share/applications` for `.desktop` files.
  - Matches requested application names using fuzzy matching.
  - Launches apps cleanly using `gio launch` or `gtk-launch`.
- `jarvis/tools/terminal_runner.py`:
  - Executes shell commands via `subprocess` with timeout and stdout/stderr capture.
  - Command risk classifier (Safe read-only vs. Modifying state vs. Critical).
- `jarvis/core/safety.py`:
  - HITL confirmation prompt displaying command, target path, and risk level.
  - User can press `[Y]es` / `[N]o` / `[E]dit` before any non-read-only command runs.

### Acceptance Criteria
- [ ] Prompt: *"Open Google Chrome"* or *"Launch text editor"* successfully opens the Ubuntu application.
- [ ] Prompt: *"Check my disk usage"* executes `df -h` and reports free disk space.
- [ ] Prompt: *"Install htop"* pauses and prompts the user for approval: `[Approve command 'sudo apt install htop'? (y/n)]`.
- [ ] Rejected commands abort safely with explanatory message back to LLM.

---

## Phase 4: Multimodal Voice Interface (Listen & Speak)

### Objectives
- Add real-time speech input (STT) and spoken responses (TTS) on Ubuntu.
- Support both Push-to-Talk (terminal keypress) and Voice Activity Detection (VAD).

### Key Deliverables
- `jarvis/voice/stt.py`: Speech-to-Text using `faster-whisper` (local offline) with audio device selection.
- `jarvis/voice/tts.py`: Text-to-Speech using `piper-tts` or `edge-tts` for high-fidelity spoken output.
- `jarvis/voice/audio_io.py`: Microphone stream capture, VAD (webrtcvad / silero-vad), and speaker playback.
- `jarvis/cli/voice_mode.py`: Voice-interactive CLI loop enabling hands-free or push-to-talk conversation.

### Acceptance Criteria
- [ ] Speaking into the microphone transcribes audio accurately into text.
- [ ] JARVIS answers with synthesized audio playback while simultaneously printing text to console.
- [ ] Voice mode supports interrupt/cancel controls.

---

## Phase 5: Reliability Testing & Hardening of JARVIS v1

### Objectives
- Validate end-to-end integration of all 7 core v1 capabilities.
- Write unit and integration test suites.
- Optimize response latency and memory footprints.

### Key Deliverables
- `tests/test_llm.py`, `tests/test_memory.py`, `tests/test_tools.py`, `tests/test_safety.py`.
- Automated regression suite checking tool schema generation and command approval logic.
- Comprehensive user setup guide for Ubuntu dependencies (PulseAudio/PipeWire, libportaudio, system packages).

### Acceptance Criteria
- [ ] Full end-to-end run passing all capability tests on Ubuntu.
- [ ] Zero crash states on invalid tool inputs or network timeouts.
- [ ] v1 marked complete and tagged.

---

## Phase 6: Multi-Agent Architecture Transition

### Objectives
- Refactor the single-agent tool loop into a distributed multi-agent graph using **LangGraph**.
- Separate concerns into specialized agents:
  - **Supervisor Agent:** Planning, task breakdown, delegation.
  - **OS & Terminal Agent:** System monitoring, application launching, shell commands.
  - **Research & Document Agent:** Web search, PDF parsing, information synthesis.
  - **Voice & Persona Agent:** Natural speech rhythm, tone, and dialogue management.

### Key Deliverables
- `jarvis/agents/supervisor.py`: State graph router and task planner.
- `jarvis/agents/system_agent.py`: Specialist for Ubuntu environment operations.
- `jarvis/agents/research_agent.py`: Specialist for deep web and document research.
- `jarvis/agents/state.py`: Global multi-agent state dictionary.

### Acceptance Criteria
- [ ] Multi-step prompts (e.g., *"Search for the latest Linux kernel update, summarize the changelog PDF, and write a summary file to my desktop"*) are decomposed and distributed across specialist agents.
- [ ] Robust error recovery if one specialist fails.
