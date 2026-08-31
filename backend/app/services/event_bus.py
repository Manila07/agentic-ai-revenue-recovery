# backend/app/services/event_bus.py
from typing import List, Dict, Any
from fastapi import WebSocket
import asyncio
import json
import logging

logger = logging.getLogger(__name__)

class EventBus:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
        logger.info(f"WebSocket connected. Total: {len(self.connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.connections:
            self.connections.remove(websocket)
            logger.info(f"WebSocket disconnected. Total: {len(self.connections)}")

    async def broadcast(self, event: Dict[str, Any]):
        """Send event to all connected clients."""
        message = json.dumps(event, default=str)
        for websocket in self.connections[:]:  # iterate over copy
            try:
                await websocket.send_text(message)
            except Exception:
                # Remove broken connection
                await self.disconnect(websocket)

# Singleton instance
event_bus = EventBus()