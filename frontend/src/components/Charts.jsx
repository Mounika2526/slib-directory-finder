/**
 * Charts.jsx — Reusable chart and KPI components for SLIB Finder Stats Dashboard
 *
 * All charts are built with plain HTML/CSS — no external charting library needed.
 * This keeps the bundle small and gives full control over styling.
 *
 * Exports:
 *   SimpleBarChart — horizontal bar chart using div widths as bar lengths
 *   DonutChart     — circular donut chart using CSS conic-gradient
 *   StatCard       — single KPI tile with an icon, label, and value
 *
 * All three components are consumed by StatsTab.jsx.
 * Color values are passed in via props so the parent controls the palette.
 */

import React from "react";

// ─────────────────────────────────────────────────────────────────────────────
// COMPONENT: SimpleBarChart
//
// Renders a horizontal bar chart using plain divs.
// Bar widths are calculated as a percentage of the maximum value in the dataset.
// Includes a label on the left and the numeric value on the right.
//
// Props:
//   data  — array of { label: string, value: number, color: string }
//   title — optional section heading shown above the chart
// ─────────────────────────────────────────────────────────────────────────────
export function SimpleBarChart({ data, title }) {
  // Find the largest value so all bars are scaled relative to it
  const max = Math.max(...data.map((d) => d.value), 1);

  return (
    <div>
      {/* Optional title above the chart */}
      {title && (
        <p className="mb-4 text-sm font-bold uppercase tracking-wide text-slate-500">
          {title}
        </p>
      )}
      <div className="space-y-3">
        {data.map((item) => (
          <div key={item.label}>
            {/* Row: label on left, value on right */}
            <div className="mb-1 flex items-center justify-between gap-2">
              <span
                className="truncate text-sm font-medium text-slate-700"
                style={{ maxWidth: "65%" }}
              >
                {item.label}
              </span>
              <span className="text-sm font-bold text-slate-900">{item.value}</span>
            </div>
            {/* Bar track — grey background with colored fill */}
            <div className="h-2.5 w-full overflow-hidden rounded-full bg-slate-100">
              <div
                className="h-full rounded-full transition-all duration-700"
                style={{
                  // Width is proportional to this item's value vs the max
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

// ─────────────────────────────────────────────────────────────────────────────
// COMPONENT: DonutChart
//
// Renders a circular donut chart using a single CSS conic-gradient.
// Each segment is defined by its start and end percentage around the circle.
// The centre hole shows the total count across all segments.
// A colour-coded legend is shown beside the donut ring.
//
// Props:
//   segments — array of { label: string, value: number, color: string }
//   title    — optional section heading shown above the chart
// ─────────────────────────────────────────────────────────────────────────────
export function DonutChart({ segments, title }) {
  // Total across all segments — used for percentage calculations
  const total = segments.reduce((sum, s) => sum + s.value, 0);

  // Nothing to render if all values are zero
  if (total === 0) return null;

  // Build the conic-gradient string by accumulating percentages
  // Each segment starts where the previous one ended
  let cumulative = 0;
  const gradient = `conic-gradient(${segments
    .map((seg) => {
      const pct = (seg.value / total) * 100;
      const part = `${seg.color} ${cumulative}% ${cumulative + pct}%`;
      cumulative += pct; // advance the start point for the next segment
      return part;
    })
    .join(", ")})`;

  return (
    <div>
      {/* Optional title above the chart */}
      {title && (
        <p className="mb-4 text-sm font-bold uppercase tracking-wide text-slate-500">
          {title}
        </p>
      )}
      <div className="flex flex-col items-center gap-6 sm:flex-row sm:items-start">

        {/* Donut ring — the conic-gradient div with a white centre hole */}
        <div className="relative flex-shrink-0">
          <div
            style={{
              width: 140, height: 140,
              borderRadius: "50%",
              background: gradient,
            }}
          />
          {/* White circle in the centre creates the donut hole effect */}
          <div
            style={{
              position: "absolute", top: "50%", left: "50%",
              transform: "translate(-50%, -50%)",
              width: 80, height: 80,
              borderRadius: "50%", background: "white",
              display: "flex", alignItems: "center", justifyContent: "center",
            }}
          >
            {/* Total count displayed in the centre of the donut */}
            <span className="text-lg font-black text-slate-800">{total}</span>
          </div>
        </div>

        {/* Legend — colour dot + label + count + percentage */}
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

// ─────────────────────────────────────────────────────────────────────────────
// COMPONENT: StatCard
//
// A single KPI tile shown in the 4-column grid at the top of the Stats Dashboard.
// Displays a label, a large numeric value, and a matching SVG icon.
// Background and border colours are derived from the passed color prop.
//
// Props:
//   label — short description shown above the number (e.g. "Total APIs")
//   value — the numeric KPI value to display
//   color — hex color string used for text, border, and icon stroke
//   icon  — one of "apis" | "categories" | "developers" | "lowrisk"
// ─────────────────────────────────────────────────────────────────────────────
export function StatCard({ label, value, color, icon }) {

  // SVG icon definitions — each icon is a 20×20 outline SVG
  // Stroke color is driven by the color prop for visual consistency
  const icons = {
    // Monitor icon — represents API entries
    apis: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2" y="3" width="20" height="14" rx="2" />
        <path d="M8 21h8M12 17v4" />
      </svg>
    ),
    // Four squares icon — represents categories
    categories: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="3" width="7" height="7" rx="1" />
        <rect x="14" y="3" width="7" height="7" rx="1" />
        <rect x="3" y="14" width="7" height="7" rx="1" />
        <rect x="14" y="14" width="7" height="7" rx="1" />
      </svg>
    ),
    // People icon — represents unique developers
    developers: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
        <circle cx="9" cy="7" r="4" />
        <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
        <path d="M16 3.13a4 4 0 0 1 0 7.75" />
      </svg>
    ),
    // Shield with checkmark — represents low-risk APIs
    lowrisk: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
        <polyline points="9 12 11 14 15 10" />
      </svg>
    ),
  };

  return (
    // Card border and background tint are derived from the color prop
    // "33" suffix = 20% opacity hex, "0d" suffix = 5% opacity hex
    <div
      className="rounded-2xl border px-5 py-4 shadow-sm"
      style={{ borderColor: color + "33", background: color + "0d" }}
    >
      <div className="flex items-center justify-between gap-2">
        <div>
          {/* Label — small uppercase text in the brand color */}
          <p className="text-xs font-bold uppercase tracking-wide" style={{ color }}>
            {label}
          </p>
          {/* Value — large bold number */}
          <p className="mt-1 text-2xl font-black text-slate-900">{value}</p>
        </div>
        {/* Icon container — lightly tinted circle matching the color */}
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