from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class Goal:
    id: str = field(default_factory=lambda: "goal-" + str(datetime.now().timestamp())[:10].replace(".", ""))
    description: str = ""
    success_criteria: List[str] = field(default_factory=list)
    version: str = "v1.0"
    status: str = "active"
    created_at: datetime = field(default_factory=datetime.now)
    progress: float = 0.0
    history: List[Dict] = field(default_factory=list)

    def update_progress(self, delta: float, note: str = "") -> None:
        self.progress = min(1.0, max(0.0, self.progress + delta))
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "delta": delta,
            "note": note,
            "new_progress": self.progress
        })
        if self.progress >= 1.0:
            self.status = "completed"

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "description": self.description,
            "success_criteria": self.success_criteria,
            "version": self.version,
            "status": self.status,
            "progress": self.progress,
            "created_at": self.created_at.isoformat(),
            "history_length": len(self.history)
        }
