import React, { useState, useEffect, useRef } from 'react'
import api from '../services/api'

export default function LiveDemo() {
  const [events, setEvents] = useState([])
  const [isRunning, setIsRunning] = useState(false)
  const wsRef = useRef(null)

  useEffect(() => {
    // Connect WebSocket
    const ws = new WebSocket('ws://localhost:8000/api/v1/ws/live')
    wsRef.current = ws

    ws.onopen = () => console.log('WebSocket connected')
    ws.onmessage = (e) => {
      const event = JSON.parse(e.data)
      setEvents(prev => [...prev, event])
    }
    ws.onerror = (e) => console.error('WebSocket error', e)

    return () => {
      ws.close()
    }
  }, [])

  const simulate = async () => {
    setIsRunning(true)
    try {
      await api.post('/payments/simulate-failure', {
        amount: Math.random() * 5000 + 100
      })
      // The events will stream via WebSocket
    } catch (err) {
      console.error('Simulation failed', err)
    }
    setTimeout(() => setIsRunning(false), 10000) // stop after 10s
  }

  const getEventColor = (type) => {
    switch (type) {
      case 'PAYMENT_FAILED': return 'bg-red-100 text-red-800'
      case 'PAYMENT_ANALYZED': return 'bg-blue-100 text-blue-800'
      case 'RECOVERY_EXECUTED': return 'bg-green-100 text-green-800'
      case 'RECOVERY_BLOCKED': return 'bg-orange-100 text-orange-800'
      case 'HUMAN_APPROVAL_REQUIRED': return 'bg-yellow-100 text-yellow-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Live Demo</h1>
        <button
          onClick={simulate}
          disabled={isRunning}
          className="bg-primary text-white px-6 py-2 rounded-lg disabled:opacity-50"
        >
          {isRunning ? 'Processing...' : 'Simulate Failed Payment'}
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold mb-4">Real-time Recovery Workflow</h3>
        {events.length === 0 && (
          <p className="text-gray-500">No events yet. Click "Simulate Failed Payment" to see the agent in action.</p>
        )}
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {events.map((event, idx) => (
            <div key={idx} className={`p-3 rounded-lg ${getEventColor(event.type)}`}>
              <div className="flex justify-between">
                <span className="font-semibold">{event.type}</span>
                <span className="text-xs">{new Date().toLocaleTimeString()}</span>
              </div>
              <div className="mt-1 text-sm">
                {event.payment_id && <span>Payment: {event.payment_id}</span>}
                {event.action && <span className="ml-2">Action: {event.action}</span>}
                {event.recovery_probability && <span className="ml-2">Prob: {(event.recovery_probability * 100).toFixed(0)}%</span>}
                {event.message && <span className="ml-2">{event.message}</span>}
              </div>
            </div>
          ))}
        </div>
      </div>

      {isRunning && (
        <div className="flex justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      )}
    </div>
  )
}