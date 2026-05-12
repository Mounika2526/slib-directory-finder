/**
 * Charts.jsx — Reusable chart components for SLIB Finder Stats Dashboard
 *
 * Exports:
 *   SimpleBarChart — horizontal bar chart using plain divs
 *   DonutChart     — CSS conic-gradient donut chart
 *   StatCard       — single KPI tile with icon and value
 */

import React from "react";

// ─────────────────────────────────────────────
// COMPONENT: SimpleBarChart
// Horizontal bar chart using plain divs.
// Props:
//   data  — [{ label, value, color }]
//   title — string
// ─────────────────────────────────────────────
export function SimpleBarChart({ data, title }) {
  const max = Math.max(...data.map((d) => d.value), 1);
  return (
    <div>
      {title && (
        <p className="mb-4 text-sm font-bold uppercase tracking-wide text-slate-500">
          {title}
        </p>
      )}
      <div className="space-y-3">
        {data.map((item) => (
          <div key={item.label}>
            <div className="mb-1 flex items-center justify-between gap-2">
              <span
                className="truncate text-sm font-medium text-slate-700"
                style={{ maxWidth: "65%" }}
              >
                {item.label}
              </span>
              <span className="text-sm font-bold text-slate-900">{item.value}</span>
            </div>
            <div className="h-2.5 w-full overflow-hidden rounded-full bg-slate-100">
              <div
                className="h-full rounded-full transition-all duration-700"
                style={{
                  width: `${(item.value / max) * 100}%`,
                  background: item.color || "#3b82f6",
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// COMPONENT: DonutChart
// CSS conic-gradient donut chart.
// Props:
//   segments — [{ label, value, color }]
//   title    — string
// ─────────────────────────────────────────────
export function DonutChart({ segments, title }) {
  const total = segments.reduce((sum, s) => sum + s.value, 0);
  if (total === 0) return null;

  let cumulative = 0;
  const gradient = `conic-gradient(${segments
    .map((seg) => {
      const pct = (seg.value / total) * 100;
      const part = `${seg.color} ${cumulative}% ${cumulative + pct}%`;
      cumulative += pct;
      return part;
    })
    .join(", ")})`;

  return (
    <div>
      {title && (
        <p className="mb-4 text-sm font-bold uppercase tracking-wide text-slate-500">
          {title}
        </p>
      )}
      <div className="flex flex-col items-center gap-6 sm:flex-row sm:items-start">
        {/* Donut ring */}
        <div className="relative flex-shrink-0">
          <div
            style={{
              width: 140, height: 140,
              borderRadius: "50%",
              background: gradient,
            }}
          />
          {/* Centre hole with total count */}
          <div
            style={{
              position: "absolute", top: "50%", left: "50%",
              transform: "translate(-50%, -50%)",
              width: 80, height: 80,
              borderRadius: "50%", background: "white",
              display: "flex", alignItems: "center", justifyContent: "center",
            }}
          >
            <span className="text-lg font-black text-slate-800">{total}</span>
          </div>
        </div>

        {/* Legend */}
        <div className="flex flex-col gap-2">
          {segments.map((seg) => (
            <div key={seg.label} className="flex items-center gap-2">
              <div
                className="h-3 w-3 flex-shrink-0 rounded-full"
                style={{ background: seg.color }}
              />
              <span className="text-sm text-slate-700">
                {seg.label}{" "}
                <span className="font-bold text-slate-900">{seg.value}</span>{" "}
                <span className="text-slate-400">
                  ({Math.round((seg.value / total) * 100)}%)
                </span>
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// COMPONENT: StatCard
// Single KPI tile with label, value, color, and icon.
// Props:
//   label — string
//   value — number
//   color — hex color string
//   icon  — "apis" | "categories" | "developers" | "lowrisk"
// ─────────────────────────────────────────────
export function StatCard({ label, value, color, icon }) {
  const icons = {
    apis: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2" y="3" width="20" height="14" rx="2" />
        <path d="M8 21h8M12 17v4" />
      </svg>
    ),
    categories: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="3" width="7" height="7" rx="1" />
        <rect x="14" y="3" width="7" height="7" rx="1" />
        <rect x="3" y="14" width="7" height="7" rx="1" />
        <rect x="14" y="14" width="7" height="7" rx="1" />
      </svg>
    ),
    developers: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
        <circle cx="9" cy="7" r="4" />
        <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
        <path d="M16 3.13a4 4 0 0 1 0 7.75" />
      </svg>
    ),
    lowrisk: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
        <polyline points="9 12 11 14 15 10" />
      </svg>
    ),
  };

  return (
    <div
      className="rounded-2xl border px-5 py-4 shadow-sm"
      style={{ borderColor: color + "33", background: color + "0d" }}
    >
      <div className="flex items-center justify-between gap-2">
        <div>
          <p className="text-xs font-bold uppercase tracking-wide" style={{ color }}>
            {label}
          </p>
          <p className="mt-1 text-2xl font-black text-slate-900">{value}</p>
        </div>
        <div
          style={{
            padding: 8, borderRadius: 10,
            background: color + "20", flexShrink: 0,
          }}
        >
          {icons[icon] || null}
        </div>
      </div>
    </div>
  );
}