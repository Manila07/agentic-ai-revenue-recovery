"""In-process event bus for WebSocket broadcasting."""
import asyncio
import json
from typing import List
from fastapi import WebSocket


class EventBus:
    def __init__(self):
        self.connections: List[WebSocket] = []
        self._lock = asyncio.Lock()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        async with self._lock:
            self.connections.append(ws)

    async def disconnect(self, ws: WebSocket):
        async with self._lock:
            if ws in self.connections:
                self.connections.remove(ws)

    async def broadcast(self, event_type: str, data: dict):
        message = json.dumps({"type": event_type, "data": data})
        dead = []
        async with self._lock:
            for ws in self.connections:
                try:
                    await ws.send_text(message)
                except Exception:
                    dead.append(ws)
            for ws in dead:
                self.connections.remove(ws)


event_bus = EventBus()
