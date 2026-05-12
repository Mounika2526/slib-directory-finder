/**
 * CompareModal.jsx — Side-by-side API comparison modal for SLIB Finder
 *
 * Full-screen overlay showing up to 4 selected APIs side by side.
 * Highlights cells where values differ between entries.
 *
 * Props:
 *   apis    — array of ApiEntry objects (2–4 items)
 *   onClose — callback to close the modal
 */

import React from "react";
import { getRiskColor } from "../utils/riskHelpers";

function CompareModal({ apis, onClose }) {
  if (!apis || apis.length < 2) return null;

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

  const colWidth =
    apis.length === 2 ? "1fr 1fr" :
    apis.length === 3 ? "1fr 1fr 1fr" :
    "1fr 1fr 1fr 1fr";

  const diffColors = [
    { bg: "#fffbeb", border: "#fde68a" },
    { bg: "#f0fdf4", border: "#bbf7d0" },
    { bg: "#eff6ff", border: "#bfdbfe" },
    { bg: "#fdf4ff", border: "#e9d5ff" },
  ];

  return (
    <div
      style={{
        position: "fixed", inset: 0, zIndex: 1000,
        background: "rgba(15,23,42,0.7)", backdropFilter: "blur(6px)",
        display: "flex", alignItems: "flex-start", justifyContent: "center",
        padding: "40px 16px", overflowY: "auto",
      }}
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div style={{
        background: "#fff", borderRadius: 28, width: "100%", maxWidth: 1100,
        boxShadow: "0 32px 80px rgba(0,0,0,0.25)", overflow: "hidden", flexShrink: 0,
      }}>

        {/* Modal header */}
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
          <button
            onClick={onClose}
            style={{
              background: "rgba(255,255,255,0.1)", border: "1px solid rgba(255,255,255,0.2)",
              color: "#fff", borderRadius: 12, width: 40, height: 40,
              fontSize: 20, cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center",
            }}
          >×</button>
        </div>

        <div style={{ padding: "0 32px 32px 32px", overflowX: "auto" }}>

          {/* API name headers */}
          <div style={{
            display: "grid", gridTemplateColumns: `180px ${colWidth}`,
            gap: 16, paddingTop: 28, paddingBottom: 20,
            borderBottom: "2px solid #f1f5f9", marginBottom: 8,
          }}>
            <div />
            {apis.map((api) => (
              <div
                key={api.id}
                style={{
                  background: "linear-gradient(135deg, #eff6ff, #eef2ff)",
                  borderRadius: 20, padding: "18px 20px", border: "1px solid #bfdbfe",
                }}
              >
                <h3 style={{ margin: "0 0 8px 0", fontSize: 17, fontWeight: 800, color: "#1e293b" }}>
                  {api.name}
                </h3>
                <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                  <span style={{ background: "#dbeafe", color: "#1d4ed8", borderRadius: 20, padding: "3px 10px", fontSize: 11, fontWeight: 600 }}>
                    {api.category}
                  </span>
                  <span style={{
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

          {/* Description row */}
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

          {/* Field rows */}
          {fields.map((field, i) => {
            const values = apis.map((a) => a[field.key] || "—");
            const allSame = values.every((v) => v === values[0]);
            return (
              <div
                key={field.key}
                style={{
                  display: "grid", gridTemplateColumns: `180px ${colWidth}`,
                  gap: 16, padding: "14px 0", borderBottom: "1px solid #f8fafc",
                  background: i % 2 === 0 ? "transparent" : "#fafbff", borderRadius: 8,
                }}
              >
                <div style={{ display: "flex", alignItems: "center" }}>
                  <span style={{ fontSize: 12, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.08em" }}>
                    {field.label}
                  </span>
                </div>
                {apis.map((api, idx) => {
                  const val = api[field.key] || "—";
                  return (
                    <div
                      key={api.id}
                      style={{
                        padding: "6px 12px",
                        background: !allSame ? diffColors[idx % 4].bg : "transparent",
                        borderRadius: 10,
                        border: !allSame ? `1px solid ${diffColors[idx % 4].border}` : "none",
                      }}
                    >
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

          {/* Sample code row — only shown if at least one API has sample code */}
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
                    <span style={{ fontSize: 13, color: "#cbd5e1" }}>—</span>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Diff legend */}
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