import React, { useState } from 'react'

export default function Settings() {
  const [settings, setSettings] = useState({
    max_retries: 3,
    cooldown_minutes: 60,
    max_auto_approval: 5000,
    require_approval: true,
  })

  const handleChange = (e) => setSettings({ ...settings, [e.target.name]: e.target.value })

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
      <div className="bg-white rounded-lg p-6 shadow-card border border-gray-200 max-w-lg">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Max Retries per Payment</label>
            <input
              type="number"
              name="max_retries"
              value={settings.max_retries}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Cooldown (minutes)</label>
            <input
              type="number"
              name="cooldown_minutes"
              value={settings.cooldown_minutes}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Max Auto Approval Amount</label>
            <input
              type="number"
              name="max_auto_approval"
              value={settings.max_auto_approval}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <button className="btn btn-primary w-full">Save Settings</button>
        </div>
      </div>
    </div>
  )
}