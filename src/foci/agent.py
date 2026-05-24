from dataclasses import dataclass, field
from typing import List, Dict, Any
from uuid import uuid4

@dataclass
class Agent:
    id: str = field(default_factory=lambda: str(uuid4())[:8])
    role: str = "general"
    focus: str = "task"
    status: str = "idle"
    metrics: Dict[str, float] = field(default_factory=dict)

    def execute(self, task: str) -> Dict[str, Any]:
        self.status = "working"
        # Simulate focused work
        result = {
            "agent_id": self.id,
            "task": task,
            "outcome": f"Completed {task} with high focus",
            "confidence": 0.92
        }
        self.status = "completed"
        self.metrics["tasks_completed"] = self.metrics.get("tasks_completed", 0) + 1
        return result

    def report(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "focus": self.focus,
            "status": self.status,
            "metrics": self.metrics
        }
