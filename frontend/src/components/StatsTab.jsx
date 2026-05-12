/**
 * StatsTab.jsx — Full analytics dashboard for SLIB Finder
 *
 * Displays KPI tiles and charts computed from the full API list.
 * Users can filter stats by developer and/or category.
 *
 * Props:
 *   apis — full array of API entry objects
 */

import React, { useMemo, useState } from "react";
import { SimpleBarChart, DonutChart, StatCard } from "./Charts";

function StatsTab({ apis }) {
  // ── Filter state ──────────────────────────────────────────────────
  const [filterDeveloper, setFilterDeveloper] = useState("All");
  const [filterCategory, setFilterCategory] = useState("All");

  // Searchable developer dropdown state
  const [devSearch, setDevSearch] = useState("");
  const [showDevDropdown, setShowDevDropdown] = useState(false);

  // Unique sorted lists for filter dropdowns
  const allDevelopers = useMemo(() =>
    ["All", ...[...new Set(apis.map((a) => a.developer?.trim()).filter(Boolean))].sort()],
    [apis]
  );

  const filteredDevelopers = useMemo(() =>
    allDevelopers.filter((d) =>
      d === "All" || d.toLowerCase().includes(devSearch.toLowerCase())
    ),
    [allDevelopers, devSearch]
  );

  const allCategories = useMemo(() =>
    ["All", ...[...new Set(apis.map((a) => a.category?.trim()).filter(Boolean))].sort()],
    [apis]
  );

  // Apply developer + category filters to the full API list
  const filteredData = useMemo(() => apis.filter((a) => {
    const matchDev = filterDeveloper === "All" || a.developer?.trim() === filterDeveloper;
    const matchCat = filterCategory === "All" || a.category?.trim() === filterCategory;
    return matchDev && matchCat;
  }), [apis, filterDeveloper, filterCategory]);

  const isFiltered = filterDeveloper !== "All" || filterCategory !== "All";

  // ── Chart data ────────────────────────────────────────────────────

  const categoryCounts = useMemo(() => {
    const map = {};
    filteredData.forEach((a) => {
      const cat = a.category?.trim() || "Unknown";
      map[cat] = (map[cat] || 0) + 1;
    });
    return Object.entries(map).sort((a, b) => b[1] - a[1])
      .map(([label, value], i) => ({
        label, value,
        color: ["#3b82f6","#6366f1","#8b5cf6","#ec4899","#f59e0b","#10b981","#ef4444","#06b6d4","#f97316","#84cc16"][i % 10],
      }));
  }, [filteredData]);

  const developerCounts = useMemo(() => {
    const map = {};
    filteredData.forEach((a) => {
      const dev = a.developer?.trim() || "Unknown";
      map[dev] = (map[dev] || 0) + 1;
    });
    return Object.entries(map).sort((a, b) => b[1] - a[1]).slice(0, 15)
      .map(([label, value], i) => ({
        label, value,
        color: ["#6366f1","#8b5cf6","#a78bfa","#c4b5fd","#ddd6fe","#3b82f6","#60a5fa","#93c5fd","#bfdbfe","#e0f2fe"][i % 10],
      }));
  }, [filteredData]);

  const riskCounts = useMemo(() => {
    const map = { Low: 0, Medium: 0, High: 0 };
    filteredData.forEach((a) => {
      const r = a.risk_level || "Medium";
      map[r] = (map[r] || 0) + 1;
    });
    return [
      { label: "Low", value: map.Low, color: "#10b981" },
      { label: "Medium", value: map.Medium, color: "#f59e0b" },
      { label: "High", value: map.High, color: "#ef4444" },
    ].filter((s) => s.value > 0);
  }, [filteredData]);

  const languageCounts = useMemo(() => {
    const map = {};
    filteredData.forEach((a) => {
      const lang = a.programming_language?.trim() || "Unknown";
      map[lang] = (map[lang] || 0) + 1;
    });
    return Object.entries(map).sort((a, b) => b[1] - a[1]).slice(0, 8)
      .map(([label, value], i) => ({
        label, value,
        color: ["#10b981","#14b8a6","#06b6d4","#0ea5e9","#3b82f6","#6366f1","#8b5cf6","#ec4899"][i % 8],
      }));
  }, [filteredData]);

  const costCounts = useMemo(() => {
    const map = {};
    filteredData.forEach((a) => {
      const cost = a.cost?.trim() || "Unknown";
      map[cost] = (map[cost] || 0) + 1;
    });
    return Object.entries(map).sort((a, b) => b[1] - a[1]).slice(0, 6)
      .map(([label, value], i) => ({
        label, value,
        color: ["#f59e0b","#10b981","#3b82f6","#8b5cf6","#ef4444","#94a3b8"][i % 6],
      }));
  }, [filteredData]);

  const patternCounts = useMemo(() => {
    const map = {};
    filteredData.forEach((a) => {
      const p = a.design_pattern?.trim() || "Unknown";
      map[p] = (map[p] || 0) + 1;
    });
    return Object.entries(map).sort((a, b) => b[1] - a[1]).slice(0, 6)
      .map(([label, value], i) => ({
        label, value,
        color: ["#f97316","#eab308","#84cc16","#06b6d4","#a855f7","#ec4899"][i % 6],
      }));
  }, [filteredData]);

  const scalabilityCounts = useMemo(() => {
    const map = {};
    filteredData.forEach((a) => {
      const s = a.scalability?.trim() || "Unknown";
      map[s] = (map[s] || 0) + 1;
    });
    return Object.entries(map).sort((a, b) => b[1] - a[1])
      .map(([label, value], i) => ({
        label, value,
        color: ["#10b981","#3b82f6","#f59e0b","#ef4444","#8b5cf6","#94a3b8"][i % 6],
      }));
  }, [filteredData]);

  const topDevelopers = developerCounts.slice(0, 5);

  // KPI tiles
  const totalApis = filteredData.length;
  const uniqueCategories = new Set(filteredData.map((a) => a.category?.trim()).filter(Boolean)).size;
  const uniqueDevelopers = new Set(filteredData.map((a) => a.developer?.trim()).filter(Boolean)).size;
  const lowRiskCount = filteredData.filter((a) => (a.risk_level || "Medium") === "Low").length;

  return (
    <div className="space-y-8">

      {/* ── Stats Filter Bar ── */}
      <div className="mb-4 rounded-[24px] border border-slate-200/80 bg-white p-4 shadow-sm">
        <div className="flex flex-wrap items-center gap-3">

          <span className="text-sm font-bold text-slate-600">Filter Stats By:</span>

          {/* Developer filter — searchable dropdown */}
          <div className="flex items-center gap-2" style={{ position: "relative" }}>
            <label className="text-xs font-semibold uppercase tracking-wide text-slate-400">Developer</label>
            <div style={{ position: "relative" }}>
              <input
                type="text"
                placeholder={filterDeveloper === "All" ? "All Developers" : filterDeveloper}
                value={devSearch}
                onFocus={() => setShowDevDropdown(true)}
                onBlur={() => setTimeout(() => setShowDevDropdown(false), 150)}
                onChange={(e) => { setDevSearch(e.target.value); setShowDevDropdown(true); }}
                className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm font-medium text-slate-700 outline-none transition focus:border-blue-400 focus:bg-white focus:ring-2 focus:ring-blue-100"
                style={{ width: 180 }}
              />
              {showDevDropdown && (
                <div style={{
                  position: "absolute", top: "110%", left: 0, zIndex: 200,
                  background: "#fff", border: "1px solid #e2e8f0",
                  borderRadius: 14, boxShadow: "0 8px 32px rgba(0,0,0,0.12)",
                  maxHeight: 240, overflowY: "auto", minWidth: 200,
                }}>
                  {filteredDevelopers.length === 0 ? (
                    <div style={{ padding: "10px 14px", fontSize: 12, color: "#94a3b8" }}>
                      No matches found
                    </div>
                  ) : filteredDevelopers.map((d) => (
                    <div
                      key={d}
                      onMouseDown={() => {
                        setFilterDeveloper(d);
                        setDevSearch("");
                        setShowDevDropdown(false);
                      }}
                      style={{
                        padding: "8px 14px", fontSize: 13, cursor: "pointer",
                        fontWeight: d === filterDeveloper ? 700 : 400,
                        color: d === filterDeveloper ? "#2563eb" : "#374151",
                        background: d === filterDeveloper ? "#eff6ff" : "transparent",
                      }}
                      onMouseEnter={(e) => e.currentTarget.style.background = d === filterDeveloper ? "#eff6ff" : "#f8fafc"}
                      onMouseLeave={(e) => e.currentTarget.style.background = d === filterDeveloper ? "#eff6ff" : "transparent"}
                    >
                      {d}
                    </div>
                  ))}
                  {/* Fade gradient */}
                  <div style={{
                    position: "sticky", bottom: 0,
                    height: 32, pointerEvents: "none",
                    background: "linear-gradient(to bottom, transparent, rgba(255,255,255,0.95))",
                    borderRadius: "0 0 14px 14px",
                  }} />
                </div>
              )}
            </div>
            {filterDeveloper !== "All" && (
              <span className="rounded-full bg-blue-100 px-2 py-0.5 text-xs font-bold text-blue-700">
                {filterDeveloper}
                <button
                  onMouseDown={() => { setFilterDeveloper("All"); setDevSearch(""); }}
                  style={{ marginLeft: 4, color: "#2563eb", fontWeight: 700, background: "none", border: "none", cursor: "pointer" }}
                >×</button>
              </span>
            )}
          </div>

          {/* Category filter */}
          <div className="flex items-center gap-2">
            <label className="text-xs font-semibold uppercase tracking-wide text-slate-400">Category</label>
            <select
              value={filterCategory}
              onChange={(e) => setFilterCategory(e.target.value)}
              className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-700 outline-none transition focus:border-blue-400 focus:ring-2 focus:ring-blue-100"
            >
              {allCategories.map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>

          {/* Reset button */}
          {isFiltered && (
            <button
              onClick={() => { setFilterDeveloper("All"); setFilterCategory("All"); setDevSearch(""); }}
              className="rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm font-semibold text-slate-500 transition hover:bg-slate-50"
            >
              Reset
            </button>
          )}

          {/* Active filter count badge */}
          {isFiltered && (
            <span className="rounded-full bg-blue-100 px-3 py-1 text-xs font-bold text-blue-700">
              Showing {filteredData.length} of {apis.length} APIs
            </span>
          )}
        </div>
      </div>

      {/* ── KPI Tiles ── */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard label={isFiltered ? "Filtered APIs" : "Total APIs"} value={totalApis} color="#3b82f6" icon="apis" />
        <StatCard label="Categories" value={uniqueCategories} color="#8b5cf6" icon="categories" />
        <StatCard label="Developers" value={uniqueDevelopers} color="#10b981" icon="developers" />
        <StatCard label="Low Risk" value={lowRiskCount} color="#059669" icon="lowrisk" />
      </div>

      {/* ── Chart rows ── */}
      <div className="grid gap-6 lg:grid-cols-2" style={{ alignItems: "stretch" }}>
        <div className="rounded-[24px] border border-slate-200 bg-white p-6 shadow-sm">
          <SimpleBarChart data={categoryCounts} title="APIs by Category" />
        </div>
        <div className="rounded-[24px] border border-slate-200 bg-white p-6 shadow-sm flex flex-col justify-between">
          <SimpleBarChart data={developerCounts} title="Top Developers by API Count" />
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-[24px] border border-slate-200 bg-white p-6 shadow-sm">
          <DonutChart segments={riskCounts} title="Risk Level Distribution" />
        </div>
        <div className="rounded-[24px] border border-slate-200 bg-white p-6 shadow-sm">
          <DonutChart segments={costCounts} title="Cost Model Breakdown" />
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-[24px] border border-slate-200 bg-white p-6 shadow-sm">
          <SimpleBarChart data={languageCounts} title="Programming Languages" />
        </div>
        <div className="rounded-[24px] border border-slate-200 bg-white p-6 shadow-sm">
          <SimpleBarChart data={patternCounts} title="Design Patterns" />
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-[24px] border border-slate-200 bg-white p-6 shadow-sm">
          <DonutChart
            segments={scalabilityCounts.slice(0, 5).map((s, i) => ({
              ...s,
              color: ["#10b981","#3b82f6","#f59e0b","#ef4444","#94a3b8"][i],
            }))}
            title="Scalability Distribution"
          />
        </div>
        <div className="rounded-[24px] border border-slate-200 bg-white p-6 shadow-sm">
          <p className="mb-4 text-sm font-bold uppercase tracking-wide text-slate-500">
            Developer Leaderboard
          </p>
          <div className="space-y-3">
            {topDevelopers.map((dev, idx) => (
              <div
                key={dev.label}
                className="flex items-center gap-4 rounded-2xl border border-slate-100 bg-slate-50 px-4 py-3"
              >
                <div
                  className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full text-sm font-black text-white"
                  style={{
                    background: idx === 0 ? "#f59e0b" : idx === 1 ? "#94a3b8" : idx === 2 ? "#b45309" : "#6366f1",
                  }}
                >
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

export default StatsTab;