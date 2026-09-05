import { useEffect, useRef, useCallback } from "react";

const WS_URL = "ws://localhost:8000/ws";

export function useWebSocket(onMessage) {
  const wsRef = useRef(null);
  const reconnectRef = useRef(null);

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("🔌 WebSocket connected");
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        if (onMessage) onMessage(msg);
      } catch (e) {
        console.error("WebSocket parse error:", e);
      }
    };

    ws.onclose = () => {
      console.log("🔌 WebSocket disconnected, reconnecting in 3s...");
      reconnectRef.current = setTimeout(connect, 3000);
    };

    ws.onerror = (err) => {
      console.error("WebSocket error:", err);
      ws.close();
    };
  }, [onMessage]);

  useEffect(() => {
    connect();
    return () => {
      clearTimeout(reconnectRef.current);
      wsRef.current?.close();
    };
  }, [connect]);
}
