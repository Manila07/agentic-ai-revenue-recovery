from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.event_bus import event_bus

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await event_bus.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await event_bus.disconnect(websocket)
