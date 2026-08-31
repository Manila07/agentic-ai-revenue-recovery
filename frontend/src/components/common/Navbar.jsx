import React, { useState, useEffect } from 'react'

export default function Navbar() {
  const [isConnected, setIsConnected] = useState(false)
  const [liveEvent, setLiveEvent] = useState(null)

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/api/v1/ws/live') // URL for your backend
    
    ws.onopen = () => {
      setIsConnected(true)
      console.log('Live connection established')
    }
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setLiveEvent(data)
      
      // Example: Show toast notification for new events
      if (data.type === 'PAYMENT_FAILED') {
        // Trigger your notification system
        console.log('Payment failed', data)
      }
    }
    
    ws.onclose = () => setIsConnected(false)
    
    return () => ws.close()
  }, [])

  return (
    <nav className="bg-white shadow px-6 py-3 flex items-center justify-between">
      <h1 className="text-xl font-semibold">Agentic AI Revenue Recovery</h1>
      <div className="flex items-center gap-4">
        <span className={`flex items-center gap-1 text-sm ${isConnected ? 'text-green-600' : 'text-gray-500'}`}>
          <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-gray-400'}`}></span>
          {isConnected ? 'Live' : 'Offline'}
        </span>
        <button className="bg-primary text-white px-3 py-1 rounded">Logout</button>
      </div>
    </nav>
  )
}