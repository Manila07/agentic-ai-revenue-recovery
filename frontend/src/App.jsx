import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Sidebar from './components/common/Sidebar'
import Navbar from './components/common/Navbar'
import Dashboard from './pages/Dashboard'
import Payments from './pages/Payments'
import Recovery from './pages/Recovery'
import AgentActivity from './pages/AgentActivity'
import Analytics from './pages/Analytics'
import Settings from './pages/Settings'
import NotFound from './pages/NotFound'
import LiveDemo from './pages/LiveDemo'

// inside Routes:
<Route path="/demo" element={<LiveDemo />} />

// Inline ErrorBoundary
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught:', error, errorInfo)
  }

  handleRetry = () => this.setState({ hasError: false, error: null })

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="text-center p-8">
            <h1 className="text-2xl font-bold">Something went wrong</h1>
            <p className="text-gray-600 mt-2">
              {this.state.error?.message || 'An unexpected error occurred.'}
            </p>
            <button onClick={this.handleRetry} className="mt-4 bg-primary text-white px-4 py-2 rounded">
              Try Again
            </button>
          </div>
        </div>
      )
    }
    return this.props.children
  }
}

export default function App() {
  return (
    <ErrorBoundary>
      <Router>
        <div className="flex h-screen bg-gray-50">
          <Sidebar />
          <div className="flex-1 flex flex-col overflow-hidden">
            <Navbar />
            <main className="flex-1 overflow-y-auto p-6">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/payments" element={<Payments />} />
                <Route path="/recovery" element={<Recovery />} />
                <Route path="/agent" element={<AgentActivity />} />
                <Route path="/analytics" element={<Analytics />} />
                <Route path="/settings" element={<Settings />} />
                <Route path="*" element={<NotFound />} />
              </Routes>
            </main>
          </div>
        </div>
      </Router>
    </ErrorBoundary>
  )
}