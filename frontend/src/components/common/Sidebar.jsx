import React from "react";
import { NavLink } from "react-router-dom";
import { 
  LayoutDashboard, CreditCard, RotateCcw, Bot, BarChart3, Play, Settings 
} from "lucide-react";

const links = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/payments", label: "Payments", icon: CreditCard },
  { to: "/recovery", label: "Recovery", icon: RotateCcw },
  { to: "/agent", label: "Agent", icon: Bot },
  { to: "/analytics", label: "Analytics", icon: BarChart3 },
  { to: "/live-demo", label: "Live Demo", icon: Play },
  { to: "/settings", label: "Settings", icon: Settings },
];

export default function Sidebar() {
  return (
    <aside style={{ width: 256, backgroundColor: '#1e293b', borderRight: '1px solid #334155' }}>
      <div style={{ padding: 24, borderBottom: '1px solid #334155' }}>
        <h1 style={{ fontSize: 20, fontWeight: 'bold', color: '#818cf8' }}>
          🤖 Revenue Recovery
        </h1>
        <p style={{ fontSize: 12, color: '#94a3b8', marginTop: 4 }}>
          Agentic AI Platform
        </p>
      </div>
      <nav style={{ padding: 16 }}>
        {links.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === "/"}
            style={({ isActive }) => ({
              display: 'flex',
              alignItems: 'center',
              gap: 12,
              padding: '10px 16px',
              borderRadius: 8,
              marginBottom: 4,
              color: isActive ? '#ffffff' : '#94a3b8',
              backgroundColor: isActive ? '#4f46e5' : 'transparent',
              textDecoration: 'none',
              fontSize: 14,
            })}
          >
            <Icon size={18} />
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
