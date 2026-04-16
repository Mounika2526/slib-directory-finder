import { useEffect, useMemo, useState } from "react";

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

  const getRiskColor = (risk) => {
    if (risk === "High") return "#dc2626";
    if (risk === "Medium") return "#d97706";
    return "#059669";
  };

  const colWidth = apis.length === 2 ? "1fr 1fr" : apis.length === 3 ? "1fr 1fr 1fr" : "1fr 1fr 1fr 1fr";

  return (
    <div
      style={{
        position: "fixed", inset: 0, zIndex: 1000,
        background: "rgba(15,23,42,0.7)",
        backdropFilter: "blur(6px)",
        display: "flex", alignItems: "flex-start", justifyContent: "center",
        padding: "40px 16px", overflowY: "auto",
      }}
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div style={{
        background: "#fff", borderRadius: 28, width: "100%", maxWidth: 1100,
        boxShadow: "0 32px 80px rgba(0,0,0,0.25)",
        overflow: "hidden", flexShrink: 0,
      }}>
        {/* Header */}
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
              transition: "background 0.2s",
            }}
            onMouseEnter={e => e.currentTarget.style.background = "rgba(255,255,255,0.2)"}
            onMouseLeave={e => e.currentTarget.style.background = "rgba(255,255,255,0.1)"}
          >
            ×
          </button>
        </div>

        <div style={{ padding: "0 32px 32px 32px", overflowX: "auto" }}>
          {/* API Name Headers */}
          <div style={{
            display: "grid", gridTemplateColumns: `180px ${colWidth}`,
            gap: 16, paddingTop: 28, paddingBottom: 20,
            borderBottom: "2px solid #f1f5f9", marginBottom: 8,
          }}>
            <div />
            {apis.map((api) => (
              <div key={api.id} style={{
                background: "linear-gradient(135deg, #eff6ff, #eef2ff)",
                borderRadius: 20, padding: "18px 20px",
                border: "1px solid #bfdbfe",
              }}>
                <h3 style={{ margin: "0 0 8px 0", fontSize: 17, fontWeight: 800, color: "#1e293b" }}>
                  {api.name}
                </h3>
                <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                  <span style={{
                    background: "#dbeafe", color: "#1d4ed8",
                    borderRadius: 20, padding: "3px 10px", fontSize: 11, fontWeight: 600,
                  }}>{api.category}</span>
                  <span style={{
                    background: api.risk_level === "High" ? "#fee2e2" : api.risk_level === "Medium" ? "#fef3c7" : "#d1fae5",
                    color: getRiskColor(api.risk_level),
                    borderRadius: 20, padding: "3px 10px", fontSize: 11, fontWeight: 600,
                  }}>{api.risk_level || "Medium"} Risk</span>
                </div>
              </div>
            ))}
          </div>

          {/* Description Row */}
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
              <div key={api.id} style={{ padding: "4px 0" }}>
                <p style={{ margin: 0, fontSize: 13, color: "#475569", lineHeight: 1.6 }}>
                  {api.description || "—"}
                </p>
              </div>
            ))}
          </div>

          {/* Property Rows */}
          {fields.map((field, i) => {
            const values = apis.map(a => a[field.key] || "—");
            const allSame = values.every(v => v === values[0]);

            return (
              <div key={field.key} style={{
                display: "grid", gridTemplateColumns: `180px ${colWidth}`,
                gap: 16, padding: "14px 0",
                borderBottom: "1px solid #f8fafc",
                background: i % 2 === 0 ? "transparent" : "#fafbff",
                borderRadius: 8,
              }}>
                <div style={{ display: "flex", alignItems: "center" }}>
                  <span style={{ fontSize: 12, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.08em" }}>
                    {field.label}
                  </span>
                </div>
                {apis.map((api, idx) => {
                  const val = api[field.key] || "—";
                  const isRisk = field.key === "risk_level";
                  const isDiff = !allSame;

                  return (
                    <div key={api.id} style={{
                      padding: "6px 12px",
                      background: isDiff ? (idx === 0 ? "#fffbeb" : idx === 1 ? "#f0fdf4" : idx === 2 ? "#eff6ff" : "#fdf4ff") : "transparent",
                      borderRadius: 10,
                      border: isDiff ? "1px solid " + (idx === 0 ? "#fde68a" : idx === 1 ? "#bbf7d0" : idx === 2 ? "#bfdbfe" : "#e9d5ff") : "none",
                    }}>
                      {isRisk ? (
                        <span style={{
                          color: getRiskColor(val),
                          fontWeight: 700, fontSize: 13,
                        }}>{val}</span>
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

          {/* Sample Code Rows */}
          {apis.some(a => a.sample_code) && (
            <>
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
                        overflowX: "auto", whiteSpace: "pre-wrap", wordBreak: "break-all",
                        maxHeight: 160,
                      }}>
                        {api.sample_code}
                      </pre>
                    ) : (
                      <span style={{ fontSize: 13, color: "#cbd5e1" }}>—</span>
                    )}
                  </div>
                ))}
              </div>
            </>
          )}

          {/* Diff legend */}
          <div style={{
            marginTop: 24, padding: "14px 20px",
            background: "#f8fafc", borderRadius: 16,
            display: "flex", alignItems: "center", gap: 10,
          }}>
            <span style={{ fontSize: 12, color: "#94a3b8", fontWeight: 600 }}>
              💡 Highlighted cells indicate differences between entries
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

function App() {
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

  // Compare state
  const [compareIds, setCompareIds] = useState([]);
  const [showCompare, setShowCompare] = useState(false);

  const [formData, setFormData] = useState({
    name: "",
    category: "",
    description: "",
    version: "",
    developer: "",
    programming_language: "",
    framework: "",
    cost: "",
    latency: "",
    scalability: "",
    design_pattern: "",
    sample_code: "",
  });

  const fetchApis = () => {
    setLoading(true);
    setError("");

    fetch("https://slib-directory-finder.onrender.com/api/apis")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch APIs");
        return res.json();
      })
      .then((data) => {
        setApis(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  };

  useEffect(() => { fetchApis(); }, []);

  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => setSuccessMessage(""), 2500);
      return () => clearTimeout(timer);
    }
  }, [successMessage]);

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const resetForm = () => {
    setFormData({
      name: "", category: "", description: "", version: "", developer: "",
      programming_language: "", framework: "", cost: "", latency: "",
      scalability: "", design_pattern: "", sample_code: "",
    });
    setGithubRepo("");
    setEditId(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccessMessage("");
    setSubmitting(true);

    try {
      const url = editId
        ? `https://slib-directory-finder.onrender.com/api/apis/${editId}`
        : "https://slib-directory-finder.onrender.com/api/apis";
      const method = editId ? "PUT" : "POST";

      if (!editId) {
        const alreadyExists = apis.some(
          (api) =>
            api.name?.toLowerCase() === formData.name.toLowerCase() &&
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

  const handleGithubFetch = async () => {
    if (!githubRepo.trim()) { setError("Please enter a GitHub repository in owner/repo format."); return; }
    setError(""); setSuccessMessage(""); setFetchingGithub(true);
    try {
      const res = await fetch("https://slib-directory-finder.onrender.com/api/github-fetch", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repo: githubRepo }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed to fetch GitHub repository data");
      setFormData({
        name: data.name || "", category: data.category || "", description: data.description || "",
        version: data.version || "", developer: data.developer || "",
        programming_language: data.programming_language || "", framework: data.framework || "",
        cost: data.cost || "", latency: data.latency || "", scalability: data.scalability || "",
        design_pattern: data.design_pattern || "", sample_code: data.sample_code || "",
      });
      setSuccessMessage("GitHub repository data fetched successfully.");
    } catch (err) {
      setError(err.message);
    } finally {
      setFetchingGithub(false);
    }
  };

  const handleGithubFetchAndSave = async () => {
    if (!githubRepo.trim()) { setError("Please enter a GitHub repository in owner/repo format."); return; }
    setError(""); setSuccessMessage(""); setFetchingGithub(true);
    try {
      const res = await fetch("https://slib-directory-finder.onrender.com/api/github-fetch", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repo: githubRepo }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed to fetch GitHub repository data");

      const fetchedFormData = {
        name: data.name || "", category: data.category || "", description: data.description || "",
        version: data.version || "", developer: data.developer || "",
        programming_language: data.programming_language || "", framework: data.framework || "",
        cost: data.cost || "", latency: data.latency || "", scalability: data.scalability || "",
        design_pattern: data.design_pattern || "", sample_code: data.sample_code || "",
      };
      setFormData(fetchedFormData);

      const alreadyExists = apis.some(
        (api) =>
          api.name?.toLowerCase() === fetchedFormData.name.toLowerCase() &&
          api.developer?.toLowerCase() === fetchedFormData.developer.toLowerCase()
      );
      if (alreadyExists) { setError("This API entry already exists."); setFetchingGithub(false); return; }

      const saveRes = await fetch("https://slib-directory-finder.onrender.com/api/apis", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(fetchedFormData),
      });
      const saveData = await saveRes.json();
      if (!saveRes.ok) throw new Error(saveData.error || "Fetched successfully, but failed to save API");

      setSuccessMessage("GitHub repository data fetched and saved successfully.");
      setGithubRepo("");
      resetForm();
      fetchApis();
    } catch (err) {
      setError(err.message);
    } finally {
      setFetchingGithub(false);
    }
  };

  const handleDelete = async (id) => {
    const confirmed = window.confirm("Are you sure you want to delete this API?");
    if (!confirmed) return;
    setError(""); setSuccessMessage("");
    try {
      const res = await fetch(`https://slib-directory-finder.onrender.com/api/apis/${id}`, { method: "DELETE" });
      if (!res.ok) throw new Error("Failed to delete API");
      setSuccessMessage("API deleted successfully.");
      setCompareIds(prev => prev.filter(cid => cid !== id));
      fetchApis();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleEdit = (api) => {
    setFormData({
      name: api.name || "", category: api.category || "", description: api.description || "",
      version: api.version || "", developer: api.developer || "",
      programming_language: api.programming_language || "", framework: api.framework || "",
      cost: api.cost || "", latency: api.latency || "", scalability: api.scalability || "",
      design_pattern: api.design_pattern || "", sample_code: api.sample_code || "",
    });
    setEditId(api.id);
    setSuccessMessage("");
    setError("");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  // Compare handlers
  const toggleCompare = (id) => {
    setCompareIds(prev => {
      if (prev.includes(id)) return prev.filter(cid => cid !== id);
      if (prev.length >= 4) return prev; // max 4
      return [...prev, id];
    });
  };

  const compareApis = useMemo(() => apis.filter(a => compareIds.includes(a.id)), [apis, compareIds]);

  const categories = useMemo(() => {
    const uniqueCategories = [...new Set(apis.map((api) => api.category?.trim()).filter(Boolean))].sort();
    return ["All", ...uniqueCategories];
  }, [apis]);

  const filteredApis = useMemo(() => {
    return apis.filter((api) => {
      const term = searchTerm.toLowerCase();
      const matchesSearch =
        api.name?.toLowerCase().includes(term) ||
        api.category?.toLowerCase().includes(term) ||
        api.description?.toLowerCase().includes(term) ||
        api.version?.toLowerCase().includes(term) ||
        api.developer?.toLowerCase().includes(term) ||
        api.programming_language?.toLowerCase().includes(term) ||
        api.framework?.toLowerCase().includes(term) ||
        api.cost?.toLowerCase().includes(term) ||
        api.latency?.toLowerCase().includes(term) ||
        api.scalability?.toLowerCase().includes(term) ||
        api.design_pattern?.toLowerCase().includes(term);
      const matchesCategory = selectedCategory === "All" || api.category === selectedCategory;
      return matchesSearch && matchesCategory;
    });
  }, [apis, searchTerm, selectedCategory]);

  const totalApis = apis.length;
  const totalCategories = Math.max(categories.length - 1, 0);
  const uniqueDevelopers = new Set(apis.map((api) => api.developer?.trim()).filter(Boolean)).size;

  const getRiskBadgeClass = (riskLevel) => {
    if (riskLevel === "High") return "bg-red-100 text-red-700";
    if (riskLevel === "Medium") return "bg-yellow-100 text-yellow-700";
    return "bg-emerald-100 text-emerald-700";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 px-4 py-8 md:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">

        {/* Header */}
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
          </div>
        </div>

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

        {/* ── COMPARE TOOLBAR ── */}
        {compareIds.length > 0 && (
          <div className="mb-6 flex flex-wrap items-center justify-between gap-4 rounded-[20px] border border-blue-200 bg-blue-50 px-5 py-4 shadow-sm">
            <div className="flex flex-wrap items-center gap-3">
              <span className="rounded-full bg-blue-600 px-3 py-1 text-xs font-bold text-white">
                {compareIds.length} selected
              </span>
              <span className="text-sm font-medium text-blue-800">
                {compareIds.length < 2
                  ? `Select ${2 - compareIds.length} more to compare`
                  : compareIds.length < 4
                  ? `Ready to compare — or add up to ${4 - compareIds.length} more`
                  : "Maximum 4 APIs selected"}
              </span>
              <div className="flex flex-wrap gap-2">
                {compareApis.map(a => (
                  <span key={a.id} className="inline-flex items-center gap-1.5 rounded-full bg-white border border-blue-200 px-3 py-1 text-xs font-semibold text-blue-700 shadow-sm">
                    {a.name}
                    <button
                      onClick={() => toggleCompare(a.id)}
                      className="text-blue-400 hover:text-blue-700 leading-none"
                      style={{ fontSize: 14, lineHeight: 1 }}
                    >×</button>
                  </span>
                ))}
              </div>
            </div>
            <div className="flex gap-3">
              {compareIds.length >= 2 && (
                <button
                  onClick={() => setShowCompare(true)}
                  className="rounded-2xl bg-blue-600 px-5 py-2.5 text-sm font-bold text-white shadow-md transition hover:bg-blue-700 hover:shadow-lg"
                >
                  ⚖️ Compare Now
                </button>
              )}
              <button
                onClick={() => setCompareIds([])}
                className="rounded-2xl border border-blue-300 bg-white px-4 py-2.5 text-sm font-semibold text-blue-700 transition hover:bg-blue-50"
              >
                Clear
              </button>
            </div>
          </div>
        )}

        <div className="grid gap-8 lg:grid-cols-3">
          {/* Left: Form */}
          <div className="lg:col-span-1">
            <div className="sticky top-6 rounded-[28px] border border-slate-200/80 bg-white p-6 shadow-lg">
              <div className="mb-6">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <h2 className="text-2xl font-bold text-slate-900">
                      {editId ? "Edit API Entry" : "Add New API"}
                    </h2>
                    <p className="mt-1 text-sm text-slate-500">Enter the API details below.</p>
                  </div>
                  {editId && (
                    <span className="rounded-full bg-amber-100 px-3 py-1 text-xs font-semibold text-amber-700">Editing</span>
                  )}
                </div>
              </div>

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="mb-2 block text-sm font-semibold text-slate-700">GitHub Repository</label>
                  <div className="flex gap-3">
                    <input
                      type="text" placeholder="Ex: facebook/react" value={githubRepo}
                      onChange={(e) => setGithubRepo(e.target.value)}
                      className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100"
                    />
                    <button type="button" onClick={handleGithubFetch} disabled={fetchingGithub}
                      className="rounded-2xl bg-indigo-600 px-4 py-3 font-semibold text-white shadow-md transition hover:bg-indigo-700 disabled:opacity-70">
                      {fetchingGithub ? "..." : "Auto Fill"}
                    </button>
                    <button type="button" onClick={handleGithubFetchAndSave} disabled={fetchingGithub}
                      className="rounded-2xl bg-emerald-600 px-4 py-3 font-semibold text-white shadow-md transition hover:bg-emerald-700 disabled:opacity-70">
                      {fetchingGithub ? "..." : "Fill & Save"}
                    </button>
                  </div>
                  <p className="mt-2 text-xs text-slate-500">Enter a repository in owner/repo format to auto-fill the form.</p>
                </div>

                <div>
                  <label className="mb-2 block text-sm font-semibold text-slate-700">API Name</label>
                  <input type="text" name="name" placeholder="Ex: Stripe API" value={formData.name} onChange={handleChange} required
                    className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100" />
                </div>

                <div>
                  <label className="mb-2 block text-sm font-semibold text-slate-700">Category</label>
                  <input type="text" name="category" placeholder="Ex: Payments" value={formData.category} onChange={handleChange} required
                    className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100" />
                </div>

                <div>
                  <label className="mb-2 block text-sm font-semibold text-slate-700">Description</label>
                  <textarea name="description" placeholder="Write a short description about this API or microservice..." value={formData.description} onChange={handleChange} required rows={4}
                    className="w-full resize-none rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100" />
                </div>

                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <label className="mb-2 block text-sm font-semibold text-slate-700">Version</label>
                    <input type="text" name="version" placeholder="Ex: v1.0.0" value={formData.version} onChange={handleChange} required
                      className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100" />
                  </div>
                  <div>
                    <label className="mb-2 block text-sm font-semibold text-slate-700">Developer</label>
                    <input type="text" name="developer" placeholder="Ex: Internal Team" value={formData.developer} onChange={handleChange} required
                      className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100" />
                  </div>
                </div>

                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <label className="mb-2 block text-sm font-semibold text-slate-700">Programming Language</label>
                    <input type="text" name="programming_language" placeholder="Ex: JavaScript" value={formData.programming_language} onChange={handleChange}
                      className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100" />
                  </div>
                  <div>
                    <label className="mb-2 block text-sm font-semibold text-slate-700">Framework</label>
                    <input type="text" name="framework" placeholder="Ex: Express" value={formData.framework} onChange={handleChange}
                      className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100" />
                  </div>
                </div>

                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <label className="mb-2 block text-sm font-semibold text-slate-700">Cost</label>
                    <input type="text" name="cost" placeholder="Ex: Free / Paid / Freemium" value={formData.cost} onChange={handleChange}
                      className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100" />
                  </div>
                  <div>
                    <label className="mb-2 block text-sm font-semibold text-slate-700">Latency</label>
                    <input type="text" name="latency" placeholder="Ex: Low / Medium / High" value={formData.latency} onChange={handleChange}
                      className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100" />
                  </div>
                </div>

                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <label className="mb-2 block text-sm font-semibold text-slate-700">Scalability</label>
                    <input type="text" name="scalability" placeholder="Ex: High" value={formData.scalability} onChange={handleChange}
                      className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100" />
                  </div>
                  <div>
                    <label className="mb-2 block text-sm font-semibold text-slate-700">Design Pattern</label>
                    <input type="text" name="design_pattern" placeholder="Ex: REST" value={formData.design_pattern} onChange={handleChange}
                      className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100" />
                  </div>
                </div>

                <div>
                  <label className="mb-2 block text-sm font-semibold text-slate-700">Sample Code</label>
                  <textarea name="sample_code" placeholder="Paste sample usage code here..." value={formData.sample_code} onChange={handleChange} rows={5}
                    className="w-full resize-none rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 font-mono text-sm text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100" />
                </div>

                <div className="flex flex-wrap gap-3 pt-2">
                  <button type="submit" disabled={submitting}
                    className="rounded-2xl bg-blue-600 px-5 py-3 font-semibold text-white shadow-md transition hover:bg-blue-700 hover:shadow-lg disabled:cursor-not-allowed disabled:opacity-70">
                    {submitting ? (editId ? "Updating..." : "Adding...") : editId ? "Update API" : "Add API"}
                  </button>
                  <button type="button" onClick={resetForm}
                    className="rounded-2xl border border-slate-300 bg-white px-5 py-3 font-semibold text-slate-700 transition hover:bg-slate-100">
                    Clear
                  </button>
                  {editId && (
                    <button type="button" onClick={resetForm}
                      className="rounded-2xl border border-amber-300 bg-amber-50 px-5 py-3 font-semibold text-amber-700 transition hover:bg-amber-100">
                      Cancel Edit
                    </button>
                  )}
                </div>
              </form>
            </div>
          </div>

          {/* Right: API List */}
          <div className="lg:col-span-2">
            <div className="mb-6 rounded-[28px] border border-slate-200/80 bg-white p-6 shadow-lg">
              <div className="mb-5 flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
                <div>
                  <h2 className="text-2xl font-bold text-slate-900">Search & Filter</h2>
                  <p className="mt-1 text-sm text-slate-500">Find APIs by keyword or narrow them by category.</p>
                </div>
                <div className="flex items-center gap-3 self-start xl:self-auto">
                  <div className="rounded-full bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700">
                    {filteredApis.length} result{filteredApis.length !== 1 ? "s" : ""}
                  </div>
                </div>
              </div>
              <div className="grid gap-4 md:grid-cols-[1.6fr_1fr_auto]">
                <input type="text" placeholder="Search by name, category, language, framework, pattern, developer"
                  value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100" />
                <select value={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)}
                  className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition">
                  <option value="All">All Categories</option>
                  {categories.filter((cat) => cat !== "All").map((category) => (
                    <option key={category} value={category}>{category}</option>
                  ))}
                </select>
                <button type="button" onClick={() => { setSearchTerm(""); setSelectedCategory("All"); }}
                  className="rounded-2xl border border-slate-300 bg-white px-5 py-3 font-semibold text-slate-700 transition hover:bg-slate-100">
                  Reset
                </button>
              </div>
            </div>

            <div className="mb-4 flex items-center justify-between gap-4">
              <div>
                <h2 className="text-2xl font-bold text-slate-900">Available APIs</h2>
                <p className="mt-1 text-sm text-slate-500">
                  Browse and manage your saved API and microservice entries.{" "}
                  <span className="font-medium text-blue-600">Check boxes to compare.</span>
                </p>
              </div>
            </div>

            {loading && (
              <div className="grid gap-6 md:grid-cols-2">
                {[1, 2, 3, 4].map((item) => (
                  <div key={item} className="animate-pulse rounded-[28px] border border-slate-200 bg-white p-6 shadow-lg">
                    <div className="mb-4 h-6 w-2/3 rounded bg-slate-200" />
                    <div className="mb-5 h-5 w-24 rounded-full bg-slate-200" />
                    <div className="space-y-3">
                      <div className="h-4 w-full rounded bg-slate-200" />
                      <div className="h-4 w-5/6 rounded bg-slate-200" />
                      <div className="h-4 w-2/3 rounded bg-slate-200" />
                    </div>
                    <div className="mt-6 flex gap-3">
                      <div className="h-10 w-20 rounded-xl bg-slate-200" />
                      <div className="h-10 w-24 rounded-xl bg-slate-200" />
                    </div>
                  </div>
                ))}
              </div>
            )}

            {!loading && filteredApis.length === 0 && (
              <div className="rounded-[28px] border border-dashed border-slate-300 bg-white p-12 text-center shadow-lg">
                <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-slate-100 text-2xl">🔎</div>
                <h3 className="mt-4 text-xl font-semibold text-slate-800">No APIs found</h3>
                <p className="mt-2 text-slate-500">Try a different search term or add a new API entry.</p>
              </div>
            )}

            {!loading && filteredApis.length > 0 && (
              <div className="grid gap-6 md:grid-cols-2">
                {filteredApis.map((api) => {
                  const isSelected = compareIds.includes(api.id);
                  const isDisabled = !isSelected && compareIds.length >= 4;

                  return (
                    <div key={api.id}
                      className="group rounded-[28px] border bg-white p-6 shadow-lg transition duration-300 hover:-translate-y-1 hover:shadow-2xl"
                      style={{
                        borderColor: isSelected ? "#3b82f6" : "#e2e8f0",
                        boxShadow: isSelected ? "0 0 0 3px rgba(59,130,246,0.15), 0 10px 30px rgba(0,0,0,0.08)" : undefined,
                      }}
                    >
                      <div className="mb-5 flex items-start justify-between gap-3">
                        <div className="min-w-0 flex-1">
                          <div className="flex items-center gap-3 mb-1">
                            {/* Compare checkbox */}
                            <label
                              className="flex items-center gap-2 cursor-pointer select-none"
                              title={isDisabled ? "Maximum 4 APIs can be compared" : isSelected ? "Remove from comparison" : "Add to comparison"}
                            >
                              <div
                                onClick={() => !isDisabled && toggleCompare(api.id)}
                                className="flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-md border-2 transition-all"
                                style={{
                                  borderColor: isSelected ? "#3b82f6" : isDisabled ? "#e2e8f0" : "#94a3b8",
                                  background: isSelected ? "#3b82f6" : "white",
                                  cursor: isDisabled ? "not-allowed" : "pointer",
                                  opacity: isDisabled ? 0.4 : 1,
                                }}
                              >
                                {isSelected && (
                                  <svg width="10" height="8" viewBox="0 0 10 8" fill="none">
                                    <path d="M1 4L3.5 6.5L9 1" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                                  </svg>
                                )}
                              </div>
                              <span className="text-xs font-medium" style={{ color: isSelected ? "#3b82f6" : "#94a3b8" }}>
                                {isSelected ? "Selected" : "Compare"}
                              </span>
                            </label>
                          </div>
                          <h3 className="truncate text-xl font-bold text-slate-900">{api.name}</h3>
                          <div className="mt-3 flex flex-wrap gap-2">
                            <span className="inline-block rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-700">{api.category}</span>
                            <span className="inline-block rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">{api.version}</span>
                            <span className={`inline-block rounded-full px-3 py-1 text-xs font-semibold ${getRiskBadgeClass(api.risk_level)}`}>
                              {api.risk_level || "Medium"} Risk
                            </span>
                          </div>
                        </div>
                      </div>

                      <div className="space-y-4 text-sm text-slate-700">
                        <div>
                          <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">Description</p>
                          <p className="leading-6 text-slate-700">{api.description}</p>
                        </div>
                        <div className="grid grid-cols-2 gap-3">
                          <div>
                            <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">Developer</p>
                            <p className="font-medium text-slate-900">{api.developer || "N/A"}</p>
                          </div>
                          <div>
                            <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">Language</p>
                            <p className="font-medium text-slate-900">{api.programming_language || "N/A"}</p>
                          </div>
                          <div>
                            <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">Framework</p>
                            <p className="font-medium text-slate-900">{api.framework || "N/A"}</p>
                          </div>
                          <div>
                            <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">Cost</p>
                            <p className="font-medium text-slate-900">{api.cost || "N/A"}</p>
                          </div>
                          <div>
                            <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">Latency</p>
                            <p className="font-medium text-slate-900">{api.latency || "N/A"}</p>
                          </div>
                          <div>
                            <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">Scalability</p>
                            <p className="font-medium text-slate-900">{api.scalability || "N/A"}</p>
                          </div>
                          <div className="col-span-2">
                            <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">Design Pattern</p>
                            <p className="font-medium text-slate-900">{api.design_pattern || "N/A"}</p>
                          </div>
                          {api.sample_code && (
                            <div className="col-span-2">
                              <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">Sample Code</p>
                              <pre className="overflow-x-auto rounded-2xl bg-slate-900 p-3 text-xs text-slate-100">{api.sample_code}</pre>
                            </div>
                          )}
                        </div>
                      </div>

                      <div className="mt-6 flex gap-3">
                        <button onClick={() => handleEdit(api)}
                          className="rounded-2xl bg-amber-500 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-amber-600">
                          Edit
                        </button>
                        <button onClick={() => handleDelete(api.id)}
                          className="rounded-2xl bg-red-500 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-red-600">
                          Delete
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Compare Modal */}
      {showCompare && compareApis.length >= 2 && (
        <CompareModal apis={compareApis} onClose={() => setShowCompare(false)} />
      )}
    </div>
  );
}

export default App;