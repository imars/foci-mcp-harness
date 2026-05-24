from typing import Dict, Any, List
from .goal import Goal
from .swarm import Swarm

class Loki:
    """Loki orchestrator for focused agent swarms around versioned goals."""

    def __init__(self):
        self.goals: Dict[str, Goal] = {}
        self.swarms: Dict[str, Swarm] = {}

    def create_goal(self, description: str, success_criteria: List[str], version: str = "v1.0") -> Goal:
        goal = Goal(description=description, success_criteria=success_criteria, version=version)
        self.goals[goal.id] = goal
        return goal

    def spawn_swarm(self, goal_id: str, num_agents: int = 3, focus: str = "task") -> Swarm:
        if goal_id not in self.goals:
            raise ValueError(f"Goal {goal_id} not found")
        swarm = Swarm(goal_id=goal_id, focus=focus)
        swarm.spawn(num_agents)
        self.swarms[swarm.id] = swarm
        return swarm

    def measure_progress(self, goal_id: str) -> Dict[str, Any]:
        if goal_id not in self.goals:
            raise ValueError(f"Goal {goal_id} not found")
        goal = self.goals[goal_id]
        swarm_metrics = None
        if goal_id in self.swarms:
            swarm = self.swarms[goal_id]
            swarm_metrics = swarm.get_metrics()
            goal.update_progress(0.25, "Swarm progress update")
        return {
            "goal": goal.to_dict(),
            "swarm_metrics": swarm_metrics
        }

    def simulate_git_pr(self, goal_id: str, branch: str) -> Dict[str, Any]:
        goal = self.goals.get(goal_id)
        if not goal:
            return {"error": "Goal not found"}
        # Simulate Git collaboration
        pr = {
            "pr_id": f"pr-{goal_id[-4:]}",
            "branch": branch,
            "goal_version": goal.version,
            "status": "open",
            "reviewers": ["grok", "loki"],
            "message": f"Achieved goal {goal.description} at {goal.version}"
        }
        goal.update_progress(0.5, f"PR created for {branch}")
        return pr
