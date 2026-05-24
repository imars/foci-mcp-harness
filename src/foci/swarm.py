from dataclasses import dataclass, field
from typing import List, Dict, Any
from .agent import Agent

@dataclass
class Swarm:
    id: str = field(default_factory=lambda: "swarm-" + str(__import__('time').time())[:8])
    goal_id: str = ""
    agents: List[Agent] = field(default_factory=list)
    focus: str = "general"
    status: str = "idle"

    def spawn(self, num_agents: int, role: str = "worker") -> None:
        for _ in range(num_agents):
            agent = Agent(role=role, focus=self.focus)
            self.agents.append(agent)
        self.status = "active"

    def execute_task(self, task: str) -> List[Dict[str, Any]]:
        results = []
        for agent in self.agents:
            result = agent.execute(task)
            results.append(result)
        self.status = "completed"
        return results

    def get_metrics(self) -> Dict[str, Any]:
        total_tasks = sum(a.metrics.get("tasks_completed", 0) for a in self.agents)
        avg_confidence = sum(a.metrics.get("confidence", 0.9) for a in self.agents) / max(len(self.agents), 1) if self.agents else 0
        return {
            "swarm_id": self.id,
            "goal_id": self.goal_id,
            "num_agents": len(self.agents),
            "total_tasks_completed": total_tasks,
            "avg_confidence": round(avg_confidence, 3),
            "status": self.status
        }
