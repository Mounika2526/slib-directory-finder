/**
 * App.jsx — Root component for SLIB Finder: API & Microservices Directory
 *
 * This is the main entry point of the React application.
 * It manages all global state and orchestrates the full UI.
 *
 * Architecture:
 *   - All API data is fetched from the Flask backend on mount
 *   - Search, filter, sort, and pagination are handled client-side
 *   - The drawer (add/edit form), modals, and toasts are conditionally rendered
 *   - Helper functions and sub-components are imported from utils/ and components/
 *
 * Tabs:
 *   "directory" — searchable, filterable card grid of all API entries
 *   "stats"     — analytics dashboard with charts and KPI tiles
 *
 * Key features:
 *   - Add / Edit / Delete API entries via a slide-in drawer
 *   - GitHub auto-fill: fetch repo metadata and pre-populate the form
 *   - Post-fetch ReviewModal: user fills in fields GitHub can't provide
 *   - Sample code generation from language-specific templates
 *   - Relevance-ranked search with typo tolerance (bigram scoring)
 *   - Side-by-side comparison of up to 4 APIs
 *   - CSV export of the current filtered results
 *   - Shareable deep-link URL per API card
 *   - Back-to-top floating button
 */

import React, { useEffect, useMemo, useState } from "react";
import { scoreApi } from "./utils/search";
import { getRiskBadgeClass } from "./utils/riskHelpers";
import { generateSampleCode } from "./utils/codeGenerator";
import ReviewModal from "./components/ReviewModal";
import StatsTab from "./components/StatsTab";
import CompareModal from "./components/CompareModal";

// ─────────────────────────────────────────────────────────────────────────────
// BACKEND BASE URL
// Points to the deployed Flask API on Render.
// Update this if the backend deployment URL changes.
// ─────────────────────────────────────────────────────────────────────────────
const API_BASE = "https://slib-directory-finder.onrender.com";

// ─────────────────────────────────────────────────────────────────────────────
// COMPONENT: BackToTop
//
// A floating button fixed to the bottom-right of the screen.
// Becomes visible after the user scrolls down more than 300px.
// Clicking it smoothly scrolls back to the top of the page.
// ─────────────────────────────────────────────────────────────────────────────
function BackToTop() {
  const [visible, setVisible] = React.useState(false);

  // Listen to scroll events and show/hide based on scroll position
  React.useEffect(() => {
    const onScroll = () => setVisible(window.scrollY > 300);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll); // cleanup on unmount
  }, []);

  // Don't render anything if the button is not visible
  if (!visible) return null;

  return (
    <button
      onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
      style={{
        position: "fixed", bottom: 100, right: 32, zIndex: 999,
        background: "#1e3a5f", color: "#fff",
        border: "none", borderRadius: 12,
        width: 44, height: 44,
        display: "flex", alignItems: "center", justifyContent: "center",
        boxShadow: "0 4px 20px rgba(0,0,0,0.2)",
        cursor: "pointer", transition: "opacity 0.2s",
        opacity: visible ? 1 : 0,
      }}
      title="Back to top"
    >
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="18 15 12 9 6 15"/>
      </svg>
    </button>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// COMPONENT: App (root)
// ─────────────────────────────────────────────────────────────────────────────
function App() {

  // ── Core data state ───────────────────────────────────────────────────────
  const [apis, setApis] = useState([]);          // all API entries from the backend
  const [loading, setLoading] = useState(true);  // true while the initial fetch is in progress
  const [submitting, setSubmitting] = useState(false); // true while a form is being submitted
  const [error, setError] = useState("");         // global error message (shown above cards)
  const [successMessage, setSuccessMessage] = useState(""); // global success message

  // ── Search and filter state ───────────────────────────────────────────────
  const [searchTerm, setSearchTerm] = useState("");          // current text in the search bar
  const [selectedCategory, setSelectedCategory] = useState("All"); // active category filter
  const [sortBy, setSortBy] = useState("default");           // active sort order

  // ── Pagination state ──────────────────────────────────────────────────────
  const [currentPage, setCurrentPage] = useState(1);
  const ITEMS_PER_PAGE = 12; // number of cards shown per page

  // ── Form and drawer state ─────────────────────────────────────────────────
  const [editId, setEditId] = useState(null);         // id of the entry being edited (null = add mode)
  const [githubRepo, setGithubRepo] = useState("");   // value of the GitHub repo input
  const [fetchingGithub, setFetchingGithub] = useState(false); // true while GitHub fetch is in progress
  const [showDrawer, setShowDrawer] = useState(false); // controls the slide-in form drawer
  const [showReview, setShowReview] = useState(false); // controls the ReviewModal visibility
  const [drawerError, setDrawerError] = useState("");  // inline error shown inside the drawer
  const drawerErrorTimer = React.useRef(null);         // ref for the drawer error auto-dismiss timer

  // ── Card expansion state ──────────────────────────────────────────────────
  const [expandedId, setExpandedId] = useState(null); // id of the card with expanded details

  // ── Compare state ─────────────────────────────────────────────────────────
  const [compareIds, setCompareIds] = useState([]);     // ids of APIs selected for comparison
  const [showCompare, setShowCompare] = useState(false); // controls the CompareModal visibility
  const [showCompareLimit, setShowCompareLimit] = useState(false); // toast for 4-item limit

  // ── Toast and copy state ──────────────────────────────────────────────────
  const [toast, setToast] = useState(null);    // { message, type } for the bottom-right toast
  const [copiedId, setCopiedId] = useState(null); // id of card whose share link was just copied

  // ── Tab state ─────────────────────────────────────────────────────────────
  const [activeTab, setActiveTab] = useState("directory"); // "directory" or "stats"

  // ── Form data (controlled inputs) ────────────────────────────────────────
  // All fields match the ApiEntry model in the backend
  const [formData, setFormData] = useState({
    name: "", category: "", description: "", version: "", developer: "",
    programming_language: "", framework: "", cost: "", latency: "",
    scalability: "", design_pattern: "", sample_code: "",
  });

  // ── Data fetching ─────────────────────────────────────────────────────────

  /**
   * fetchApis
   * Loads all API entries from the backend and stores them in state.
   * Called on mount and after any add/edit/delete operation.
   */
  const fetchApis = () => {
    setLoading(true);
    setError("");
    fetch(`${API_BASE}/api/apis`)
      .then((res) => { if (!res.ok) throw new Error("Failed to fetch APIs"); return res.json(); })
      .then((data) => { setApis(data); setLoading(false); })
      .catch((err) => { setError(err.message); setLoading(false); });
  };

  // Fetch APIs on initial mount
  useEffect(() => { fetchApis(); }, []);

  // Auto-clear success message after 2.5 seconds
  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => setSuccessMessage(""), 2500);
      return () => clearTimeout(timer);
    }
  }, [successMessage]);

  // Auto-dismiss bottom-right toast after 5 seconds
  useEffect(() => {
    if (toast) {
      const timer = setTimeout(() => setToast(null), 5000);
      return () => clearTimeout(timer);
    }
  }, [toast]);

  // ── Form handlers ─────────────────────────────────────────────────────────

  // Update a single form field from an input onChange event
  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  // Update a single form field by key — used by ReviewModal
  const handleReviewUpdate = (key, value) => setFormData((prev) => ({ ...prev, [key]: value }));

  /**
   * resetForm
   * Clears all form fields and exits edit mode.
   * Also closes the drawer and clears any drawer error.
   */
  const resetForm = () => {
    setFormData({
      name: "", category: "", description: "", version: "", developer: "",
      programming_language: "", framework: "", cost: "", latency: "",
      scalability: "", design_pattern: "", sample_code: "",
    });
    setGithubRepo("");
    setEditId(null);
    setDrawerError("");
    setShowDrawer(false);
  };

  /**
   * showDrawerError
   * Displays an inline error message inside the drawer.
   * Auto-dismisses after 5 seconds using a ref-tracked timer.
   *
   * @param {string} msg - Error message to display
   */
  const showDrawerError = (msg) => {
    if (drawerErrorTimer.current) clearTimeout(drawerErrorTimer.current);
    setDrawerError(msg);
    drawerErrorTimer.current = setTimeout(() => setDrawerError(""), 5000);
  };

  /**
   * handleGenerateCode
   * Generates a language-specific sample code snippet from the template library
   * and injects it into the sample_code field of the form.
   */
  const handleGenerateCode = () => {
    const code = generateSampleCode(formData.name, formData.programming_language);
    setFormData((prev) => ({ ...prev, sample_code: code }));
  };

  /**
   * handleSubmit
   * Submits the form — either POST (add) or PUT (edit) depending on editId.
   * Performs a client-side duplicate check before hitting the backend.
   *
   * @param {Event} e - Form submit event
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(""); setSuccessMessage(""); setDrawerError(""); setSubmitting(true);
    try {
      const url = editId ? `${API_BASE}/api/apis/${editId}` : `${API_BASE}/api/apis`;
      const method = editId ? "PUT" : "POST";

      // Client-side duplicate check — avoids a round-trip to the server for obvious duplicates
      if (!editId) {
        const alreadyExists = apis.some(
          (api) => api.name?.toLowerCase() === formData.name.toLowerCase() &&
                   api.developer?.toLowerCase() === formData.developer.toLowerCase()
        );
        if (alreadyExists) {
          showDrawerError("An entry with this name and developer already exists.");
          setSubmitting(false);
          return;
        }
      }

      const res = await fetch(url, {
        method, headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || (editId ? "Failed to update API" : "Failed to add API"));

      // Success — close the drawer and show the bottom toast
      const msg = editId ? "API updated successfully." : "API added successfully.";
      resetForm();
      fetchApis();
      setToast({ message: msg, type: "success" });
    } catch (err) {
      showDrawerError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  /**
   * handleGithubFetch
   * Calls the backend GitHub proxy endpoint with the entered repo name.
   * On success: pre-fills the form with repo metadata and opens the ReviewModal.
   * On duplicate found: shows an inline error instead of opening the modal.
   */
  const handleGithubFetch = async () => {
    if (!githubRepo.trim()) { showDrawerError("Please enter a GitHub repository in owner/repo format."); return; }
    setError(""); setSuccessMessage(""); setDrawerError(""); setFetchingGithub(true);
    try {
      const res = await fetch(`${API_BASE}/api/github-fetch`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repo: githubRepo }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed to fetch GitHub repository data");

      // Check for duplicates before opening the review modal
      // This avoids making the user fill in all fields only to get a duplicate error at the end
      const alreadyExists = apis.some(
        (api) => api.name?.toLowerCase() === (data.name || "").toLowerCase() &&
                 api.developer?.toLowerCase() === (data.developer || "").toLowerCase()
      );
      if (alreadyExists) {
        showDrawerError(`"${data.name}" by ${data.developer} already exists in the directory.`);
        setFetchingGithub(false);
        return;
      }

      // Pre-fill the form with GitHub data — fields not available from GitHub are left empty
      setFormData({
        name: data.name || "", category: data.category || "",
        description: data.description || "", version: data.version || "",
        developer: data.developer || "", programming_language: data.programming_language || "",
        framework: "", cost: "", latency: "", scalability: "",
        design_pattern: "", sample_code: "",
      });

      // Open the review modal so the user can fill in the missing fields
      setShowReview(true);
    } catch (err) {
      showDrawerError(err.message);
    } finally {
      setFetchingGithub(false);
    }
  };

  /**
   * handleReviewConfirm
   * Called when the user clicks "Save Entry" in the ReviewModal.
   * Submits the completed form data to the backend as a new POST.
   */
  const handleReviewConfirm = async () => {
    setShowReview(false);
    setError(""); setSuccessMessage(""); setDrawerError(""); setSubmitting(true);
    try {
      // Final duplicate check before saving
      const alreadyExists = apis.some(
        (api) => api.name?.toLowerCase() === formData.name.toLowerCase() &&
                 api.developer?.toLowerCase() === formData.developer.toLowerCase()
      );
      if (alreadyExists) {
        showDrawerError("An entry with this name and developer already exists.");
        setSubmitting(false);
        return;
      }

      const res = await fetch(`${API_BASE}/api/apis`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed to save API");

      resetForm();
      fetchApis();
      setToast({ message: "API saved successfully.", type: "success" });
    } catch (err) {
      showDrawerError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  /**
   * handleDelete
   * Deletes an API entry by id after user confirmation.
   * Also removes the deleted entry from the compare selection if present.
   *
   * @param {number} id - The id of the ApiEntry to delete
   */
  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this API?")) return;
    setError(""); setSuccessMessage("");
    try {
      const res = await fetch(`${API_BASE}/api/apis/${id}`, { method: "DELETE" });
      if (!res.ok) throw new Error("Failed to delete API");
      setToast({ message: "API deleted successfully.", type: "success" });
      // Remove from compare selection so the compare toolbar stays consistent
      setCompareIds((prev) => prev.filter((cid) => cid !== id));
      fetchApis();
    } catch (err) {
      setError(err.message);
    }
  };

  /**
   * handleEdit
   * Populates the form with an existing entry's data and opens the drawer in edit mode.
   *
   * @param {object} api - The ApiEntry object to edit
   */
  const handleEdit = (api) => {
    setFormData({
      name: api.name || "", category: api.category || "", description: api.description || "",
      version: api.version || "", developer: api.developer || "",
      programming_language: api.programming_language || "", framework: api.framework || "",
      cost: api.cost || "", latency: api.latency || "", scalability: api.scalability || "",
      design_pattern: api.design_pattern || "", sample_code: api.sample_code || "",
    });
    setEditId(api.id);
    setSuccessMessage(""); setError(""); setDrawerError("");
    setShowDrawer(true);
    setActiveTab("directory"); // switch to directory tab if on stats
  };

  // ── Compare handlers ──────────────────────────────────────────────────────

  /**
   * toggleCompare
   * Adds or removes an API from the compare selection.
   * Maximum of 4 APIs can be selected at once.
   * Shows a toast if the user tries to add a 5th.
   *
   * @param {number} id - The id of the ApiEntry to toggle
   */
  const toggleCompare = (id) => {
    setCompareIds((prev) => {
      if (prev.includes(id)) return prev.filter((cid) => cid !== id); // deselect
      if (prev.length >= 4) {
        // Show limit toast briefly and return unchanged selection
        setShowCompareLimit(true);
        setTimeout(() => setShowCompareLimit(false), 2500);
        return prev;
      }
      return [...prev, id]; // add to selection
    });
  };

  // ── Export to CSV ─────────────────────────────────────────────────────────

  /**
   * exportToCSV
   * Converts the currently filtered API list to a CSV file and triggers a download.
   * Uses the browser Blob + anchor click pattern — no library required.
   * Exported file name includes today's date for easy identification.
   */
  const exportToCSV = () => {
    const headers = ["Name","Category","Version","Developer","Language","Framework","Cost","Latency","Scalability","Design Pattern","Risk Level","Description","Sample Code"];
    const rows = filteredApis.map((api) => [
      api.name, api.category, api.version, api.developer,
      api.programming_language, api.framework, api.cost,
      api.latency, api.scalability, api.design_pattern,
      api.risk_level, api.description,
      (api.sample_code || "").replace(/\n/g, " "), // flatten multiline code to single line
    ].map((v) => `"${(v || "").replace(/"/g, '""')}"`)); // escape quotes for CSV

    const csv = [headers.join(","), ...rows.map((r) => r.join(","))].join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `slib-directory-${new Date().toISOString().slice(0,10)}.csv`;
    a.click();
    URL.revokeObjectURL(url); // release memory after download
  };

  // ── Shareable card link ───────────────────────────────────────────────────

  /**
   * copyShareLink
   * Copies a deep-link URL for a specific API card to the clipboard.
   * The link uses the api id as a URL hash so it's bookmarkable.
   * Shows a brief checkmark on the card button to confirm the copy.
   *
   * @param {number} id - The id of the ApiEntry to link to
   */
  const copyShareLink = (id) => {
    const url = `${window.location.origin}${window.location.pathname}#api-${id}`;
    navigator.clipboard.writeText(url).then(() => {
      setCopiedId(id);
      setTimeout(() => setCopiedId(null), 2000); // reset checkmark after 2 seconds
    });
  };

  // ── Derived data ──────────────────────────────────────────────────────────

  // ApiEntry objects for the currently selected compare ids.
  // Derived from the full apis array so data is always fresh after edits.
  const compareApis = useMemo(() => apis.filter((a) => compareIds.includes(a.id)), [apis, compareIds]);

  // Unique sorted category list for the filter dropdown.
  // "All" is prepended so it always appears first in the select element.
  // Memoized so it only recomputes when the apis array changes.
  const categories = useMemo(() => {
    const unique = [...new Set(apis.map((api) => api.category?.trim()).filter(Boolean))].sort();
    return ["All", ...unique];
  }, [apis]);

  /**
   * filteredApis
   * Applies search scoring and category filter to the full API list.
   * Each entry gets a _score property from scoreApi() — entries with
   * a score of 0 are excluded entirely from the results.
   * The category filter is applied after scoring as a hard AND condition.
   */
  const filteredApis = useMemo(() => {
    const term = searchTerm.toLowerCase().trim();
    return apis
      .map((api) => ({ ...api, _score: scoreApi(api, term) }))
      .filter((api) => api._score > 0 &&
        (selectedCategory === "All" || api.category === selectedCategory)
      );
  }, [apis, searchTerm, selectedCategory]);

  /**
   * sortedFilteredApis
   * Applies the active sort order to the filtered list.
   * When searching with default sort, results are ranked by relevance score.
   * Named sort options (name-asc, risk-high, etc.) override relevance ranking.
   */
  const sortedFilteredApis = useMemo(() => {
    const list = [...filteredApis];
    const isSearching = searchTerm.trim().length > 0;

    // Named sort options — applied regardless of whether a search is active
    if (sortBy === "name-asc")   return list.sort((a, b) => (a.name || "").localeCompare(b.name || ""));
    if (sortBy === "name-desc")  return list.sort((a, b) => (b.name || "").localeCompare(a.name || ""));
    if (sortBy === "risk-high")  return list.sort((a, b) => ["High","Medium","Low"].indexOf(a.risk_level) - ["High","Medium","Low"].indexOf(b.risk_level));
    if (sortBy === "risk-low")   return list.sort((a, b) => ["Low","Medium","High"].indexOf(a.risk_level) - ["Low","Medium","High"].indexOf(b.risk_level));
    if (sortBy === "category")   return list.sort((a, b) => (a.category || "").localeCompare(b.category || ""));
    if (sortBy === "developer")  return list.sort((a, b) => (a.developer || "").localeCompare(b.developer || ""));

    // Default sort — rank by relevance score when a search is active
    // This ensures the best match always appears first
    if (isSearching) return list.sort((a, b) => b._score - a._score);

    // No search active — preserve original database insertion order
    return list;
  }, [filteredApis, sortBy, searchTerm]);

  // Reset to page 1 whenever search term, category filter, or sort order changes
  // Prevents the user from landing on a non-existent page after filtering
  useEffect(() => { setCurrentPage(1); }, [searchTerm, selectedCategory, sortBy]);

  // ── Pagination calculations ───────────────────────────────────────────────
  // totalPages — how many pages the sorted+filtered list spans
  const totalPages = Math.ceil(sortedFilteredApis.length / ITEMS_PER_PAGE);

  // paginatedApis — the slice of cards shown on the current page
  const paginatedApis = sortedFilteredApis.slice(
    (currentPage - 1) * ITEMS_PER_PAGE,
    currentPage * ITEMS_PER_PAGE
  );

  // ── Header stats ──────────────────────────────────────────────────────────
  // These always reflect the full unfiltered dataset (shown in the page header)
  // so they give a consistent overview regardless of active search/filter state
  const totalApis = apis.length;
  const totalCategories = Math.max(categories.length - 1, 0); // subtract "All" from count
  const uniqueDevelopers = new Set(apis.map((api) => api.developer?.trim()).filter(Boolean)).size;

  // ── Render ────────────────────────────────────────────────────────────────
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 px-4 pt-8 pb-4 md:px-8 lg:px-12">
      <div className="w-full">

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
              {/* Header KPI counters — always show full dataset totals */}
              <div className="grid grid-cols-3 gap-3">
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

        {/* Global alert banners */}
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

        {/* Stats tab — passes full unfiltered api list; StatsTab manages its own filters */}
        {activeTab === "stats" && <StatsTab apis={apis} />}

        {/* Directory tab */}
        {activeTab === "directory" && (
          <>
            {/* ── Compare toolbar — sticky so it stays visible while scrolling ── */}
            {compareIds.length > 0 && (
              <div className="mb-6 flex flex-wrap items-center justify-between gap-4 rounded-[20px] border border-blue-200 bg-blue-50/95 px-5 py-4 shadow-md backdrop-blur"
                style={{ position: "sticky", top: 8, zIndex: 100 }}>
                <div className="flex flex-wrap items-center gap-3">
                  <span className="rounded-full bg-blue-600 px-3 py-1 text-xs font-bold text-white">{compareIds.length} selected</span>
                  <span className={`text-sm font-medium ${compareIds.length >= 4 ? "text-red-600 font-bold" : "text-blue-800"}`}>
                    {compareIds.length < 2 ? `Select ${2 - compareIds.length} more to compare`
                      : compareIds.length < 4 ? `Ready — or add up to ${4 - compareIds.length} more`
                      : "⛔ Maximum 4 APIs selected — remove one to add another"}
                  </span>
                  {/* Chips for each selected API with individual remove buttons */}
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

            {/* ── Search, filter and action toolbar ── */}
            <div className="mb-4 rounded-[24px] border border-slate-200/80 bg-white p-4 shadow-sm">
              <div className="flex flex-wrap items-center gap-3">
                {/* Search input — flexible width, fills available space */}
                <input type="text"
                  placeholder="Search by name, category, language, framework..."
                  value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)}
                  className="min-w-0 rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-sm text-slate-800 outline-none transition focus:border-blue-400 focus:bg-white focus:ring-2 focus:ring-blue-100"
                  style={{ flex: "1 1 0" }} />
                {/* Category filter dropdown */}
                <select value={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)}
                  className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-700 outline-none transition">
                  <option value="All">All Categories</option>
                  {categories.filter((c) => c !== "All").map((c) => <option key={c} value={c}>{c}</option>)}
                </select>
                {/* Sort order dropdown */}
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
                {/* Reset all filters button */}
                <button onClick={() => { setSearchTerm(""); setSelectedCategory("All"); setSortBy("default"); }}
                  className="rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm font-semibold text-slate-500 transition hover:bg-slate-50">
                  Reset
                </button>
                {/* Result count badge */}
                <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-500">
                  {sortedFilteredApis.length} result{sortedFilteredApis.length !== 1 ? "s" : ""}
                </span>
                {/* Right-side actions: export + add */}
                <div className="ml-auto flex items-center gap-3">
                  <div style={{ width: 1, height: 24, background: "#e2e8f0", flexShrink: 0 }} />
                  {/* Dynamic CSV export button — colour changes based on whether filters are active */}
                  <button onClick={exportToCSV}
                    className={`rounded-xl px-3 py-2.5 text-xs font-bold transition ${
                      searchTerm || selectedCategory !== "All"
                        ? "border border-blue-200 bg-blue-50 text-blue-700 hover:bg-blue-100"
                        : "border border-emerald-200 bg-emerald-50 text-emerald-700 hover:bg-emerald-100"
                    }`}>
                    ⬇ {searchTerm || selectedCategory !== "All"
                      ? `Export ${sortedFilteredApis.length} Results (CSV)`
                      : `Export All ${sortedFilteredApis.length} (CSV)`}
                  </button>
                  <button
                    onClick={() => { resetForm(); setShowDrawer(true); }}
                    className="rounded-2xl bg-blue-600 px-5 py-2.5 text-sm font-bold text-white shadow-md transition hover:bg-blue-700 hover:shadow-lg"
                  >
                    + Add New API
                  </button>
                </div>
              </div>
            </div>

            {/* ── Cards section header ── */}
            {/* Hint text on the right reminds users they can select cards to compare */}
            <div className="mb-3 flex items-center justify-between">
              <h2 className="text-lg font-bold text-slate-800">Available APIs</h2>
              <p className="text-xs text-slate-400">Check boxes to compare</p>
            </div>

            {/* Loading skeleton — shown while the initial fetch is in progress */}
            {loading && (
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
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

            {/* Empty state — shown when search/filter returns no results */}
            {!loading && sortedFilteredApis.length === 0 && (
              <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-12 text-center shadow-sm">
                <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-slate-100 text-2xl">🔎</div>
                <h3 className="mt-3 text-lg font-semibold text-slate-800">No APIs found</h3>
                <p className="mt-1 text-sm text-slate-500">Try a different search term or add a new entry.</p>
              </div>
            )}

            {/* ── API card grid ── */}
            {/* alignItems stretch ensures all cards in a row have equal height */}
            {!loading && sortedFilteredApis.length > 0 && (
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4" style={{ alignItems: "stretch" }}>
                {paginatedApis.map((api) => {
                  // Card display state — drives styling and overlay visibility
                  const isSelected = compareIds.includes(api.id);
                  const isDisabled = !isSelected && compareIds.length >= 4; // max 4 in compare
                  const isExpanded = expandedId === api.id;

                  // Count optional fields that are missing or have placeholder values
                  // Used to show the "⚠ N missing" or "✓ Complete" badge on each card
                  const optionalFields = [api.programming_language, api.framework, api.cost, api.latency, api.scalability, api.design_pattern, api.sample_code];
                  const missingCount = optionalFields.filter((v) => !v || v === "Unknown" || v === "N/A").length;

                  return (
                    <div key={api.id} id={`api-${api.id}`}
                      className="rounded-2xl border bg-white shadow-sm transition duration-200 hover:shadow-md"
                      style={{
                        borderColor: isSelected ? "#3b82f6" : "#e2e8f0",
                        boxShadow: isSelected ? "0 0 0 2px rgba(59,130,246,0.2)" : undefined,
                        position: "relative",
                        opacity: isDisabled ? 0.6 : 1,
                        display: "flex",
                        flexDirection: "column",
                      }}>

                      {/* ── Disabled overlay — shown when 4 APIs are already selected ── */}
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
                        {/* Top row: compare checkbox + completeness badge */}
                        <div className="mb-2 flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            {/* Custom checkbox — clicking toggles compare selection */}
                            <div onClick={() => !isDisabled && toggleCompare(api.id)}
                              className="flex h-4 w-4 flex-shrink-0 items-center justify-center rounded border-2 transition-all"
                              style={{ borderColor: isSelected ? "#3b82f6" : isDisabled ? "#e2e8f0" : "#94a3b8", background: isSelected ? "#3b82f6" : "white", cursor: isDisabled ? "not-allowed" : "pointer" }}>
                              {isSelected && <svg width="8" height="6" viewBox="0 0 10 8" fill="none"><path d="M1 4L3.5 6.5L9 1" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/></svg>}
                            </div>
                            <span className="text-xs" style={{ color: isSelected ? "#3b82f6" : "#94a3b8" }}>
                              {isSelected ? "Selected" : "Compare"}
                            </span>
                          </div>
                          {/* Completeness badge — amber warning or green complete */}
                          {missingCount > 0
                            ? <span className="rounded-full border border-amber-200 bg-amber-50 px-2 py-0.5 text-xs font-semibold text-amber-600">⚠ {missingCount} missing</span>
                            : <span className="rounded-full border border-emerald-200 bg-emerald-50 px-2 py-0.5 text-xs font-semibold text-emerald-600">✓ Complete</span>
                          }
                        </div>

                        {/* API name */}
                        <h3 className="truncate text-base font-bold text-slate-900">{api.name}</h3>

                        {/* Category, version, and risk badges */}
                        <div className="mt-1.5 flex flex-wrap gap-1.5">
                          <span className="rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-semibold text-blue-700">{api.category}</span>
                          <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-semibold text-slate-600">{api.version}</span>
                          <span className={`rounded-full px-2.5 py-0.5 text-xs font-semibold ${getRiskBadgeClass(api.risk_level)}`}>{api.risk_level || "Medium"} Risk</span>
                        </div>

                        {/* Description — truncated to 2 lines */}
                        <p className="mt-2 text-xs leading-5 text-slate-500 line-clamp-2">{api.description}</p>

                        {/* Key metadata row — developer, language, cost shown inline */}
                        {/* Amber italic text signals missing or unknown values */}
                        <div className="mt-2 flex flex-wrap gap-x-3 gap-y-1">
                          {[["Dev", api.developer], ["Lang", api.programming_language], ["Cost", api.cost]].map(([label, val]) => (
                            <span key={label} className="text-xs text-slate-500">
                              <span className="font-semibold text-slate-400">{label}:</span>{" "}
                              <span className={val && val !== "Unknown" ? "text-slate-700" : "text-amber-400 italic"}>{val || "—"}</span>
                            </span>
                          ))}
                        </div>
                      </div>

                      {/* ── Expandable details section ── */}
                      {isExpanded && (
                        <div className="border-t border-slate-100 px-4 py-3">
                          {/* Secondary metadata grid — framework, latency, scalability, pattern */}
                          <div className="grid grid-cols-2 gap-x-3 gap-y-2 text-xs">
                            {[["Framework", api.framework],["Latency", api.latency],["Scalability", api.scalability],["Design Pattern", api.design_pattern]].map(([label, val]) => (
                              <div key={label}>
                                <p className="font-semibold uppercase tracking-wide text-slate-400">{label}</p>
                                <p className={val && val !== "Unknown" ? "font-medium text-slate-800" : "italic text-amber-400"}>{val || "Missing"}</p>
                              </div>
                            ))}
                          </div>
                          {/* Sample code block — only shown if the entry has code */}
                          {api.sample_code && (
                            <div className="mt-3">
                              <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-400">Sample Code</p>
                              <pre className="overflow-x-auto rounded-xl bg-slate-900 p-3 text-xs text-slate-100 max-h-32">{api.sample_code}</pre>
                            </div>
                          )}
                        </div>
                      )}

                      {/* ── Card action buttons ── */}
                      <div className="mt-auto flex items-center justify-between border-t border-slate-100 px-4 py-2.5">
                        {/* Toggle details expand/collapse */}
                        <button
                          onClick={() => setExpandedId(isExpanded ? null : api.id)}
                          className="text-xs font-semibold text-blue-500 transition hover:text-blue-700"
                        >
                          {isExpanded ? "▲ Less" : "▼ Details"}
                        </button>
                        <div className="flex gap-1.5">
                          <button onClick={() => handleEdit(api)} className="rounded-lg bg-amber-500 px-2.5 py-1 text-xs font-semibold text-white transition hover:bg-amber-600">Edit</button>
                          <button onClick={() => handleDelete(api.id)} className="rounded-lg bg-red-500 px-2.5 py-1 text-xs font-semibold text-white transition hover:bg-red-600">Delete</button>
                          {/* Share link — shows checkmark briefly after copying */}
                          <button onClick={() => copyShareLink(api.id)} className="rounded-lg border border-slate-200 bg-white px-2.5 py-1 text-xs font-semibold text-slate-600 transition hover:bg-slate-50">
                            {copiedId === api.id ? "✓" : "🔗"}
                          </button>
                          {/* Print — opens a formatted print view in a new tab */}
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

            {/* ── Smart pagination with dots ── */}
            {totalPages > 1 && (
              <div className="mt-10 flex items-center justify-center gap-2 flex-wrap">
                {/* Previous page button */}
                <button
                  onClick={() => { setCurrentPage((p) => Math.max(1, p - 1)); window.scrollTo({ top: 0, behavior: "smooth" }); }}
                  disabled={currentPage === 1}
                  className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed">
                  ← Prev
                </button>

                {/* Page number buttons with dots — always shows first, last, and 2 neighbours around current */}
                {Array.from({ length: totalPages }, (_, i) => i + 1)
                  .filter((page) => {
                    return (
                      page === 1 ||
                      page === totalPages ||
                      (page >= currentPage - 2 && page <= currentPage + 2)
                    );
                  })
                  .reduce((acc, page, idx, arr) => {
                    // Insert "..." between non-consecutive page numbers
                    if (idx > 0 && page - arr[idx - 1] > 1) {
                      acc.push("...");
                    }
                    acc.push(page);
                    return acc;
                  }, [])
                  .map((item, idx) =>
                    item === "..." ? (
                      <span key={`dots-${idx}`} className="px-2 text-sm font-semibold text-slate-400">
                        ...
                      </span>
                    ) : (
                      <button
                        key={item}
                        onClick={() => { setCurrentPage(item); window.scrollTo({ top: 0, behavior: "smooth" }); }}
                        className="rounded-xl border px-4 py-2 text-sm font-bold transition"
                        style={{
                          background: currentPage === item ? "#3b82f6" : "white",
                          color: currentPage === item ? "white" : "#64748b",
                          borderColor: currentPage === item ? "#3b82f6" : "#e2e8f0",
                        }}>
                        {item}
                      </button>
                    )
                  )}

                {/* Next page button */}
                <button
                  onClick={() => { setCurrentPage((p) => Math.min(totalPages, p + 1)); window.scrollTo({ top: 0, behavior: "smooth" }); }}
                  disabled={currentPage === totalPages}
                  className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed">
                  Next →
                </button>

                {/* Page info label */}
                <span className="ml-2 text-sm text-slate-400">
                  Page {currentPage} of {totalPages} · {sortedFilteredApis.length} total
                </span>
              </div>
            )}
          </>
        )}
      </div>

      {/* ── Slide-in form drawer ── */}
      {showDrawer && (
        <div style={{ position: "fixed", inset: 0, zIndex: 500 }}>
          {/* Semi-transparent backdrop — clicking closes the drawer */}
          <div onClick={() => { if (!editId) resetForm(); else setShowDrawer(false); }}
            style={{ position: "absolute", inset: 0, background: "rgba(15,23,42,0.4)", backdropFilter: "blur(3px)" }} />
          {/* Drawer panel — slides in from the right */}
          <div style={{
            position: "absolute", top: 0, right: 0, bottom: 0, width: "100%", maxWidth: 480,
            background: "#fff", boxShadow: "-8px 0 40px rgba(0,0,0,0.15)",
            overflowY: "auto", display: "flex", flexDirection: "column",
          }}>
            {/* Drawer header — sticky so it stays visible while scrolling the form */}
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

            {/* Drawer form body */}
            <div style={{ padding: "20px 24px", flex: 1 }}>
              <form onSubmit={(e) => { handleSubmit(e); }} className="space-y-4">

                {/* GitHub auto-fill section */}
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

                {/* Required text fields — name and category */}
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

                {/* Description textarea */}
                <div>
                  <label className="mb-1.5 block text-sm font-semibold text-slate-700">Description</label>
                  <textarea name="description" placeholder="Short description..." value={formData.description} onChange={handleChange} required rows={3}
                    className="w-full resize-none rounded-xl border border-slate-300 bg-slate-50 px-3 py-2.5 text-sm text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-100" />
                </div>

                {/* Two-column grid for shorter optional fields */}
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

                {/* Sample code textarea with generate button */}
                <div>
                  <div className="mb-1.5 flex items-center justify-between">
                    <label className="text-sm font-semibold text-slate-700">Sample Code</label>
                    <button type="button"
                      onClick={() => {
                        // Confirm before overwriting existing code in edit mode
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

                {/* ── Inline drawer error card ── */}
                {drawerError && (
                  <div style={{
                    position: "relative", overflow: "hidden",
                    display: "flex", alignItems: "flex-start", gap: 10,
                    background: "#fef2f2", border: "1px solid #fca5a5",
                    borderRadius: 12, padding: "10px 12px",
                  }}>
                    {/* Red circle icon */}
                    <div style={{
                      width: 22, height: 22, borderRadius: "50%",
                      background: "#dc2626", display: "flex",
                      alignItems: "center", justifyContent: "center",
                      flexShrink: 0, marginTop: 1,
                    }}>
                      <span style={{ color: "#fff", fontSize: 11, fontWeight: 700 }}>✕</span>
                    </div>
                    {/* Error message text */}
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <p style={{ margin: 0, fontSize: 12, fontWeight: 700, color: "#991b1b" }}>Entry already exists</p>
                      <p style={{ margin: "2px 0 0 0", fontSize: 11, color: "#b91c1c" }}>{drawerError}</p>
                    </div>
                    {/* Manual close button */}
                    <button
                      type="button"
                      onClick={() => { if (drawerErrorTimer.current) clearTimeout(drawerErrorTimer.current); setDrawerError(""); }}
                      style={{
                        background: "rgba(220,38,38,0.12)", border: "none", borderRadius: 5,
                        color: "#dc2626", fontSize: 11, width: 18, height: 18,
                        display: "flex", alignItems: "center", justifyContent: "center",
                        cursor: "pointer", flexShrink: 0, padding: 0,
                      }}>
                      ✕
                    </button>
                    {/* Animated progress bar — shows time remaining before auto-dismiss */}
                    <div style={{
                      position: "absolute", bottom: 0, left: 0,
                      height: 3, background: "#fca5a5",
                      borderRadius: "0 0 0 12px",
                      animation: "drawerErrorProgress 5s linear forwards",
                    }} />
                    <style>{`@keyframes drawerErrorProgress { from { width: 100%; } to { width: 0%; } }`}</style>
                  </div>
                )}

                {/* Form action buttons */}
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

      {/* ── Bottom-right success/error toast ── */}
      {toast && (
        <div style={{
          position: "fixed", bottom: 32, right: 32,
          zIndex: 9999,
          background: toast.type === "success" ? "#15803d" : "#b91c1c",
          color: "#fff",
          borderRadius: 14,
          padding: "14px 18px",
          boxShadow: "0 8px 32px rgba(0,0,0,0.2)",
          display: "flex", alignItems: "flex-start", gap: 12,
          width: 320,
          border: "1.5px solid rgba(255,255,255,0.2)",
          overflow: "hidden",
          animation: "toastSlideIn 0.3s ease-out",
        }}>
          {/* Success/error icon */}
          <div style={{
            width: 24, height: 24, borderRadius: "50%",
            background: "rgba(255,255,255,0.25)",
            display: "flex", alignItems: "center", justifyContent: "center",
            flexShrink: 0, fontSize: 12, fontWeight: 700, marginTop: 1,
          }}>
            {toast.type === "success" ? "✓" : "✕"}
          </div>
          {/* Toast message */}
          <div style={{ flex: 1, minWidth: 0 }}>
            <p style={{ margin: 0, fontSize: 14, fontWeight: 700, color: "#fff" }}>
              {toast.type === "success" ? "Saved successfully" : "Something went wrong"}
            </p>
            <p style={{ margin: "3px 0 0 0", fontSize: 12, color: "rgba(255,255,255,0.78)" }}>
              {toast.message}
            </p>
          </div>
          {/* Manual close button */}
          <button
            onClick={() => setToast(null)}
            style={{
              background: "rgba(255,255,255,0.18)", border: "none", borderRadius: 6,
              color: "#fff", cursor: "pointer", fontSize: 13, fontWeight: 700,
              width: 22, height: 22, display: "flex", alignItems: "center",
              justifyContent: "center", flexShrink: 0, padding: 0, marginTop: 1,
            }}>
            ✕
          </button>
          {/* Animated countdown progress bar */}
          <div style={{
            position: "absolute", bottom: 0, left: 0,
            height: 3, background: "rgba(255,255,255,0.35)",
            animation: "toastProgress 5s linear forwards",
          }} />
          <style>{`
            @keyframes toastSlideIn { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes toastProgress { from { width: 100%; } to { width: 0%; } }
          `}</style>
        </div>
      )}

      {/* Back to Top floating button */}
      <BackToTop />

      {/* ── Compare limit toast — centred bottom, shown when user tries to select a 5th API ── */}
      {showCompareLimit && (
        <div style={{
          position: "fixed", bottom: 32, left: "50%", transform: "translateX(-50%)",
          zIndex: 9999,
          background: "linear-gradient(135deg, #dc2626, #b91c1c)",
          color: "#fff", borderRadius: 20,
          padding: "16px 28px",
          boxShadow: "0 12px 48px rgba(220,38,38,0.45), 0 4px 16px rgba(0,0,0,0.3)",
          display: "flex", alignItems: "center", gap: 12,
          fontSize: 15, fontWeight: 700,
          whiteSpace: "nowrap",
          border: "2px solid rgba(255,255,255,0.2)",
          minWidth: 360, justifyContent: "center",
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

      {/* Compare modal — full-screen side-by-side view */}
      {showCompare && compareApis.length >= 2 && (
        <CompareModal apis={compareApis} onClose={() => setShowCompare(false)} />
      )}

      {/* Review modal — shown after a GitHub fetch to complete missing fields */}
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