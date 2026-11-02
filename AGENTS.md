# Agent Guidelines & Operating Rules for JARVIS

This file is automatically loaded by AI coding assistants (Antigravity, Claude Code, Cursor, Copilot) when operating in this repository. Follow these mandatory operating procedures.

---

## 1. Golden Rule: Read State First, Update State Last

Whenever you start a task in this repository:
1. **First Action:** Read [`PROJECT_STATE.md`](file:///home/abynxv/Projects/jarvis/PROJECT_STATE.md) to inspect the current active phase, completed tasks, and architectural decisions.
2. **Middle Action:** Execute your coding, testing, or debugging task following [`docs/ARCHITECTURE.md`](file:///home/abynxv/Projects/jarvis/docs/ARCHITECTURE.md) and [`docs/BACKEND_SPEC.md`](file:///home/abynxv/Projects/jarvis/docs/BACKEND_SPEC.md).
3. **Final Action (Definition of Done):** Before reporting completion to the user, you **MUST** update the documentation files to reflect your changes:
   - **[`PROJECT_STATE.md`](file:///home/abynxv/Projects/jarvis/PROJECT_STATE.md):** Update current milestone, capability status table, and add an entry to the Changelog/Decisions log.
   - **[`docs/PHASES.md`](file:///home/abynxv/Projects/jarvis/docs/PHASES.md):** Check off completed acceptance criteria `[x]`.
   - **[`docs/BACKEND_SPEC.md`](file:///home/abynxv/Projects/jarvis/docs/BACKEND_SPEC.md):** Update if you added/modified an API route, tool signature, or agent interface.

---

## 2. When to Update Which Document

| Event in Code | Required Documentation Update |
| :--- | :--- |
| **Added a new Tool or Agent** | Update `docs/BACKEND_SPEC.md` (interface/params) and `PROJECT_STATE.md` (capability matrix). |
| **Added or changed an API Route** | Update `docs/BACKEND_SPEC.md` (endpoint path, request/response schema). |
| **Completed a phase milestone** | Check off items in `docs/PHASES.md` and bump active milestone in `PROJECT_STATE.md`. |
| **Changed tech stack / config / env** | Update `.env.example`, `PROJECT_STATE.md`, and `README.md`. |
| **Made a major architectural decision** | Record an ADR in `PROJECT_STATE.md` section 4. |

---

## 3. Human-in-the-Loop (HITL) Safety Rule

Under NO circumstances may an agent remove or bypass the interactive approval mechanism for shell execution in `backend/app/tools/terminal.py` and `backend/app/core/safety.py`. All state-modifying bash commands must require user confirmation.

---

## 4. Verification Before Finishing

Before completing any task:
1. Run relevant automated tests: `pytest backend/tests/`.
2. Ensure documentation reflects reality: no ghost endpoints, no undocumented tools.
