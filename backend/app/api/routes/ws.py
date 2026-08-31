# backend/app/api/routes/ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.event_bus import event_bus

router = APIRouter()

@router.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await event_bus.connect(websocket)
    try:
        while True:
            # Keep connection alive, client may send ping
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        event_bus.disconnect(websocket)