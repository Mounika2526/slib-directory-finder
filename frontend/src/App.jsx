/**
 * App.jsx — Main application component for SLIB Finder: API & Microservices Directory
 *
 * Features:
 *  - Add / Edit / Delete API entries
 *  - GitHub auto-fill (fetch repo metadata automatically)
 *  - Post-fetch review modal: user fills in missing fields (framework, cost, latency, etc.)
 *  - Sample code generation from language templates (no API key needed)
 *  - Search & filter by keyword and category
 *  - Side-by-side comparison of up to 4 APIs
 *  - Stats Dashboard: charts by category, developer, risk, language
 */

import { useEffect, useMemo, useState } from "react";

// ─────────────────────────────────────────────
// BACKEND BASE URL — update if deployment changes
// ─────────────────────────────────────────────
const API_BASE = "https://slib-directory-finder.onrender.com";

// ─────────────────────────────────────────────
// FUZZY SEARCH
// Implements a lightweight fuzzy matching algorithm so users can
// find entries even with typos or partial words.
//
// Strategy: combine two signals
//   1. Substring match  — "pay" matches "Payments" (partial search)
//   2. Character sequence match — checks that every character in the
//      search term appears in order within the field value.
//      e.g. "Stipe" matches "Stripe" because S-t-i-p-e all appear
//      in order inside S-t-r-i-p-e.
//
// A field is considered a match if EITHER signal returns true.
// This satisfies the spec requirement for "partial and fuzzy search."
// ─────────────────────────────────────────────

/**
 * fuzzyMatch
 * Returns true if `term` loosely matches `str`.
 *
 * @param {string} str  - The field value to search within (should be lowercased)
 * @param {string} term - The search query (should be lowercased)
 * @returns {boolean}
 */
function fuzzyMatch(str, term) {
  if (!str || !term) return false;

  // Signal 1: direct substring — handles normal partial search
  if (str.includes(term)) return true;

  // Signal 2: character sequence — handles typos and skipped letters
  // Walk through `str` trying to consume every character in `term` in order
  let termIndex = 0;
  for (let i = 0; i < str.length && termIndex < term.length; i++) {
    if (str[i] === term[termIndex]) termIndex++;
  }
  // If we consumed all characters in term, it's a fuzzy match
  return termIndex === term.length;
}

/**
 * fuzzyMatchApi
 * Returns true if the search term fuzzy-matches ANY searchable field of an API entry.
 *
 * @param {object} api  - An ApiEntry object
 * @param {string} term - Lowercased search query
 * @returns {boolean}
 */
function fuzzyMatchApi(api, term) {
  if (!term) return true; // empty search shows everything

  const fields = [
    api.name,
    api.category,
    api.description,
    api.version,
    api.developer,
    api.programming_language,
    api.framework,
    api.cost,
    api.latency,
    api.scalability,
    api.design_pattern,
  ];

  return fields.some((field) => fuzzyMatch((field || "").toLowerCase(), term));
}

// ─────────────────────────────────────────────
// SAMPLE CODE TEMPLATES
// Keyed by programming language (lowercase).
// Each template receives the API name as a parameter.
// Covers the most common languages found in GitHub repos.
// ─────────────────────────────────────────────
const CODE_TEMPLATES = {
  javascript: (name) =>
`// ${name} — JavaScript (fetch)
const response = await fetch('https://api.example.com/v1/endpoint', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  }
});
const data = await response.json();
console.log(data);`,

  typescript: (name) =>
`// ${name} — TypeScript (fetch)
const response = await fetch('https://api.example.com/v1/endpoint', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  }
});
const data: Record<string, unknown> = await response.json();
console.log(data);`,

  python: (name) =>
`# ${name} — Python (requests)
import requests

headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

response = requests.get("https://api.example.com/v1/endpoint", headers=headers)
data = response.json()
print(data)`,

  java: (name) =>
`// ${name} — Java (HttpClient)
import java.net.http.*;
import java.net.URI;

HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/v1/endpoint"))
    .header("Authorization", "Bearer YOUR_API_KEY")
    .GET()
    .build();

HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());
System.out.println(response.body());`,

  go: (name) =>
`// ${name} — Go (net/http)
package main

import (
    "fmt"
    "net/http"
    "io/ioutil"
)

req, _ := http.NewRequest("GET", "https://api.example.com/v1/endpoint", nil)
req.Header.Set("Authorization", "Bearer YOUR_API_KEY")

client := &http.Client{}
resp, _ := client.Do(req)
defer resp.Body.Close()

body, _ := ioutil.ReadAll(resp.Body)
fmt.Println(string(body))`,

  ruby: (name) =>
`# ${name} — Ruby (Net::HTTP)
require 'net/http'
require 'json'

uri = URI('https://api.example.com/v1/endpoint')
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true

request = Net::HTTP::Get.new(uri)
request['Authorization'] = 'Bearer YOUR_API_KEY'

response = http.request(request)
puts JSON.parse(response.body)`,

  php: (name) =>
`<?php
// ${name} — PHP (cURL)
$curl = curl_init();
curl_setopt_array($curl, [
    CURLOPT_URL => "https://api.example.com/v1/endpoint",
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_HTTPHEADER => [
        "Authorization: Bearer YOUR_API_KEY",
        "Content-Type: application/json"
    ],
]);
$response = curl_exec($curl);
curl_close($curl);
echo $response;`,

  rust: (name) =>
`// ${name} — Rust (reqwest)
use reqwest::header::{AUTHORIZATION, CONTENT_TYPE};

let client = reqwest::Client::new();
let response = client
    .get("https://api.example.com/v1/endpoint")
    .header(AUTHORIZATION, "Bearer YOUR_API_KEY")
    .header(CONTENT_TYPE, "application/json")
    .send()
    .await?;

let data = response.text().await?;
println!("{}", data);`,

  "c#": (name) =>
`// ${name} — C# (HttpClient)
using System.Net.Http;
using System.Net.Http.Headers;

var client = new HttpClient();
client.DefaultRequestHeaders.Authorization =
    new AuthenticationHeaderValue("Bearer", "YOUR_API_KEY");

var response = await client.GetAsync("https://api.example.com/v1/endpoint");
var content = await response.Content.ReadAsStringAsync();
Console.WriteLine(content);`,

  kotlin: (name) =>
`// ${name} — Kotlin (OkHttp)
val client = OkHttpClient()
val request = Request.Builder()
    .url("https://api.example.com/v1/endpoint")
    .addHeader("Authorization", "Bearer YOUR_API_KEY")
    .build()

client.newCall(request).execute().use { response ->
    println(response.body?.string())
}`,

  swift: (name) =>
`// ${name} — Swift (URLSession)
var request = URLRequest(url: URL(string: "https://api.example.com/v1/endpoint")!)
request.setValue("Bearer YOUR_API_KEY", forHTTPHeaderField: "Authorization")

URLSession.shared.dataTask(with: request) { data, response, error in
    if let data = data {
        print(String(data: data, encoding: .utf8) ?? "")
    }
}.resume()`,

  // Default fallback for any unrecognized language — uses curl (universal)
  default: (name) =>
`# ${name} — cURL (universal)
curl -X GET "https://api.example.com/v1/endpoint" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json"`,
};

/**
 * generateSampleCode
 * Returns a language-specific code template for the given API name and language.
 *
 * @param {string} name     - API or library name (used in the comment header)
 * @param {string} language - Programming language (matched case-insensitively)
 * @returns {string} - A formatted code snippet string
 */
function generateSampleCode(name, language) {
  const lang = (language || "").toLowerCase().trim();
  const templateFn = CODE_TEMPLATES[lang] || CODE_TEMPLATES["default"];
  return templateFn(name);
}

// ─────────────────────────────────────────────
// HELPER: Tailwind classes for risk badge color
// ─────────────────────────────────────────────
function getRiskBadgeClass(riskLevel) {
  if (riskLevel === "High") return "bg-red-100 text-red-700";
  if (riskLevel === "Medium") return "bg-yellow-100 text-yellow-700";
  return "bg-emerald-100 text-emerald-700";
}

// ─────────────────────────────────────────────
// HELPER: Hex color for risk level (used in charts/compare)
// ─────────────────────────────────────────────
function getRiskColor(risk) {
  if (risk === "High") return "#dc2626";
  if (risk === "Medium") return "#d97706";
  return "#059669";
}

// ─────────────────────────────────────────────
// COMPONENT: ReviewModal
// Shown after a GitHub fetch to let the user fill in
// fields that GitHub doesn't provide, and optionally
// generate a sample code snippet from a language template.
//
// Props:
//   formData        — current form state (pre-filled from GitHub)
//   onUpdate        — callback(field, value) to update a single field
//   onGenerateCode  — callback to auto-fill sample_code from template
//   onConfirm       — callback when user clicks Save / confirm
//   onCancel        — callback when user dismisses the modal
// ─────────────────────────────────────────────
function ReviewModal({ formData, onUpdate, onGenerateCode, onConfirm, onCancel }) {
  // Fields that GitHub cannot provide — these are what the user needs to fill
  const missingFields = [
    { key: "framework", label: "Framework", placeholder: "e.g. REST, GraphQL, gRPC, SDK" },
    { key: "cost", label: "Cost", placeholder: "e.g. Free, Paid/Premium, Freemium, Open Source" },
    { key: "latency", label: "Latency", placeholder: "e.g. Low, Medium, High" },
    { key: "scalability", label: "Scalability", placeholder: "e.g. High, Medium, Low" },
    { key: "design_pattern", label: "Design Pattern", placeholder: "e.g. REST, GraphQL, Event-Driven, Pub/Sub" },
  ];

  return (
    <div
      style={{
        position: "fixed", inset: 0, zIndex: 1000,
        background: "rgba(15,23,42,0.7)",
        backdropFilter: "blur(6px)",
        display: "flex", alignItems: "center", justifyContent: "center",
        padding: "24px 16px", overflowY: "auto",
      }}
    >
      <div style={{
        background: "#fff", borderRadius: 28, width: "100%", maxWidth: 600,
        boxShadow: "0 32px 80px rgba(0,0,0,0.25)", overflow: "hidden",
      }}>
        {/* Modal header */}
        <div style={{
          background: "linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #312e81 100%)",
          padding: "24px 28px",
        }}>
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

        <div style={{ padding: "24px 28px", maxHeight: "70vh", overflowY: "auto" }}>
          {/* Read-only summary of what was fetched */}
          <div style={{
            background: "#f8fafc", borderRadius: 16, padding: "14px 18px",
            marginBottom: 20, border: "1px solid #e2e8f0",
          }}>
            <p style={{ margin: "0 0 8px 0", fontSize: 12, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.08em" }}>
              Fetched from GitHub
            </p>
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

          {/* Fields to fill in manually */}
          <p style={{ margin: "0 0 12px 0", fontSize: 13, fontWeight: 700, color: "#374151" }}>
            Please fill in the missing fields:
          </p>
          <div style={{ display: "flex", flexDirection: "column", gap: 12, marginBottom: 20 }}>
            {missingFields.map((field) => (
              <div key={field.key}>
                <label style={{ display: "block", fontSize: 13, fontWeight: 600, color: "#374151", marginBottom: 6 }}>
                  {field.label}
                </label>
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

          {/* Sample code section with template generator */}
          <div style={{ borderTop: "1px solid #f1f5f9", paddingTop: 16 }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 8 }}>
              <label style={{ fontSize: 13, fontWeight: 700, color: "#374151" }}>
                Sample Code
              </label>
              {/* Generate from template button */}
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
            <p style={{ margin: "0 0 8px 0", fontSize: 11, color: "#94a3b8" }}>
              Language detected: <strong>{formData.programming_language || "Unknown"}</strong> — click Generate to auto-fill a starter snippet, then edit as needed.
            </p>
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

        {/* Action buttons */}
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

// ─────────────────────────────────────────────
// COMPONENT: SimpleBarChart
// Horizontal bar chart using plain divs.
// Props: data — [{ label, value, color }], title — string
// ─────────────────────────────────────────────
function SimpleBarChart({ data, title }) {
  const max = Math.max(...data.map((d) => d.value), 1);
  return (
    <div>
      {title && <p className="mb-4 text-sm font-bold uppercase tracking-wide text-slate-500">{title}</p>}
      <div className="space-y-3">
        {data.map((item) => (
          <div key={item.label}>
            <div className="mb-1 flex items-center justify-between gap-2">
              <span className="truncate text-sm font-medium text-slate-700" style={{ maxWidth: "65%" }}>{item.label}</span>
              <span className="text-sm font-bold text-slate-900">{item.value}</span>
            </div>
            <div className="h-2.5 w-full overflow-hidden rounded-full bg-slate-100">
              <div className="h-full rounded-full transition-all duration-700"
                style={{ width: `${(item.value / max) * 100}%`, background: item.color || "#3b82f6" }} />
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
// Props: segments — [{ label, value, color }], title — string
// ─────────────────────────────────────────────
function DonutChart({ segments, title }) {
  const total = segments.reduce((sum, s) => sum + s.value, 0);
  if (total === 0) return null;

  let cumulative = 0;
  const gradient = `conic-gradient(${segments.map((seg) => {
    const pct = (seg.value / total) * 100;
    const part = `${seg.color} ${cumulative}% ${cumulative + pct}%`;
    cumulative += pct;
    return part;
  }).join(", ")})`;

  return (
    <div>
      {title && <p className="mb-4 text-sm font-bold uppercase tracking-wide text-slate-500">{title}</p>}
      <div className="flex flex-col items-center gap-6 sm:flex-row sm:items-start">
        <div className="relative flex-shrink-0">
          <div style={{ width: 140, height: 140, borderRadius: "50%", background: gradient }} />
          <div style={{
            position: "absolute", top: "50%", left: "50%",
            transform: "translate(-50%, -50%)",
            width: 80, height: 80, borderRadius: "50%", background: "white",
            display: "flex", alignItems: "center", justifyContent: "center",
          }}>
            <span className="text-lg font-black text-slate-800">{total}</span>
          </div>
        </div>
        <div className="flex flex-col gap-2">
          {segments.map((seg) => (
            <div key={seg.label} className="flex items-center gap-2">
              <div className="h-3 w-3 flex-shrink-0 rounded-full" style={{ background: seg.color }} />
              <span className="text-sm text-slate-700">
                {seg.label} <span className="font-bold text-slate-900">{seg.value}</span>{" "}
                <span className="text-slate-400">({Math.round((seg.value / total) * 100)}%)</span>
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// COMPONENT: StatCard — single KPI tile
// ─────────────────────────────────────────────
function StatCard({ label, value, color, icon }) {
  return (
    <div className="rounded-2xl border p-5 shadow-sm"
      style={{ borderColor: color + "33", background: color + "0d" }}>
      <div className="flex items-start justify-between gap-2">
        <div>
          <p className="text-xs font-bold uppercase tracking-wide" style={{ color }}>{label}</p>
          <p className="mt-2 text-3xl font-black text-slate-900">{value}</p>
        </div>
        <span className="text-2xl">{icon}</span>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// COMPONENT: StatsTab
// Full analytics dashboard computed from the API list.
// Props: apis — full array of API entry objects
// ─────────────────────────────────────────────
function StatsTab({ apis }) {
  // ── Filter state — user can narrow stats by developer or category ──
  const [filterDeveloper, setFilterDeveloper] = useState("All");
  const [filterCategory, setFilterCategory] = useState("All");

  // Unique sorted lists for the filter dropdowns
  const allDevelopers = useMemo(() =>
    ["All", ...[...new Set(apis.map((a) => a.developer?.trim()).filter(Boolean))].sort()],
    [apis]
  );
  const allCategories = useMemo(() =>
    ["All", ...[...new Set(apis.map((a) => a.category?.trim()).filter(Boolean))].sort()],
    [apis]
  );

  // Apply developer + category filters to the full API list
  // All charts and KPIs below use this filtered subset
  const filteredData = useMemo(() => apis.filter((a) => {
    const matchDev = filterDeveloper === "All" || a.developer?.trim() === filterDeveloper;
    const matchCat = filterCategory === "All" || a.category?.trim() === filterCategory;
    return matchDev && matchCat;
  }), [apis, filterDeveloper, filterCategory]);

  const isFiltered = filterDeveloper !== "All" || filterCategory !== "All";

  // ── Chart data — all computed from filteredData ──

  const categoryCounts = useMemo(() => {
    const map = {};
    filteredData.forEach((a) => { const cat = a.category?.trim() || "Unknown"; map[cat] = (map[cat] || 0) + 1; });
    return Object.entries(map).sort((a, b) => b[1] - a[1])
      .map(([label, value], i) => ({ label, value, color: ["#3b82f6","#6366f1","#8b5cf6","#ec4899","#f59e0b","#10b981","#ef4444","#06b6d4","#f97316","#84cc16"][i % 10] }));
  }, [filteredData]);

  const developerCounts = useMemo(() => {
    const map = {};
    filteredData.forEach((a) => { const dev = a.developer?.trim() || "Unknown"; map[dev] = (map[dev] || 0) + 1; });
    return Object.entries(map).sort((a, b) => b[1] - a[1]).slice(0, 10)
      .map(([label, value], i) => ({ label, value, color: ["#6366f1","#8b5cf6","#a78bfa","#c4b5fd","#ddd6fe","#3b82f6","#60a5fa","#93c5fd","#bfdbfe","#e0f2fe"][i % 10] }));
  }, [filteredData]);

  const riskCounts = useMemo(() => {
    const map = { Low: 0, Medium: 0, High: 0 };
    filteredData.forEach((a) => { const r = a.risk_level || "Medium"; map[r] = (map[r] || 0) + 1; });
    return [
      { label: "Low", value: map.Low, color: "#10b981" },
      { label: "Medium", value: map.Medium, color: "#f59e0b" },
      { label: "High", value: map.High, color: "#ef4444" },
    ].filter((s) => s.value > 0);
  }, [filteredData]);

  const languageCounts = useMemo(() => {
    const map = {};
    filteredData.forEach((a) => { const lang = a.programming_language?.trim() || "Unknown"; map[lang] = (map[lang] || 0) + 1; });
    return Object.entries(map).sort((a, b) => b[1] - a[1]).slice(0, 8)
      .map(([label, value], i) => ({ label, value, color: ["#10b981","#14b8a6","#06b6d4","#0ea5e9","#3b82f6","#6366f1","#8b5cf6","#ec4899"][i % 8] }));
  }, [filteredData]);

  const costCounts = useMemo(() => {
    const map = {};
    filteredData.forEach((a) => { const cost = a.cost?.trim() || "Unknown"; map[cost] = (map[cost] || 0) + 1; });
    return Object.entries(map).sort((a, b) => b[1] - a[1]).slice(0, 6)
      .map(([label, value], i) => ({ label, value, color: ["#f59e0b","#10b981","#3b82f6","#8b5cf6","#ef4444","#94a3b8"][i % 6] }));
  }, [filteredData]);

  const patternCounts = useMemo(() => {
    const map = {};
    filteredData.forEach((a) => { const p = a.design_pattern?.trim() || "Unknown"; map[p] = (map[p] || 0) + 1; });
    return Object.entries(map).sort((a, b) => b[1] - a[1]).slice(0, 6)
      .map(([label, value], i) => ({ label, value, color: ["#f97316","#eab308","#84cc16","#06b6d4","#a855f7","#ec4899"][i % 6] }));
  }, [filteredData]);

  const scalabilityCounts = useMemo(() => {
    const map = {};
    filteredData.forEach((a) => { const s = a.scalability?.trim() || "Unknown"; map[s] = (map[s] || 0) + 1; });
    return Object.entries(map).sort((a, b) => b[1] - a[1])
      .map(([label, value], i) => ({ label, value, color: ["#10b981","#3b82f6","#f59e0b","#ef4444","#8b5cf6","#94a3b8"][i % 6] }));
  }, [filteredData]);

  const topDevelopers = developerCounts.slice(0, 5);

  // KPI tiles — reflect the filtered subset
  const totalApis = filteredData.length;
  const uniqueCategories = new Set(filteredData.map((a) => a.category?.trim()).filter(Boolean)).size;
  const uniqueDevelopers = new Set(filteredData.map((a) => a.developer?.trim()).filter(Boolean)).size;
  const lowRiskCount = filteredData.filter((a) => (a.risk_level || "Medium") === "Low").length;

  return (
    <div className="space-y-8">

      {/* ── Stats Filter Bar ── */}
      <div className="rounded-[24px] border border-slate-200 bg-white p-5 shadow-sm">
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="text-sm font-bold text-slate-600">🔍 Filter Stats By:</span>
          </div>

          {/* Developer filter */}
          <div className="flex items-center gap-2">
            <label className="text-xs font-semibold uppercase tracking-wide text-slate-400">Developer</label>
            <select
              value={filterDeveloper}
              onChange={(e) => setFilterDeveloper(e.target.value)}
              className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm font-medium text-slate-700 outline-none transition focus:border-blue-400 focus:ring-2 focus:ring-blue-100"
            >
              {allDevelopers.map((d) => <option key={d} value={d}>{d}</option>)}
            </select>
          </div>

          {/* Category filter */}
          <div className="flex items-center gap-2">
            <label className="text-xs font-semibold uppercase tracking-wide text-slate-400">Category</label>
            <select
              value={filterCategory}
              onChange={(e) => setFilterCategory(e.target.value)}
              className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm font-medium text-slate-700 outline-none transition focus:border-blue-400 focus:ring-2 focus:ring-blue-100"
            >
              {allCategories.map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>

          {/* Reset button — only shown when a filter is active */}
          {isFiltered && (
            <button
              onClick={() => { setFilterDeveloper("All"); setFilterCategory("All"); }}
              className="rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs font-semibold text-slate-500 transition hover:bg-slate-100"
            >
              Reset
            </button>
          )}

          {/* Active filter label */}
          {isFiltered && (
            <span className="rounded-full bg-blue-100 px-3 py-1 text-xs font-bold text-blue-700">
              Showing {filteredData.length} of {apis.length} APIs
            </span>
          )}
        </div>
      </div>

      {/* KPI tiles */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard label={isFiltered ? "Filtered APIs" : "Total APIs"} value={totalApis} color="#3b82f6" icon="📦" />
        <StatCard label="Categories" value={uniqueCategories} color="#8b5cf6" icon="🗂️" />
        <StatCard label="Developers" value={uniqueDevelopers} color="#10b981" icon="👩‍💻" />
        <StatCard label="Low Risk" value={lowRiskCount} color="#059669" icon="✅" />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-[24px] border border-slate-200 bg-white p-6 shadow-sm">
          <SimpleBarChart data={categoryCounts} title="APIs by Category" />
        </div>
        <div className="rounded-[24px] border border-slate-200 bg-white p-6 shadow-sm">
          <DonutChart segments={riskCounts} title="Risk Level Distribution" />
        </div>
      </div>
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-[24px] border border-slate-200 bg-white p-6 shadow-sm">
          <SimpleBarChart data={developerCounts} title="Top Developers by API Count" />
        </div>
        <div className="rounded-[24px] border border-slate-200 bg-white p-6 shadow-sm">
          <SimpleBarChart data={languageCounts} title="Programming Languages" />
        </div>
      </div>
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-[24px] border border-slate-200 bg-white p-6 shadow-sm">
          <DonutChart segments={costCounts} title="Cost Model Breakdown" />
        </div>
        <div className="rounded-[24px] border border-slate-200 bg-white p-6 shadow-sm">
          <SimpleBarChart data={patternCounts} title="Design Patterns" />
        </div>
      </div>
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-[24px] border border-slate-200 bg-white p-6 shadow-sm">
          <DonutChart segments={scalabilityCounts.slice(0, 5).map((s, i) => ({
            ...s, color: ["#10b981","#3b82f6","#f59e0b","#ef4444","#94a3b8"][i],
          }))} title="Scalability Distribution" />
        </div>
        <div className="rounded-[24px] border border-slate-200 bg-white p-6 shadow-sm">
          <p className="mb-4 text-sm font-bold uppercase tracking-wide text-slate-500">Developer Leaderboard</p>
          <div className="space-y-3">
            {topDevelopers.map((dev, idx) => (
              <div key={dev.label} className="flex items-center gap-4 rounded-2xl border border-slate-100 bg-slate-50 px-4 py-3">
                <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full text-sm font-black text-white"
                  style={{ background: idx === 0 ? "#f59e0b" : idx === 1 ? "#94a3b8" : idx === 2 ? "#b45309" : "#6366f1" }}>
                  {idx + 1}
                </div>
                <div className="min-w-0 flex-1">
                  <p className="truncate font-semibold text-slate-800">{dev.label}</p>
                </div>
                <span className="rounded-full bg-blue-100 px-3 py-1 text-sm font-bold text-blue-700">
                  {dev.value} API{dev.value !== 1 ? "s" : ""}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// COMPONENT: CompareModal
// Full-screen overlay showing selected APIs side by side.
// Props: apis — [ApiEntry], onClose — callback
// ─────────────────────────────────────────────
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

  const colWidth = apis.length === 2 ? "1fr 1fr" : apis.length === 3 ? "1fr 1fr 1fr" : "1fr 1fr 1fr 1fr";
  const diffColors = [
    { bg: "#fffbeb", border: "#fde68a" },
    { bg: "#f0fdf4", border: "#bbf7d0" },
    { bg: "#eff6ff", border: "#bfdbfe" },
    { bg: "#fdf4ff", border: "#e9d5ff" },
  ];

  return (
    <div style={{
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
          <button onClick={onClose} style={{
            background: "rgba(255,255,255,0.1)", border: "1px solid rgba(255,255,255,0.2)",
            color: "#fff", borderRadius: 12, width: 40, height: 40,
            fontSize: 20, cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center",
          }}>×</button>
        </div>
        <div style={{ padding: "0 32px 32px 32px", overflowX: "auto" }}>
          <div style={{
            display: "grid", gridTemplateColumns: `180px ${colWidth}`,
            gap: 16, paddingTop: 28, paddingBottom: 20,
            borderBottom: "2px solid #f1f5f9", marginBottom: 8,
          }}>
            <div />
            {apis.map((api) => (
              <div key={api.id} style={{ background: "linear-gradient(135deg, #eff6ff, #eef2ff)", borderRadius: 20, padding: "18px 20px", border: "1px solid #bfdbfe" }}>
                <h3 style={{ margin: "0 0 8px 0", fontSize: 17, fontWeight: 800, color: "#1e293b" }}>{api.name}</h3>
                <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                  <span style={{ background: "#dbeafe", color: "#1d4ed8", borderRadius: 20, padding: "3px 10px", fontSize: 11, fontWeight: 600 }}>{api.category}</span>
                  <span style={{ background: api.risk_level === "High" ? "#fee2e2" : api.risk_level === "Medium" ? "#fef3c7" : "#d1fae5", color: getRiskColor(api.risk_level), borderRadius: 20, padding: "3px 10px", fontSize: 11, fontWeight: 600 }}>{api.risk_level || "Medium"} Risk</span>
                </div>
              </div>
            ))}
          </div>
          <div style={{ display: "grid", gridTemplateColumns: `180px ${colWidth}`, gap: 16, padding: "16px 0", borderBottom: "1px solid #f1f5f9" }}>
            <div style={{ display: "flex", alignItems: "center" }}>
              <span style={{ fontSize: 12, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.08em" }}>Description</span>
            </div>
            {apis.map((api) => (
              <p key={api.id} style={{ margin: 0, fontSize: 13, color: "#475569", lineHeight: 1.6 }}>{api.description || "—"}</p>
            ))}
          </div>
          {fields.map((field, i) => {
            const values = apis.map((a) => a[field.key] || "—");
            const allSame = values.every((v) => v === values[0]);
            return (
              <div key={field.key} style={{
                display: "grid", gridTemplateColumns: `180px ${colWidth}`,
                gap: 16, padding: "14px 0", borderBottom: "1px solid #f8fafc",
                background: i % 2 === 0 ? "transparent" : "#fafbff", borderRadius: 8,
              }}>
                <div style={{ display: "flex", alignItems: "center" }}>
                  <span style={{ fontSize: 12, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.08em" }}>{field.label}</span>
                </div>
                {apis.map((api, idx) => {
                  const val = api[field.key] || "—";
                  return (
                    <div key={api.id} style={{ padding: "6px 12px", background: !allSame ? diffColors[idx % 4].bg : "transparent", borderRadius: 10, border: !allSame ? `1px solid ${diffColors[idx % 4].border}` : "none" }}>
                      {field.key === "risk_level"
                        ? <span style={{ color: getRiskColor(val), fontWeight: 700, fontSize: 13 }}>{val}</span>
                        : <span style={{ fontSize: 13, fontWeight: 600, color: val === "—" ? "#cbd5e1" : "#1e293b" }}>{val}</span>
                      }
                    </div>
                  );
                })}
              </div>
            );
          })}
          {apis.some((a) => a.sample_code) && (
            <div style={{ display: "grid", gridTemplateColumns: `180px ${colWidth}`, gap: 16, padding: "20px 0 8px 0", borderTop: "2px solid #f1f5f9", marginTop: 8 }}>
              <div style={{ display: "flex", alignItems: "flex-start", paddingTop: 8 }}>
                <span style={{ fontSize: 12, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.08em" }}>Sample Code</span>
              </div>
              {apis.map((api) => (
                <div key={api.id}>
                  {api.sample_code
                    ? <pre style={{ margin: 0, padding: "14px 16px", background: "#0f172a", color: "#e2e8f0", borderRadius: 14, fontSize: 11, lineHeight: 1.6, overflowX: "auto", whiteSpace: "pre-wrap", wordBreak: "break-all", maxHeight: 160 }}>{api.sample_code}</pre>
                    : <span style={{ fontSize: 13, color: "#cbd5e1" }}>—</span>
                  }
                </div>
              ))}
            </div>
          )}
          <div style={{ marginTop: 24, padding: "14px 20px", background: "#f8fafc", borderRadius: 16 }}>
            <span style={{ fontSize: 12, color: "#94a3b8", fontWeight: 600 }}>💡 Highlighted cells indicate differences between entries</span>
          </div>
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// COMPONENT: App (root)
// Manages all global state and renders the full page.
// Tabs: "directory" | "stats"
// ─────────────────────────────────────────────
function App() {
  // ── Core state ──────────────────────────────
  const [apis, setApis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [editId, setEditId] = useState(null);
  const [githubRepo, setGithubRepo] = useState("");
  const [fetchingGithub, setFetchingGithub] = useState(false);
  const [activeTab, setActiveTab] = useState("directory");

  // Compare state
  const [compareIds, setCompareIds] = useState([]);
  const [showCompare, setShowCompare] = useState(false);
  const [showCompareLimit, setShowCompareLimit] = useState(false); // toast shown when user tries to select a 5th API
  const [sortBy, setSortBy] = useState("default");   // sort order for API cards
  const [copiedId, setCopiedId] = useState(null);     // id of card whose link was just copied
  const [currentPage, setCurrentPage] = useState(1);  // current pagination page
  const ITEMS_PER_PAGE = 12;                           // cards shown per page

  // Review modal state — shown after GitHub fetch
  const [showReview, setShowReview] = useState(false);
  const [showDrawer, setShowDrawer] = useState(false);  // slide-in form drawer
  const [expandedId, setExpandedId] = useState(null);   // expanded card id for details toggle

  // Form fields (controlled inputs)
  const [formData, setFormData] = useState({
    name: "", category: "", description: "", version: "", developer: "",
    programming_language: "", framework: "", cost: "", latency: "",
    scalability: "", design_pattern: "", sample_code: "",
  });

  // ── Data fetching ────────────────────────────

  /** Load all API entries from the backend */
  const fetchApis = () => {
    setLoading(true);
    setError("");
    fetch(`${API_BASE}/api/apis`)
      .then((res) => { if (!res.ok) throw new Error("Failed to fetch APIs"); return res.json(); })
      .then((data) => { setApis(data); setLoading(false); })
      .catch((err) => { setError(err.message); setLoading(false); });
  };

  useEffect(() => { fetchApis(); }, []);

  // Auto-clear success messages after 2.5 seconds
  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => setSuccessMessage(""), 2500);
      return () => clearTimeout(timer);
    }
  }, [successMessage]);

  // ── Form handlers ────────────────────────────

  /** Update a single form field */
  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  /** Update a field by key (used by ReviewModal) */
  const handleReviewUpdate = (key, value) => setFormData((prev) => ({ ...prev, [key]: value }));

  /** Reset form to empty state and exit edit mode */
  const resetForm = () => {
    setFormData({
      name: "", category: "", description: "", version: "", developer: "",
      programming_language: "", framework: "", cost: "", latency: "",
      scalability: "", design_pattern: "", sample_code: "",
    });
    setGithubRepo("");
    setEditId(null);
    setShowDrawer(false);
  };

  /** Generate sample code from template and inject into formData */
  const handleGenerateCode = () => {
    const code = generateSampleCode(formData.name, formData.programming_language);
    setFormData((prev) => ({ ...prev, sample_code: code }));
  };

  /** Submit form: POST (add) or PUT (edit) */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(""); setSuccessMessage(""); setSubmitting(true);
    try {
      const url = editId ? `${API_BASE}/api/apis/${editId}` : `${API_BASE}/api/apis`;
      const method = editId ? "PUT" : "POST";

      // Client-side duplicate check
      if (!editId) {
        const alreadyExists = apis.some(
          (api) => api.name?.toLowerCase() === formData.name.toLowerCase() &&
                   api.developer?.toLowerCase() === formData.developer.toLowerCase()
        );
        if (alreadyExists) { setError("This API entry already exists."); setSubmitting(false); return; }
      }

      const res = await fetch(url, {
        method, headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || (editId ? "Failed to update API" : "Failed to add API"));

      setSuccessMessage(editId ? "API updated successfully." : "API added successfully.");
      resetForm();
      fetchApis();
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  /**
   * GitHub fetch — fills form with available data,
   * then opens the ReviewModal for the user to fill missing fields.
   */
  const handleGithubFetch = async () => {
    if (!githubRepo.trim()) { setError("Please enter a GitHub repository in owner/repo format."); return; }
    setError(""); setSuccessMessage(""); setFetchingGithub(true);
    try {
      const res = await fetch(`${API_BASE}/api/github-fetch`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repo: githubRepo }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed to fetch GitHub repository data");

      // Pre-fill form with whatever GitHub gave us
      setFormData({
        name: data.name || "", category: data.category || "",
        description: data.description || "", version: data.version || "",
        developer: data.developer || "", programming_language: data.programming_language || "",
        framework: "", cost: "", latency: "", scalability: "",
        design_pattern: "", sample_code: "",
      });

      // Open review modal so user fills in the missing fields
      setShowReview(true);
      setSuccessMessage("GitHub data fetched — please fill in the missing fields.");
    } catch (err) {
      setError(err.message);
    } finally {
      setFetchingGithub(false);
    }
  };

  /**
   * Called when user clicks "Save Entry" in the ReviewModal.
   * Saves the completed form data to the backend.
   */
  const handleReviewConfirm = async () => {
    setShowReview(false);
    setError(""); setSuccessMessage(""); setSubmitting(true);
    try {
      const alreadyExists = apis.some(
        (api) => api.name?.toLowerCase() === formData.name.toLowerCase() &&
                 api.developer?.toLowerCase() === formData.developer.toLowerCase()
      );
      if (alreadyExists) { setError("This API entry already exists."); setSubmitting(false); return; }

      const res = await fetch(`${API_BASE}/api/apis`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed to save API");

      setSuccessMessage("API saved successfully.");
      resetForm();
      fetchApis();
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  /** Delete an entry after confirmation */
  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this API?")) return;
    setError(""); setSuccessMessage("");
    try {
      const res = await fetch(`${API_BASE}/api/apis/${id}`, { method: "DELETE" });
      if (!res.ok) throw new Error("Failed to delete API");
      setSuccessMessage("API deleted successfully.");
      setCompareIds((prev) => prev.filter((cid) => cid !== id));
      fetchApis();
    } catch (err) {
      setError(err.message);
    }
  };

  /** Populate form with existing entry data for editing */
  const handleEdit = (api) => {
    setFormData({
      name: api.name || "", category: api.category || "", description: api.description || "",
      version: api.version || "", developer: api.developer || "",
      programming_language: api.programming_language || "", framework: api.framework || "",
      cost: api.cost || "", latency: api.latency || "", scalability: api.scalability || "",
      design_pattern: api.design_pattern || "", sample_code: api.sample_code || "",
    });
    setEditId(api.id);
    setSuccessMessage(""); setError("");
    setShowDrawer(true);   // open the slide-in drawer instead of scrolling
    setActiveTab("directory");
  };

  // ── Compare handlers ─────────────────────────

  /** Toggle an API in/out of compare selection (max 4) */
  const toggleCompare = (id) => {
    setCompareIds((prev) => {
      if (prev.includes(id)) return prev.filter((cid) => cid !== id);
      if (prev.length >= 4) {
        // Show a brief toast explaining the 4-item limit
        setShowCompareLimit(true);
        setTimeout(() => setShowCompareLimit(false), 2500);
        return prev;
      }
      return [...prev, id];
    });
  };

  // ── Export to CSV ────────────────────────────
  /**
   * exportToCSV
   * Converts the currently filtered API list to a CSV file and triggers a download.
   * Uses the browser's Blob + anchor click pattern — no library needed.
   */
  const exportToCSV = () => {
    const headers = ["Name","Category","Version","Developer","Language","Framework","Cost","Latency","Scalability","Design Pattern","Risk Level","Description","Sample Code"];
    const rows = filteredApis.map((api) => [
      api.name, api.category, api.version, api.developer,
      api.programming_language, api.framework, api.cost,
      api.latency, api.scalability, api.design_pattern,
      api.risk_level, api.description,
      (api.sample_code || "").replace(/\n/g, " "),
    ].map((v) => `"${(v || "").replace(/"/g, '""')}"`));

    const csv = [headers.join(","), ...rows.map((r) => r.join(","))].join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `slib-directory-${new Date().toISOString().slice(0,10)}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // ── Shareable card link ───────────────────────
  /**
   * copyShareLink
   * Copies a deep-link URL for a specific API card to the clipboard.
   * Uses the api id as a hash so the link is bookmarkable.
   * Shows a brief "Copied!" confirmation on the card.
   */
  const copyShareLink = (id) => {
    const url = `${window.location.origin}${window.location.pathname}#api-${id}`;
    navigator.clipboard.writeText(url).then(() => {
      setCopiedId(id);
      setTimeout(() => setCopiedId(null), 2000);
    });
  };

  const compareApis = useMemo(() => apis.filter((a) => compareIds.includes(a.id)), [apis, compareIds]);

  // ── Derived UI data ──────────────────────────

  const categories = useMemo(() => {
    const unique = [...new Set(apis.map((api) => api.category?.trim()).filter(Boolean))].sort();
    return ["All", ...unique];
  }, [apis]);

  const filteredApis = useMemo(() => {
    const term = searchTerm.toLowerCase().trim();
    return apis.filter((api) => {
      // Use fuzzy matching — handles typos, partial words, and character sequences
      const matchesSearch = fuzzyMatchApi(api, term);
      const matchesCategory = selectedCategory === "All" || api.category === selectedCategory;
      return matchesSearch && matchesCategory;
    });
  }, [apis, searchTerm, selectedCategory]);

  // Sort the filtered list based on the current sortBy selection
  const sortedFilteredApis = useMemo(() => {
    const list = [...filteredApis];
    if (sortBy === "name-asc")   return list.sort((a, b) => (a.name || "").localeCompare(b.name || ""));
    if (sortBy === "name-desc")  return list.sort((a, b) => (b.name || "").localeCompare(a.name || ""));
    if (sortBy === "risk-high")  return list.sort((a, b) => ["High","Medium","Low"].indexOf(a.risk_level) - ["High","Medium","Low"].indexOf(b.risk_level));
    if (sortBy === "risk-low")   return list.sort((a, b) => ["Low","Medium","High"].indexOf(a.risk_level) - ["Low","Medium","High"].indexOf(b.risk_level));
    if (sortBy === "category")   return list.sort((a, b) => (a.category || "").localeCompare(b.category || ""));
    if (sortBy === "developer")  return list.sort((a, b) => (a.developer || "").localeCompare(b.developer || ""));
    return list; // "default" = original DB order
  }, [filteredApis, sortBy]);

  // Reset to page 1 whenever search, category or sort changes
  useEffect(() => { setCurrentPage(1); }, [searchTerm, selectedCategory, sortBy]);

  // Paginate the sorted+filtered list
  const totalPages = Math.ceil(sortedFilteredApis.length / ITEMS_PER_PAGE);
  const paginatedApis = sortedFilteredApis.slice(
    (currentPage - 1) * ITEMS_PER_PAGE,
    currentPage * ITEMS_PER_PAGE
  );

  const totalApis = apis.length;
  const totalCategories = Math.max(categories.length - 1, 0);
  const uniqueDevelopers = new Set(apis.map((api) => api.developer?.trim()).filter(Boolean)).size;

  // ── Render ───────────────────────────────────
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 px-4 py-8 md:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">

        {/* ── Page Header ── */}
        <div className="mb-8 overflow-hidden rounded-[28px] border border-white/60 bg-white/80 shadow-xl backdrop-blur">
          <div className="bg-gradient-to-r from-slate-900 via-blue-900 to-indigo-900 px-6 py-8 text-white md:px-8 md:py-10">
            <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
              <div className="max-w-3xl">
                <span className="inline-flex rounded-full border border-white/20 bg-white/10 px-4 py-1 text-sm font-medium text-blue-100">
                  SLIB Finder : API / Microservices
                </span>
                <h1 className="mt-4 text-4xl font-black tracking-tight md:text-5xl">
                  API & Microservices Directory Dashboard
                </h1>
                <p className="mt-3 max-w-2xl text-sm text-slate-200 md:text-base">
                  Discover, manage, and analyze APIs and microservices in a centralized directory
                </p>
              </div>
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-3 lg:min-w-[420px]">
                <div className="rounded-2xl border border-white/15 bg-white/10 p-4">
                  <p className="text-xs uppercase tracking-wide text-slate-300">Total APIs</p>
                  <p className="mt-2 text-2xl font-bold">{totalApis}</p>
                </div>
                <div className="rounded-2xl border border-white/15 bg-white/10 p-4">
                  <p className="text-xs uppercase tracking-wide text-slate-300">Categories</p>
                  <p className="mt-2 text-2xl font-bold">{totalCategories}</p>
                </div>
                <div className="rounded-2xl border border-white/15 bg-white/10 p-4">
                  <p className="text-xs uppercase tracking-wide text-slate-300">Developers</p>
                  <p className="mt-2 text-2xl font-bold">{uniqueDevelopers}</p>
                </div>
              </div>
            </div>

            {/* Tab navigation */}
            <div className="mt-6 flex gap-2">
              {["directory", "stats"].map((tab) => (
                <button key={tab} onClick={() => setActiveTab(tab)}
                  className="rounded-2xl px-5 py-2.5 text-sm font-bold transition"
                  style={{
                    background: activeTab === tab ? "rgba(255,255,255,0.95)" : "rgba(255,255,255,0.1)",
                    color: activeTab === tab ? "#1e3a5f" : "rgba(255,255,255,0.8)",
                    border: activeTab === tab ? "none" : "1px solid rgba(255,255,255,0.2)",
                  }}>
                  {tab === "directory" ? "📋 Directory" : "📊 Stats Dashboard"}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Global alerts */}
        {successMessage && (
          <div className="mb-6 rounded-2xl border border-emerald-200 bg-emerald-50 px-5 py-4 text-emerald-700 shadow-sm">
            <span className="font-medium">Success:</span> {successMessage}
          </div>
        )}
        {error && (
          <div className="mb-6 rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-red-700 shadow-sm">
            <span className="font-medium">Error:</span> {error}
          </div>
        )}

        {/* Stats tab */}
        {activeTab === "stats" && <StatsTab apis={apis} />}

        {/* Directory tab */}
        {activeTab === "directory" && (
          <>
            {/* Compare toolbar */}
            {compareIds.length > 0 && (
              <div className="mb-6 flex flex-wrap items-center justify-between gap-4 rounded-[20px] border border-blue-200 bg-blue-50 px-5 py-4 shadow-sm">
                <div className="flex flex-wrap items-center gap-3">
                  <span className="rounded-full bg-blue-600 px-3 py-1 text-xs font-bold text-white">{compareIds.length} selected</span>
                  <span className={`text-sm font-medium ${compareIds.length >= 4 ? "text-red-600 font-bold" : "text-blue-800"}`}>
                    {compareIds.length < 2 ? `Select ${2 - compareIds.length} more to compare`
                      : compareIds.length < 4 ? `Ready — or add up to ${4 - compareIds.length} more`
                      : "⛔ Maximum 4 APIs selected — remove one to add another"}
                  </span>
                  <div className="flex flex-wrap gap-2">
                    {compareApis.map((a) => (
                      <span key={a.id} className="inline-flex items-center gap-1.5 rounded-full bg-white border border-blue-200 px-3 py-1 text-xs font-semibold text-blue-700 shadow-sm">
                        {a.name}
                        <button onClick={() => toggleCompare(a.id)} style={{ fontSize: 14, lineHeight: 1 }} className="text-blue-400 hover:text-blue-700">×</button>
                      </span>
                    ))}
                  </div>
                </div>
                <div className="flex gap-3">
                  {compareIds.length >= 2 && (
                    <button onClick={() => setShowCompare(true)}
                      className="rounded-2xl bg-blue-600 px-5 py-2.5 text-sm font-bold text-white shadow-md transition hover:bg-blue-700">
                      ⚖️ Compare Now
                    </button>
                  )}
                  <button onClick={() => setCompareIds([])}
                    className="rounded-2xl border border-blue-300 bg-white px-4 py-2.5 text-sm font-semibold text-blue-700 transition hover:bg-blue-50">
                    Clear
                  </button>
                </div>
              </div>
            )}

            {/* ── ADD API floating button ── */}
            <div className="mb-4 flex justify-end">
              <button
                onClick={() => { resetForm(); setShowDrawer(true); }}
                className="rounded-2xl bg-blue-600 px-5 py-2.5 text-sm font-bold text-white shadow-md transition hover:bg-blue-700 hover:shadow-lg"
              >
                + Add New API
              </button>
            </div>

            {/* ── Search & Filter ── */}
            <div className="mb-4 rounded-[24px] border border-slate-200/80 bg-white p-4 shadow-sm">
              <div className="flex flex-wrap items-center gap-3">
                <input type="text"
                  placeholder="Fuzzy search — try typos like 'Stipe', 'pythn'..."
                  value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)}
                  className="min-w-0 flex-1 rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-sm text-slate-800 outline-none transition focus:border-blue-400 focus:bg-white focus:ring-2 focus:ring-blue-100" />
                <select value={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)}
                  className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-700 outline-none transition">
                  <option value="All">All Categories</option>
                  {categories.filter((c) => c !== "All").map((c) => <option key={c} value={c}>{c}</option>)}
                </select>
                <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}
                  className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-700 outline-none transition">
                  <option value="default">Sort: Default</option>
                  <option value="name-asc">Name A → Z</option>
                  <option value="name-desc">Name Z → A</option>
                  <option value="category">Category</option>
                  <option value="developer">Developer</option>
                  <option value="risk-low">Risk: Low first</option>
                  <option value="risk-high">Risk: High first</option>
                </select>
                <button onClick={() => { setSearchTerm(""); setSelectedCategory("All"); setSortBy("default"); }}
                  className="rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm font-semibold text-slate-500 transition hover:bg-slate-50">
                  Reset
                </button>
                <button onClick={exportToCSV}
                  className="rounded-xl border border-emerald-200 bg-emerald-50 px-3 py-2.5 text-xs font-bold text-emerald-700 transition hover:bg-emerald-100">
                  ⬇ CSV
                </button>
                <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-500">
                  {sortedFilteredApis.length} result{sortedFilteredApis.length !== 1 ? "s" : ""}
                </span>
              </div>
              {/* Fuzzy hint chips */}
              <div className="mt-2 flex flex-wrap items-center gap-1.5">
                <span className="text-xs text-slate-400">Try:</span>
                {["Stipe","pythn","paymnt","mcroservice","REST"].map((hint) => (
                  <button key={hint} onClick={() => setSearchTerm(hint)}
                    className="rounded-full border border-slate-200 bg-slate-50 px-2.5 py-0.5 text-xs text-slate-500 transition hover:border-blue-300 hover:text-blue-600">
                    {hint}
                  </button>
                ))}
                <span className="text-xs text-slate-300">— fuzzy search handles typos</span>
              </div>
            </div>

            {/* ── Cards header ── */}
            <div className="mb-3 flex items-center justify-between">
              <h2 className="text-lg font-bold text-slate-800">Available APIs</h2>
              <p className="text-xs text-slate-400">Check boxes to compare</p>
            </div>

            {/* Loading skeleton */}
            {loading && (
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {[1,2,3,4,5,6].map((i) => (
                  <div key={i} className="animate-pulse rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
                    <div className="mb-3 h-5 w-2/3 rounded bg-slate-200" />
                    <div className="mb-4 h-4 w-24 rounded-full bg-slate-200" />
                    <div className="space-y-2">
                      <div className="h-3 w-full rounded bg-slate-200" />
                      <div className="h-3 w-4/5 rounded bg-slate-200" />
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Empty state */}
            {!loading && sortedFilteredApis.length === 0 && (
              <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-12 text-center shadow-sm">
                <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-slate-100 text-2xl">🔎</div>
                <h3 className="mt-3 text-lg font-semibold text-slate-800">No APIs found</h3>
                <p className="mt-1 text-sm text-slate-500">Try a different search term or add a new entry.</p>
              </div>
            )}

            {/* ── Compact API cards — 3 col grid ── */}
            {!loading && sortedFilteredApis.length > 0 && (
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {paginatedApis.map((api) => {
                  const isSelected = compareIds.includes(api.id);
                  const isDisabled = !isSelected && compareIds.length >= 4;
                  const isExpanded = expandedId === api.id;
                  const optionalFields = [api.programming_language, api.framework, api.cost, api.latency, api.scalability, api.design_pattern, api.sample_code];
                  const missingCount = optionalFields.filter((v) => !v || v === "Unknown" || v === "N/A").length;

                  return (
                    <div key={api.id} id={`api-${api.id}`}
                      className="rounded-2xl border bg-white shadow-sm transition duration-200 hover:shadow-md"
                      style={{
                        borderColor: isSelected ? "#3b82f6" : isDisabled ? "#e2e8f0" : "#e2e8f0",
                        boxShadow: isSelected ? "0 0 0 2px rgba(59,130,246,0.2)" : undefined,
                        position: "relative",
                        opacity: isDisabled ? 0.6 : 1,
                      }}>

                      {/* ── Disabled overlay — shown when 4 APIs already selected ── */}
                      {isDisabled && (
                        <div style={{
                          position: "absolute", inset: 0, zIndex: 10,
                          borderRadius: 16,
                          background: "rgba(248,250,252,0.85)",
                          display: "flex", alignItems: "center", justifyContent: "center",
                          backdropFilter: "blur(1px)",
                          cursor: "not-allowed",
                        }}
                          onClick={() => {
                            setShowCompareLimit(true);
                            setTimeout(() => setShowCompareLimit(false), 3000);
                          }}
                        >
                          <div style={{
                            background: "#fff", border: "2px solid #fca5a5",
                            borderRadius: 12, padding: "10px 18px",
                            display: "flex", alignItems: "center", gap: 8,
                            boxShadow: "0 4px 16px rgba(0,0,0,0.1)",
                          }}>
                            <span style={{ fontSize: 18 }}>⛔</span>
                            <div>
                              <p style={{ margin: 0, fontSize: 13, fontWeight: 800, color: "#dc2626" }}>Max 4 selected</p>
                              <p style={{ margin: 0, fontSize: 11, color: "#94a3b8" }}>Remove one to add this</p>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* ── Card header ── */}
                      <div className="p-4 pb-3">
                        {/* Top row: compare checkbox + missing badge */}
                        <div className="mb-2 flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <div onClick={() => !isDisabled && toggleCompare(api.id)}
                              className="flex h-4 w-4 flex-shrink-0 items-center justify-center rounded border-2 transition-all"
                              style={{ borderColor: isSelected ? "#3b82f6" : isDisabled ? "#e2e8f0" : "#94a3b8", background: isSelected ? "#3b82f6" : "white", cursor: isDisabled ? "not-allowed" : "pointer" }}>
                              {isSelected && <svg width="8" height="6" viewBox="0 0 10 8" fill="none"><path d="M1 4L3.5 6.5L9 1" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/></svg>}
                            </div>
                            <span className="text-xs" style={{ color: isSelected ? "#3b82f6" : "#94a3b8" }}>
                              {isSelected ? "Selected" : "Compare"}
                            </span>
                          </div>
                          {missingCount > 0
                            ? <span className="rounded-full border border-amber-200 bg-amber-50 px-2 py-0.5 text-xs font-semibold text-amber-600">⚠ {missingCount} missing</span>
                            : <span className="rounded-full border border-emerald-200 bg-emerald-50 px-2 py-0.5 text-xs font-semibold text-emerald-600">✓ Complete</span>
                          }
                        </div>

                        {/* Name */}
                        <h3 className="truncate text-base font-bold text-slate-900">{api.name}</h3>

                        {/* Badges */}
                        <div className="mt-1.5 flex flex-wrap gap-1.5">
                          <span className="rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-semibold text-blue-700">{api.category}</span>
                          <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-semibold text-slate-600">{api.version}</span>
                          <span className={`rounded-full px-2.5 py-0.5 text-xs font-semibold ${getRiskBadgeClass(api.risk_level)}`}>{api.risk_level || "Medium"} Risk</span>
                        </div>

                        {/* Description — 2 lines truncated */}
                        <p className="mt-2 text-xs leading-5 text-slate-500 line-clamp-2">{api.description}</p>

                        {/* Key fields row */}
                        <div className="mt-2 flex flex-wrap gap-x-3 gap-y-1">
                          {[["Dev", api.developer], ["Lang", api.programming_language], ["Cost", api.cost]].map(([label, val]) => (
                            <span key={label} className="text-xs text-slate-500">
                              <span className="font-semibold text-slate-400">{label}:</span>{" "}
                              <span className={val && val !== "Unknown" ? "text-slate-700" : "text-amber-400 italic"}>{val || "—"}</span>
                            </span>
                          ))}
                        </div>
                      </div>

                      {/* ── Expandable details ── */}
                      {isExpanded && (
                        <div className="border-t border-slate-100 px-4 py-3">
                          <div className="grid grid-cols-2 gap-x-3 gap-y-2 text-xs">
                            {[["Framework", api.framework],["Latency", api.latency],["Scalability", api.scalability],["Design Pattern", api.design_pattern]].map(([label, val]) => (
                              <div key={label}>
                                <p className="font-semibold uppercase tracking-wide text-slate-400">{label}</p>
                                <p className={val && val !== "Unknown" ? "font-medium text-slate-800" : "italic text-amber-400"}>{val || "Missing"}</p>
                              </div>
                            ))}
                          </div>
                          {api.sample_code && (
                            <div className="mt-3">
                              <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-400">Sample Code</p>
                              <pre className="overflow-x-auto rounded-xl bg-slate-900 p-3 text-xs text-slate-100 max-h-32">{api.sample_code}</pre>
                            </div>
                          )}
                        </div>
                      )}

                      {/* ── Card actions ── */}
                      <div className="flex items-center justify-between border-t border-slate-100 px-4 py-2.5">
                        <button
                          onClick={() => setExpandedId(isExpanded ? null : api.id)}
                          className="text-xs font-semibold text-blue-500 transition hover:text-blue-700"
                        >
                          {isExpanded ? "▲ Less" : "▼ Details"}
                        </button>
                        <div className="flex gap-1.5">
                          <button onClick={() => handleEdit(api)} className="rounded-lg bg-amber-500 px-2.5 py-1 text-xs font-semibold text-white transition hover:bg-amber-600">Edit</button>
                          <button onClick={() => handleDelete(api.id)} className="rounded-lg bg-red-500 px-2.5 py-1 text-xs font-semibold text-white transition hover:bg-red-600">Delete</button>
                          <button onClick={() => copyShareLink(api.id)} className="rounded-lg border border-slate-200 bg-white px-2.5 py-1 text-xs font-semibold text-slate-600 transition hover:bg-slate-50">
                            {copiedId === api.id ? "✓" : "🔗"}
                          </button>
                          <button
                            onClick={() => {
                              const win = window.open("", "_blank");
                              win.document.write(`<html><head><title>${api.name} — SLIB Finder</title><style>body{font-family:system-ui,sans-serif;padding:32px;color:#1e293b}h1{font-size:22px;font-weight:800;margin-bottom:4px}.badge{display:inline-block;border-radius:99px;padding:3px 12px;font-size:12px;font-weight:700;margin-right:6px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:20px 0}.field label{font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:#94a3b8;font-weight:700;display:block;margin-bottom:4px}.field p{font-size:14px;font-weight:600;color:#1e293b;margin:0}pre{background:#0f172a;color:#e2e8f0;padding:16px;border-radius:12px;font-size:12px;overflow-x:auto}</style></head><body><h1>${api.name}</h1><div><span class="badge" style="background:#dbeafe;color:#1d4ed8">${api.category}</span><span class="badge" style="background:#f1f5f9;color:#475569">${api.version}</span></div><p style="margin-top:12px;color:#475569;line-height:1.6;font-size:14px">${api.description}</p><div class="grid">${[["Developer",api.developer],["Language",api.programming_language],["Framework",api.framework],["Cost",api.cost],["Latency",api.latency],["Scalability",api.scalability],["Design Pattern",api.design_pattern]].map(([l,v])=>`<div class="field"><label>${l}</label><p>${v||"N/A"}</p></div>`).join("")}</div>${api.sample_code?`<p style="font-size:11px;font-weight:700;text-transform:uppercase;color:#94a3b8;letter-spacing:.08em;margin-bottom:8px">Sample Code</p><pre>${api.sample_code.replace(/</g,"&lt;")}</pre>`:""}<p style="margin-top:24px;font-size:11px;color:#94a3b8">SLIB Finder — ${new Date().toLocaleDateString()}</p></body></html>`);
                              win.document.close(); win.print();
                            }}
                            className="rounded-lg border border-slate-200 bg-white px-2.5 py-1 text-xs font-semibold text-slate-600 transition hover:bg-slate-50">
                            🖨
                          </button>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="mt-6 flex items-center justify-center gap-2 flex-wrap">
                <button onClick={() => { setCurrentPage((p) => Math.max(1, p - 1)); window.scrollTo({ top: 0, behavior: "smooth" }); }}
                  disabled={currentPage === 1}
                  className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed">
                  ← Prev
                </button>
                {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                  <button key={page} onClick={() => { setCurrentPage(page); window.scrollTo({ top: 0, behavior: "smooth" }); }}
                    className="rounded-xl border px-4 py-2 text-sm font-bold transition"
                    style={{ background: currentPage === page ? "#3b82f6" : "white", color: currentPage === page ? "white" : "#64748b", borderColor: currentPage === page ? "#3b82f6" : "#e2e8f0" }}>
                    {page}
                  </button>
                ))}
                <button onClick={() => { setCurrentPage((p) => Math.min(totalPages, p + 1)); window.scrollTo({ top: 0, behavior: "smooth" }); }}
                  disabled={currentPage === totalPages}
                  className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed">
                  Next →
                </button>
                <span className="text-sm text-slate-400 ml-2">Page {currentPage} of {totalPages} · {sortedFilteredApis.length} total</span>
              </div>
            )}
          </>
        )}
      </div>

      {/* ── Slide-in form drawer ── */}
      {showDrawer && (
        <div style={{ position: "fixed", inset: 0, zIndex: 500 }}>
          {/* Backdrop */}
          <div onClick={() => { if (!editId) resetForm(); else setShowDrawer(false); }}
            style={{ position: "absolute", inset: 0, background: "rgba(15,23,42,0.4)", backdropFilter: "blur(3px)" }} />
          {/* Drawer panel */}
          <div style={{
            position: "absolute", top: 0, right: 0, bottom: 0, width: "100%", maxWidth: 480,
            background: "#fff", boxShadow: "-8px 0 40px rgba(0,0,0,0.15)",
            overflowY: "auto", display: "flex", flexDirection: "column",
          }}>
            {/* Drawer header */}
            <div style={{ padding: "20px 24px 16px", borderBottom: "1px solid #f1f5f9", display: "flex", alignItems: "center", justifyContent: "space-between", position: "sticky", top: 0, background: "#fff", zIndex: 10 }}>
              <div>
                <h2 style={{ fontSize: 18, fontWeight: 800, color: "#1e293b", margin: 0 }}>
                  {editId ? "Edit API Entry" : "Add New API"}
                </h2>
                <p style={{ fontSize: 12, color: "#94a3b8", margin: "2px 0 0 0" }}>
                  {editId ? "Update the fields below" : "Fill in the API details"}
                </p>
              </div>
              <div className="flex items-center gap-2">
                {editId && <span className="rounded-full bg-amber-100 px-3 py-1 text-xs font-semibold text-amber-700">Editing</span>}
                <button onClick={() => { if (!editId) resetForm(); else setShowDrawer(false); }}
                  style={{ background: "#f1f5f9", border: "none", borderRadius: 10, width: 32, height: 32, fontSize: 18, cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", color: "#64748b" }}>
                  ×
                </button>
              </div>
            </div>

            {/* Drawer form */}
            <div style={{ padding: "20px 24px", flex: 1 }}>
              <form onSubmit={(e) => { handleSubmit(e); }} className="space-y-4">
                {/* GitHub fetch */}
                <div>
                  <label className="mb-1.5 block text-sm font-semibold text-slate-700">GitHub Repository</label>
                  <div className="flex gap-2">
                    <input type="text" placeholder="Ex: facebook/react" value={githubRepo}
                      onChange={(e) => setGithubRepo(e.target.value)}
                      onKeyDown={(e) => e.key === "Enter" && handleGithubFetch()}
                      className="w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-100" />
                    <button type="button" onClick={handleGithubFetch} disabled={fetchingGithub}
                      className="whitespace-nowrap rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-indigo-700 disabled:opacity-70">
                      {fetchingGithub ? "..." : "🔍 Fetch"}
                    </button>
                  </div>
                  <p className="mt-1 text-xs text-slate-400">owner/repo format — opens review form</p>
                </div>

                {/* Required fields */}
                {[
                  { name: "name", label: "API Name", placeholder: "Ex: Stripe API", required: true },
                  { name: "category", label: "Category", placeholder: "Ex: Payments", required: true },
                ].map((f) => (
                  <div key={f.name}>
                    <label className="mb-1.5 block text-sm font-semibold text-slate-700">{f.label}</label>
                    <input type="text" name={f.name} placeholder={f.placeholder} value={formData[f.name]} onChange={handleChange} required={f.required}
                      className="w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-100" />
                  </div>
                ))}

                <div>
                  <label className="mb-1.5 block text-sm font-semibold text-slate-700">Description</label>
                  <textarea name="description" placeholder="Short description..." value={formData.description} onChange={handleChange} required rows={3}
                    className="w-full resize-none rounded-xl border border-slate-300 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-100" />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  {[
                    { name: "version", label: "Version", placeholder: "Ex: v1.0.0", required: true },
                    { name: "developer", label: "Developer", placeholder: "Ex: Stripe", required: true },
                    { name: "programming_language", label: "Language", placeholder: "Ex: JavaScript" },
                    { name: "framework", label: "Framework", placeholder: "Ex: REST" },
                    { name: "cost", label: "Cost", placeholder: "Ex: Free" },
                    { name: "latency", label: "Latency", placeholder: "Ex: Low" },
                    { name: "scalability", label: "Scalability", placeholder: "Ex: High" },
                    { name: "design_pattern", label: "Design Pattern", placeholder: "Ex: REST" },
                  ].map((f) => (
                    <div key={f.name}>
                      <label className="mb-1.5 block text-xs font-semibold text-slate-600">{f.label}</label>
                      <input type="text" name={f.name} placeholder={f.placeholder} value={formData[f.name]} onChange={handleChange} required={f.required}
                        className="w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-sm text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-100" />
                    </div>
                  ))}
                </div>

                {/* Sample code */}
                <div>
                  <div className="mb-1.5 flex items-center justify-between">
                    <label className="text-sm font-semibold text-slate-700">Sample Code</label>
                    <button type="button"
                      onClick={() => {
                        if (editId && formData.sample_code) {
                          if (!window.confirm("Replace existing sample code with a template?")) return;
                        }
                        handleGenerateCode();
                      }}
                      className="rounded-lg bg-indigo-100 px-2.5 py-1 text-xs font-bold text-indigo-700 transition hover:bg-indigo-200">
                      ✨ {editId ? "Regenerate" : "Generate"}
                    </button>
                  </div>
                  <textarea name="sample_code" placeholder="Paste code or click Generate..." value={formData.sample_code} onChange={handleChange} rows={5}
                    className="w-full resize-none rounded-xl border border-slate-300 bg-slate-50 px-3 py-2.5 font-mono text-xs text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-100" />
                  <p className="mt-1 text-xs text-slate-400">Language: <strong>{formData.programming_language || "unknown"}</strong></p>
                </div>

                {/* Action buttons */}
                <div className="flex gap-2 pt-2">
                  <button type="submit" disabled={submitting}
                    className="flex-1 rounded-xl bg-blue-600 py-2.5 text-sm font-bold text-white transition hover:bg-blue-700 disabled:opacity-70">
                    {submitting ? (editId ? "Updating..." : "Adding...") : editId ? "Update API" : "Add API"}
                  </button>
                  <button type="button" onClick={resetForm}
                    className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-600 transition hover:bg-slate-50">
                    {editId ? "Cancel" : "Clear"}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Compare limit toast — shown briefly when user tries to select a 5th API */}
      {showCompareLimit && (
        <div style={{
          position: "fixed", bottom: 32, left: "50%", transform: "translateX(-50%)",
          zIndex: 9999,
          background: "linear-gradient(135deg, #dc2626, #b91c1c)",
          color: "#fff",
          borderRadius: 20,
          padding: "16px 28px",
          boxShadow: "0 12px 48px rgba(220,38,38,0.45), 0 4px 16px rgba(0,0,0,0.3)",
          display: "flex", alignItems: "center", gap: 12,
          fontSize: 15, fontWeight: 700,
          whiteSpace: "nowrap",
          border: "2px solid rgba(255,255,255,0.2)",
          minWidth: 360,
          justifyContent: "center",
        }}>
          <span style={{ fontSize: 22 }}>⛔</span>
          <div>
            <p style={{ margin: 0, fontSize: 15, fontWeight: 800 }}>Maximum 4 APIs reached</p>
            <p style={{ margin: "2px 0 0 0", fontSize: 12, fontWeight: 500, opacity: 0.85 }}>
              Remove one from the toolbar above, then add another
            </p>
          </div>
        </div>
      )}

      {/* Compare modal */}
      {showCompare && compareApis.length >= 2 && (
        <CompareModal apis={compareApis} onClose={() => setShowCompare(false)} />
      )}

      {/* Review modal — shown after GitHub fetch */}
      {showReview && (
        <ReviewModal
          formData={formData}
          onUpdate={handleReviewUpdate}
          onGenerateCode={handleGenerateCode}
          onConfirm={handleReviewConfirm}
          onCancel={() => setShowReview(false)}
        />
      )}
    </div>
  );
}

export default App;