"""
Computer / OS Agent.
Handles Ubuntu desktop interaction, application launching, filesystem operations,
and safe Human-in-the-Loop (HITL) terminal execution.
"""
from typing import Any, Dict, Optional

class ComputerAgent:
    """Specialist agent for Ubuntu Linux system automation."""

    def __init__(self, require_approval: bool = True):
        self.require_approval = require_approval

    async def execute_task(self, command_or_action: str) -> Dict[str, Any]:
        """Execute approved OS action (launch app, terminal command, check system)."""
        raise NotImplementedError("ComputerAgent.execute_task will be implemented in Phase 3.")
