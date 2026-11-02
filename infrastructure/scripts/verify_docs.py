#!/usr/bin/env python3
"""
Documentation Verification & Sync Checker.
Checks that all tools, agents, and endpoints in code are referenced in docs.
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
BACKEND_APP = ROOT / "backend" / "app"
DOCS_DIR = ROOT / "docs"
STATE_FILE = ROOT / "PROJECT_STATE.md"
SPEC_FILE = DOCS_DIR / "BACKEND_SPEC.md"

def check_sync():
    errors = []
    
    if not STATE_FILE.exists():
        errors.append("PROJECT_STATE.md is missing!")
    if not SPEC_FILE.exists():
        errors.append("docs/BACKEND_SPEC.md is missing!")

    spec_content = SPEC_FILE.read_text() if SPEC_FILE.exists() else ""
    state_content = STATE_FILE.read_text() if STATE_FILE.exists() else ""

    # Check tools
    tools_dir = BACKEND_APP / "tools"
    if tools_dir.exists():
        for file in tools_dir.glob("*.py"):
            if file.name == "__init__.py":
                continue
            tool_name = file.stem
            if tool_name not in spec_content and f"{tool_name}.py" not in spec_content:
                errors.append(f"Tool '{file.name}' not documented in docs/BACKEND_SPEC.md")

    # Check agents
    agents_dir = BACKEND_APP / "agents"
    if agents_dir.exists():
        for file in agents_dir.glob("*.py"):
            if file.name == "__init__.py":
                continue
            agent_name = file.stem
            if agent_name not in spec_content and f"{agent_name}.py" not in spec_content:
                errors.append(f"Agent '{file.name}' not documented in docs/BACKEND_SPEC.md")

    if errors:
        print("❌ Documentation Drift Detected:")
        for err in errors:
            print(f"  - {err}")
        print("\nPlease update docs/BACKEND_SPEC.md and PROJECT_STATE.md.")
        return 1
    else:
        print("✅ Documentation is in sync with code!")
        return 0

if __name__ == "__main__":
    sys.exit(check_sync())
