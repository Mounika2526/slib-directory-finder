/**
 * ReviewModal.jsx — Post-GitHub-fetch review form for SLIB Finder
 *
 * This modal appears after a successful GitHub repository fetch.
 * GitHub provides: name, developer, category, language, version, description.
 * GitHub cannot provide: framework, cost, latency, scalability, design_pattern,
 * or sample_code — so the user fills those in here before saving.
 *
 * Flow:
 *   1. User enters "owner/repo" in the drawer and clicks Fetch
 *   2. Backend calls GitHub API and returns available metadata
 *   3. ReviewModal opens with pre-filled read-only fields + empty manual fields
 *   4. User fills in missing fields and optionally generates sample code
 *   5. User clicks Save Entry → data is submitted to the backend
 *
 * Props:
 *   formData        — current form state (pre-filled from GitHub fetch)
 *   onUpdate        — callback(field, value) to update a single form field
 *   onGenerateCode  — callback to auto-fill sample_code from language template
 *   onConfirm       — callback when user clicks Save Entry
 *   onCancel        — callback when user dismisses the modal
 */

import React from "react";

function ReviewModal({ formData, onUpdate, onGenerateCode, onConfirm, onCancel }) {

  // Fields that GitHub cannot provide — user must fill these in manually.
  // Each field has a helpful placeholder showing accepted values.
  // These map directly to the ApiEntry model fields in the backend.
  const missingFields = [
    // API communication style — e.g. REST, GraphQL, gRPC, SDK
    { key: "framework", label: "Framework", placeholder: "e.g. REST, GraphQL, gRPC, SDK" },
    // Pricing model — determines the cost badge shown on the card
    { key: "cost", label: "Cost", placeholder: "e.g. Free, Paid/Premium, Freemium, Open Source" },
    // Response speed expectation — used in compare modal and stats charts
    { key: "latency", label: "Latency", placeholder: "e.g. Low, Medium, High" },
    // Ability to handle increased load — shown in scalability chart
    { key: "scalability", label: "Scalability", placeholder: "e.g. High, Medium, Low" },
    // Architectural pattern — used in design pattern distribution chart
    { key: "design_pattern", label: "Design Pattern", placeholder: "e.g. REST, GraphQL, Event-Driven, Pub/Sub" },
  ];

  return (
    // Full-screen backdrop with blur effect
    // Clicking outside does nothing — user must explicitly confirm or cancel
    <div
      style={{
        position: "fixed", inset: 0, zIndex: 1000,
        background: "rgba(15,23,42,0.7)",
        backdropFilter: "blur(6px)",
        display: "flex", alignItems: "center", justifyContent: "center",
        padding: "24px 16px", overflowY: "auto",
      }}
    >
      {/* Modal container — max 600px wide, rounded corners */}
      <div style={{
        background: "#fff", borderRadius: 28, width: "100%", maxWidth: 600,
        boxShadow: "0 32px 80px rgba(0,0,0,0.25)", overflow: "hidden",
      }}>

        {/* ── Modal header — dark gradient matches the main page header ── */}
        <div style={{
          background: "linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #312e81 100%)",
          padding: "24px 28px",
        }}>
          {/* Success indicator — shown after a successful GitHub fetch */}
          <p style={{ color: "#93c5fd", fontSize: 12, fontWeight: 600, letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: 6 }}>
            GitHub Data Fetched ✓
          </p>
          <h2 style={{ color: "#fff", fontSize: 20, fontWeight: 800, margin: "0 0 4px 0" }}>
            Review & Complete Entry
          </h2>
          <p style={{ color: "#94a3b8", fontSize: 13, margin: 0 }}>
            Fill in the fields below that GitHub couldn't provide, then save.
          </p>
        </div>

        {/* ── Scrollable body — max height 70vh to handle small screens ── */}
        <div style={{ padding: "24px 28px", maxHeight: "70vh", overflowY: "auto" }}>

          {/* Read-only summary of data already fetched from GitHub.
              Shown so the user can verify the data before filling in the rest. */}
          <div style={{
            background: "#f8fafc", borderRadius: 16, padding: "14px 18px",
            marginBottom: 20, border: "1px solid #e2e8f0",
          }}>
            <p style={{ margin: "0 0 8px 0", fontSize: 12, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.08em" }}>
              Fetched from GitHub
            </p>
            {/* Two-column grid for compact display of fetched values */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "6px 16px" }}>
              {[
                { label: "Name", value: formData.name },
                { label: "Developer", value: formData.developer },
                { label: "Category", value: formData.category },
                { label: "Language", value: formData.programming_language || "Unknown" },
                { label: "Version", value: formData.version },
              ].map(({ label, value }) => (
                <div key={label}>
                  <span style={{ fontSize: 11, color: "#94a3b8", fontWeight: 600 }}>{label}: </span>
                  <span style={{ fontSize: 12, color: "#1e293b", fontWeight: 600 }}>{value || "—"}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Manual input fields — rendered from the missingFields array above */}
          <p style={{ margin: "0 0 12px 0", fontSize: 13, fontWeight: 700, color: "#374151" }}>
            Please fill in the missing fields:
          </p>
          <div style={{ display: "flex", flexDirection: "column", gap: 12, marginBottom: 20 }}>
            {missingFields.map((field) => (
              <div key={field.key}>
                <label style={{ display: "block", fontSize: 13, fontWeight: 600, color: "#374151", marginBottom: 6 }}>
                  {field.label}
                </label>
                {/* Controlled input — calls onUpdate with field key and new value */}
                <input
                  type="text"
                  value={formData[field.key] || ""}
                  onChange={(e) => onUpdate(field.key, e.target.value)}
                  placeholder={field.placeholder}
                  style={{
                    width: "100%", boxSizing: "border-box",
                    borderRadius: 14, border: "1px solid #cbd5e1",
                    background: "#f8fafc", padding: "10px 14px",
                    fontSize: 13, color: "#1e293b", outline: "none",
                  }}
                />
              </div>
            ))}
          </div>

          {/* ── Sample code section ── */}
          <div style={{ borderTop: "1px solid #f1f5f9", paddingTop: 16 }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 8 }}>
              <label style={{ fontSize: 13, fontWeight: 700, color: "#374151" }}>
                Sample Code
              </label>
              {/* Generate button — triggers codeGenerator with the detected language.
                  Produces a starter snippet the user can then edit as needed. */}
              <button
                type="button"
                onClick={onGenerateCode}
                style={{
                  background: "#6366f1", color: "#fff",
                  border: "none", borderRadius: 10,
                  padding: "6px 14px", fontSize: 12, fontWeight: 700,
                  cursor: "pointer",
                }}
              >
                ✨ Generate from Template
              </button>
            </div>
            {/* Language hint — shows what language was detected from GitHub */}
            <p style={{ margin: "0 0 8px 0", fontSize: 11, color: "#94a3b8" }}>
              Language detected: <strong>{formData.programming_language || "Unknown"}</strong> — click Generate to auto-fill a starter snippet, then edit as needed.
            </p>
            {/* Dark-themed code textarea — monospace font for readability */}
            <textarea
              value={formData.sample_code || ""}
              onChange={(e) => onUpdate("sample_code", e.target.value)}
              placeholder="Paste or generate sample usage code here..."
              rows={6}
              style={{
                width: "100%", boxSizing: "border-box",
                borderRadius: 14, border: "1px solid #cbd5e1",
                background: "#0f172a", padding: "12px 14px",
                fontSize: 12, color: "#e2e8f0", fontFamily: "monospace",
                outline: "none", resize: "vertical",
              }}
            />
          </div>
        </div>

        {/* ── Footer action buttons ── */}
        {/* Cancel dismisses the modal without saving.
            Save Entry submits the completed form to the backend via onConfirm. */}
        <div style={{
          padding: "16px 28px 24px 28px",
          display: "flex", gap: 12, justifyContent: "flex-end",
          borderTop: "1px solid #f1f5f9",
        }}>
          <button
            onClick={onCancel}
            style={{
              background: "white", color: "#64748b",
              border: "1px solid #e2e8f0", borderRadius: 14,
              padding: "10px 20px", fontSize: 13, fontWeight: 600,
              cursor: "pointer",
            }}
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            style={{
              background: "#3b82f6", color: "#fff",
              border: "none", borderRadius: 14,
              padding: "10px 24px", fontSize: 13, fontWeight: 700,
              cursor: "pointer",
            }}
          >
            Save Entry
          </button>
        </div>
      </div>
    </div>
  );
}

export default ReviewModal;