from typing import Dict, Any, List
from datetime import datetime

class ConversationMemory:
    def __init__(self):
        self.memory: Dict[str, List[Dict[str, Any]]] = {}

    def add(self, payment_id: str, event: Dict[str, Any]):
        if payment_id not in self.memory:
            self.memory[payment_id] = []
        self.memory[payment_id].append({**event, "timestamp": datetime.now().isoformat()})

    def get(self, payment_id: str) -> List[Dict[str, Any]]:
        return self.memory.get(payment_id, [])

    def clear(self, payment_id: str):
        if payment_id in self.memory:
            del self.memory[payment_id]

    def get_all(self) -> Dict[str, List[Dict[str, Any]]]:
        return self.memory