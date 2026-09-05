import React from "react";
import { Bell } from "lucide-react";

export default function Navbar() {
  return (
    <header style={{ 
      height: 64, 
      backgroundColor: '#1e293b', 
      borderBottom: '1px solid #334155',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 24px'
    }}>
      <h2 style={{ fontSize: 18, fontWeight: '600', color: '#e2e8f0' }}>
        Agentic AI Revenue Recovery
      </h2>
      <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
        <button style={{ 
          position: 'relative', 
          background: 'none', 
          border: 'none', 
          color: '#94a3b8',
          cursor: 'pointer'
        }}>
          <Bell size={20} />
          <span style={{ 
            position: 'absolute', 
            top: 0, 
            right: 0, 
            width: 8, 
            height: 8, 
            backgroundColor: '#ef4444', 
            borderRadius: '50%' 
          }}></span>
        </button>
        <div style={{ 
          width: 32, 
          height: 32, 
          backgroundColor: '#4f46e5', 
          borderRadius: '50%', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center', 
          color: '#fff', 
          fontSize: 14 
        }}>A</div>
      </div>
    </header>
  );
}
