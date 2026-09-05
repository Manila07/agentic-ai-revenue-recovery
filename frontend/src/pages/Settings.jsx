import { useState } from "react";

const DEFAULTS = {
  maxRetries: 3,
  retryIntervalMinutes: 30,
  autoRecoveryThreshold: 0.7,
  requireHumanApprovalAbove: 10000,
  enableSmsNotifications: true,
  enableEmailNotifications: true,
  enableWhatsappNotifications: false,
  autoExecute: true,
};

export default function Settings() {
  const [config, setConfig] = useState(DEFAULTS);
  const [saved, setSaved] = useState(false);

  function update(key, value) {
    setConfig((prev) => ({ ...prev, [key]: value }));
    setSaved(false);
  }

  function handleSave() {
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  }

  return (
    <div className="p-6 max-w-3xl">
      <h1 className="text-2xl font-bold text-white mb-2">Settings</h1>
      <p className="text-gray-400 text-sm mb-6">
        Configure agent behavior and recovery thresholds
      </p>

      {/* Recovery Settings */}
      <Section title="🔄 Recovery Settings">
        <Field label="Max Retries per Payment">
          <input
            type="number"
            value={config.maxRetries}
            onChange={(e) => update("maxRetries", +e.target.value)}
            className="bg-gray-900 border border-gray-600 rounded px-3 py-2 text-white w-24"
          />
        </Field>
        <Field label="Retry Interval (minutes)">
          <input
            type="number"
            value={config.retryIntervalMinutes}
            onChange={(e) => update("retryIntervalMinutes", +e.target.value)}
            className="bg-gray-900 border border-gray-600 rounded px-3 py-2 text-white w-24"
          />
        </Field>
        <Field label="Auto-Recovery Threshold (probability)">
          <div className="flex items-center gap-3">
            <input
              type="range"
              min="0"
              max="1"
              step="0.05"
              value={config.autoRecoveryThreshold}
              onChange={(e) => update("autoRecoveryThreshold", +e.target.value)}
              className="flex-1"
            />
            <span className="text-white font-mono w-16">
              {(config.autoRecoveryThreshold * 100).toFixed(0)}%
            </span>
          </div>
        </Field>
        <Field label="Require Human Approval Above (₹)">
          <input
            type="number"
            value={config.requireHumanApprovalAbove}
            onChange={(e) => update("requireHumanApprovalAbove", +e.target.value)}
            className="bg-gray-900 border border-gray-600 rounded px-3 py-2 text-white w-32"
          />
        </Field>
        <Field label="Auto-Execute Recoveries">
          <Toggle
            value={config.autoExecute}
            onChange={(v) => update("autoExecute", v)}
          />
        </Field>
      </Section>

      {/* Notification Settings */}
      <Section title="🔔 Notifications">
        <Field label="SMS Notifications">
          <Toggle
            value={config.enableSmsNotifications}
            onChange={(v) => update("enableSmsNotifications", v)}
          />
        </Field>
        <Field label="Email Notifications">
          <Toggle
            value={config.enableEmailNotifications}
            onChange={(v) => update("enableEmailNotifications", v)}
          />
        </Field>
        <Field label="WhatsApp Notifications">
          <Toggle
            value={config.enableWhatsappNotifications}
            onChange={(v) => update("enableWhatsappNotifications", v)}
          />
        </Field>
      </Section>

      {/* Agent Info */}
      <Section title="ℹ️ Agent Info">
        <div className="space-y-2 text-sm">
          <InfoRow label="Agent Version" value="1.0.0" />
          <InfoRow label="Model" value="Rule-Based + ML Predictor" />
          <InfoRow label="Strategies Available" value="8" />
          <InfoRow label="Mode" value="Simulation (Buildathon)" />
        </div>
      </Section>

      {/* Save */}
      <button
        onClick={handleSave}
        className={`px-6 py-2 rounded font-bold text-white transition-all ${
          saved
            ? "bg-green-600"
            : "bg-blue-600 hover:bg-blue-500"
        }`}
      >
        {saved ? "✅ Saved!" : "Save Settings"}
      </button>
    </div>
  );
}

function Section({ title, children }) {
  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700 p-4 mb-6">
      <h3 className="text-white font-semibold mb-4">{title}</h3>
      <div className="space-y-4">{children}</div>
    </div>
  );
}

function Field({ label, children }) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-gray-300 text-sm">{label}</span>
      {children}
    </div>
  );
}

function Toggle({ value, onChange }) {
  return (
    <button
      onClick={() => onChange(!value)}
      className={`w-12 h-6 rounded-full transition-all ${
        value ? "bg-green-500" : "bg-gray-600"
      }`}
    >
      <div
        className={`w-5 h-5 bg-white rounded-full transition-all mx-0.5 ${
          value ? "translate-x-6" : ""
        }`}
      />
    </button>
  );
}

function InfoRow({ label, value }) {
  return (
    <div className="flex justify-between">
      <span className="text-gray-400">{label}</span>
      <span className="text-white">{value}</span>
    </div>
  );
}
