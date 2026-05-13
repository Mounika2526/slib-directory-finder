/**
 * CompareModal.jsx — Side-by-side API comparison modal for SLIB Finder
 *
 * Renders a full-screen overlay showing 2–4 selected APIs side by side.
 * Each field is displayed in a row, and cells that differ between APIs
 * are highlighted with a soft background colour so differences stand out.
 *
 * Key features:
 *   - Supports 2, 3, or 4 APIs simultaneously
 *   - Auto-adjusts grid column widths based on API count
 *   - Highlights differing cells with distinct pastel colours per column
 *   - Shows sample code section only if at least one API has code
 *   - Clicking the backdrop closes the modal
 *   - Horizontally scrollable on small screens
 *
 * Props:
 *   apis    — array of ApiEntry objects (2–4 items selected by the user)
 *   onClose — callback to close the modal and return to the directory
 */

import React from "react";
import { getRiskColor } from "../utils/riskHelpers";

function CompareModal({ apis, onClose }) {

  // Guard: need at least 2 APIs to show a meaningful comparison
  if (!apis || apis.length < 2) return null;

  // All fields shown in the comparison table rows.
  // label is the display name, key maps to the ApiEntry object property.
  const fields = [
    { label: "Category", key: "category" },
    { label: "Version", key: "version" },
    { label: "Developer", key: "developer" },
    { label: "Language", key: "programming_language" },
    { label: "Framework", key: "framework" },
    { label: "Cost", key: "cost" },
    { label: "Latency", key: "latency" },
    { label: "Scalability", key: "scalability" },
    { label: "Design Pattern", key: "design_pattern" },
    { label: "Risk Level", key: "risk_level" },
  ];

  // CSS grid column template — 180px for field labels, then equal columns for each API
  // Adjusts automatically based on how many APIs are being compared
  const colWidth =
    apis.length === 2 ? "1fr 1fr" :
    apis.length === 3 ? "1fr 1fr 1fr" :
    "1fr 1fr 1fr 1fr"; // max 4 columns

  // Pastel highlight colours for cells that differ between APIs.
  // Each column index gets its own colour so diffs are visually distinct.
  const diffColors = [
    { bg: "#fffbeb", border: "#fde68a" }, // amber  — column 0
    { bg: "#f0fdf4", border: "#bbf7d0" }, // green  — column 1
    { bg: "#eff6ff", border: "#bfdbfe" }, // blue   — column 2
    { bg: "#fdf4ff", border: "#e9d5ff" }, // purple — column 3
  ];

  return (
    // Full-screen backdrop — clicking directly on the backdrop closes the modal
    <div
      style={{
        position: "fixed", inset: 0, zIndex: 1000,
        background: "rgba(15,23,42,0.7)", backdropFilter: "blur(6px)",
        display: "flex", alignItems: "flex-start", justifyContent: "center",
        padding: "40px 16px", overflowY: "auto",
      }}
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      {/* Modal panel — max 1100px, horizontally scrollable for many APIs */}
      <div style={{
        background: "#fff", borderRadius: 28, width: "100%", maxWidth: 1100,
        boxShadow: "0 32px 80px rgba(0,0,0,0.25)", overflow: "hidden", flexShrink: 0,
      }}>

        {/* ── Modal header ── */}
        <div style={{
          background: "linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #312e81 100%)",
          padding: "28px 32px", display: "flex", alignItems: "center", justifyContent: "space-between",
        }}>
          <div>
            <p style={{ color: "#93c5fd", fontSize: 12, fontWeight: 600, letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: 6 }}>
              Side-by-Side Comparison
            </p>
            <h2 style={{ color: "#fff", fontSize: 24, fontWeight: 800, margin: 0 }}>
              Comparing {apis.length} APIs
            </h2>
          </div>
          {/* Close button — top right corner of the header */}
          <button
            onClick={onClose}
            style={{
              background: "rgba(255,255,255,0.1)", border: "1px solid rgba(255,255,255,0.2)",
              color: "#fff", borderRadius: 12, width: 40, height: 40,
              fontSize: 20, cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center",
            }}
          >×</button>
        </div>

        {/* ── Comparison table body ── */}
        <div style={{ padding: "0 32px 32px 32px", overflowX: "auto" }}>

          {/* ── API name header cards — one per selected API ── */}
          <div style={{
            display: "grid", gridTemplateColumns: `180px ${colWidth}`,
            gap: 16, paddingTop: 28, paddingBottom: 20,
            borderBottom: "2px solid #f1f5f9", marginBottom: 8,
          }}>
            {/* Empty cell for the label column */}
            <div />
            {apis.map((api) => (
              <div
                key={api.id}
                style={{
                  background: "linear-gradient(135deg, #eff6ff, #eef2ff)",
                  borderRadius: 20, padding: "18px 20px", border: "1px solid #bfdbfe",
                }}
              >
                {/* API name as the card title */}
                <h3 style={{ margin: "0 0 8px 0", fontSize: 17, fontWeight: 800, color: "#1e293b" }}>
                  {api.name}
                </h3>
                {/* Category and risk level badges under the name */}
                <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                  <span style={{ background: "#dbeafe", color: "#1d4ed8", borderRadius: 20, padding: "3px 10px", fontSize: 11, fontWeight: 600 }}>
                    {api.category}
                  </span>
                  <span style={{
                    // Risk background colour varies by level
                    background: api.risk_level === "High" ? "#fee2e2" : api.risk_level === "Medium" ? "#fef3c7" : "#d1fae5",
                    color: getRiskColor(api.risk_level),
                    borderRadius: 20, padding: "3px 10px", fontSize: 11, fontWeight: 600,
                  }}>
                    {api.risk_level || "Medium"} Risk
                  </span>
                </div>
              </div>
            ))}
          </div>

          {/* ── Description row — always shown, never highlighted as a diff ── */}
          <div style={{
            display: "grid", gridTemplateColumns: `180px ${colWidth}`,
            gap: 16, padding: "16px 0", borderBottom: "1px solid #f1f5f9",
          }}>
            <div style={{ display: "flex", alignItems: "center" }}>
              <span style={{ fontSize: 12, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.08em" }}>
                Description
              </span>
            </div>
            {apis.map((api) => (
              <p key={api.id} style={{ margin: 0, fontSize: 13, color: "#475569", lineHeight: 1.6 }}>
                {api.description || "—"}
              </p>
            ))}
          </div>

          {/* ── Field rows — one row per field in the fields array ── */}
          {fields.map((field, i) => {
            // Collect the value for this field from each API being compared
            const values = apis.map((a) => a[field.key] || "—");

            // If all values are the same, no highlighting is needed
            const allSame = values.every((v) => v === values[0]);

            return (
              <div
                key={field.key}
                style={{
                  display: "grid", gridTemplateColumns: `180px ${colWidth}`,
                  gap: 16, padding: "14px 0", borderBottom: "1px solid #f8fafc",
                  // Alternate row backgrounds for easier horizontal scanning
                  background: i % 2 === 0 ? "transparent" : "#fafbff", borderRadius: 8,
                }}
              >
                {/* Field label column */}
                <div style={{ display: "flex", alignItems: "center" }}>
                  <span style={{ fontSize: 12, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.08em" }}>
                    {field.label}
                  </span>
                </div>
                {/* Value cells — highlighted in pastel if values differ */}
                {apis.map((api, idx) => {
                  const val = api[field.key] || "—";
                  return (
                    <div
                      key={api.id}
                      style={{
                        padding: "6px 12px",
                        // Apply diff highlight only when not all values are the same
                        background: !allSame ? diffColors[idx % 4].bg : "transparent",
                        borderRadius: 10,
                        border: !allSame ? `1px solid ${diffColors[idx % 4].border}` : "none",
                      }}
                    >
                      {/* Risk level gets semantic color; all other fields are plain */}
                      {field.key === "risk_level" ? (
                        <span style={{ color: getRiskColor(val), fontWeight: 700, fontSize: 13 }}>
                          {val}
                        </span>
                      ) : (
                        <span style={{ fontSize: 13, fontWeight: 600, color: val === "—" ? "#cbd5e1" : "#1e293b" }}>
                          {val}
                        </span>
                      )}
                    </div>
                  );
                })}
              </div>
            );
          })}

          {/* ── Sample code row — only rendered if at least one API has code ── */}
          {apis.some((a) => a.sample_code) && (
            <div style={{
              display: "grid", gridTemplateColumns: `180px ${colWidth}`,
              gap: 16, padding: "20px 0 8px 0",
              borderTop: "2px solid #f1f5f9", marginTop: 8,
            }}>
              <div style={{ display: "flex", alignItems: "flex-start", paddingTop: 8 }}>
                <span style={{ fontSize: 12, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.08em" }}>
                  Sample Code
                </span>
              </div>
              {apis.map((api) => (
                <div key={api.id}>
                  {api.sample_code ? (
                    // Dark code block — max height 160px with scroll for long snippets
                    <pre style={{
                      margin: 0, padding: "14px 16px",
                      background: "#0f172a", color: "#e2e8f0",
                      borderRadius: 14, fontSize: 11, lineHeight: 1.6,
                      overflowX: "auto", whiteSpace: "pre-wrap",
                      wordBreak: "break-all", maxHeight: 160,
                    }}>
                      {api.sample_code}
                    </pre>
                  ) : (
                    // Placeholder shown when this API has no sample code
                    <span style={{ fontSize: 13, color: "#cbd5e1" }}>—</span>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* ── Footer legend — explains what the highlighted cells mean ── */}
          <div style={{ marginTop: 24, padding: "14px 20px", background: "#f8fafc", borderRadius: 16 }}>
            <span style={{ fontSize: 12, color: "#94a3b8", fontWeight: 600 }}>
              💡 Highlighted cells indicate differences between entries
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CompareModal;