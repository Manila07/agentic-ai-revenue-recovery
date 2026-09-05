import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sidebar from "./components/common/Sidebar";
import Navbar from "./components/common/Navbar";
import Dashboard from "./pages/Dashboard";
import Payments from "./pages/Payments";
import Recovery from "./pages/Recovery";
import Agent from "./pages/Agent";
import Analytics from "./pages/Analytics";
import LiveDemo from "./pages/LiveDemo";
import Settings from "./pages/Settings";
import NotFound from "./pages/NotFound";

export default function App() {
  return (
    <Router>
      <div className="flex h-screen bg-[#0f172a] text-slate-200">
        <Sidebar />
        <div className="flex-1 flex flex-col overflow-hidden">
          <Navbar />
          <main className="flex-1 overflow-y-auto p-6">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/payments" element={<Payments />} />
              <Route path="/recovery" element={<Recovery />} />
              <Route path="/agent" element={<Agent />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/live-demo" element={<LiveDemo />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}
