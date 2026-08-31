from typing import Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class AgentState:
    payment_id: str
    current_step: str = "INIT"
    decisions: List[Dict[str, Any]] = field(default_factory=list)
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed: bool = False

    def record_decision(self, decision: Dict[str, Any]):
        self.decisions.append({**decision, "timestamp": datetime.now().isoformat()})

    def record_tool_call(self, tool_name: str, args: Dict[str, Any], result: Dict[str, Any]):
        self.tool_calls.append({
            "tool_name": tool_name,
            "args": args,
            "result": result,
            "timestamp": datetime.now().isoformat(),
        })

    def to_dict(self) -> Dict[str, Any]:
        return {
            "payment_id": self.payment_id,
            "current_step": self.current_step,
            "decisions": self.decisions,
            "tool_calls": self.tool_calls,
            "started_at": self.started_at,
            "completed": self.completed,
        }