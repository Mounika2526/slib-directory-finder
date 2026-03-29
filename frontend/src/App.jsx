import { useEffect, useMemo, useState } from "react";

function App() {
  const [apis, setApis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [editId, setEditId] = useState(null);

  const [formData, setFormData] = useState({
    name: "",
    category: "",
    description: "",
    version: "",
    developer: "",
  });

  const fetchApis = () => {
    setLoading(true);
    setError("");

    fetch("https://slib-directory-finder.onrender.com/api/apis")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch APIs");
        }
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

  useEffect(() => {
    fetchApis();
  }, []);

  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => {
        setSuccessMessage("");
      }, 2500);

      return () => clearTimeout(timer);
    }
  }, [successMessage]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const resetForm = () => {
    setFormData({
      name: "",
      category: "",
      description: "",
      version: "",
      developer: "",
    });
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

      const res = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        throw new Error(editId ? "Failed to update API" : "Failed to add API");
      }

      setSuccessMessage(
        editId ? "API updated successfully." : "API added successfully."
      );
      resetForm();
      fetchApis();
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id) => {
    const confirmed = window.confirm("Are you sure you want to delete this API?");
    if (!confirmed) return;

    setError("");
    setSuccessMessage("");

    try {
      const res = await fetch(
        `https://slib-directory-finder.onrender.com/api/apis/${id}`,
        {
          method: "DELETE",
        }
      );

      if (!res.ok) {
        throw new Error("Failed to delete API");
      }

      setSuccessMessage("API deleted successfully.");
      fetchApis();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleEdit = (api) => {
    setFormData({
      name: api.name || "",
      category: api.category || "",
      description: api.description || "",
      version: api.version || "",
      developer: api.developer || "",
    });
    setEditId(api.id);
    setSuccessMessage("");
    setError("");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const categories = useMemo(() => {
    const uniqueCategories = [
      ...new Set(
        apis.map((api) => api.category?.trim()).filter(Boolean)
      ),
    ].sort();

    return ["All", ...uniqueCategories];
  }, [apis]);

  const filteredApis = useMemo(() => {
    return apis.filter((api) => {
      const matchesSearch =
        api.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        api.category?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        api.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        api.version?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        api.developer?.toLowerCase().includes(searchTerm.toLowerCase());

      const matchesCategory =
        selectedCategory === "All" || api.category === selectedCategory;

      return matchesSearch && matchesCategory;
    });
  }, [apis, searchTerm, selectedCategory]);

  const totalApis = apis.length;
  const totalCategories = Math.max(categories.length - 1, 0);
  const uniqueDevelopers = new Set(
    apis.map((api) => api.developer?.trim()).filter(Boolean)
  ).size;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 px-4 py-8 md:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
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
                  <p className="text-xs uppercase tracking-wide text-slate-300">
                    Total APIs
                  </p>
                  <p className="mt-2 text-2xl font-bold">{totalApis}</p>
                </div>
                <div className="rounded-2xl border border-white/15 bg-white/10 p-4">
                  <p className="text-xs uppercase tracking-wide text-slate-300">
                    Categories
                  </p>
                  <p className="mt-2 text-2xl font-bold">{totalCategories}</p>
                </div>
                <div className="rounded-2xl border border-white/15 bg-white/10 p-4">
                  <p className="text-xs uppercase tracking-wide text-slate-300">
                    Developers
                  </p>
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

        <div className="grid gap-8 lg:grid-cols-3">
          <div className="lg:col-span-1">
            <div className="sticky top-6 rounded-[28px] border border-slate-200/80 bg-white p-6 shadow-lg">
              <div className="mb-6">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <h2 className="text-2xl font-bold text-slate-900">
                      {editId ? "Edit API Entry" : "Add New API"}
                    </h2>
                    <p className="mt-1 text-sm text-slate-500">
                      Enter the API details below.
                    </p>
                  </div>
                  {editId && (
                    <span className="rounded-full bg-amber-100 px-3 py-1 text-xs font-semibold text-amber-700">
                      Editing
                    </span>
                  )}
                </div>
              </div>

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="mb-2 block text-sm font-semibold text-slate-700">
                    API Name
                  </label>
                  <input
                    type="text"
                    name="name"
                    placeholder="Ex: Stripe API"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-sm font-semibold text-slate-700">
                    Category
                  </label>
                  <input
                    type="text"
                    name="category"
                    placeholder="Ex: Payments"
                    value={formData.category}
                    onChange={handleChange}
                    required
                    className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-sm font-semibold text-slate-700">
                    Description
                  </label>
                  <textarea
                    name="description"
                    placeholder="Write a short description about this API or microservice..."
                    value={formData.description}
                    onChange={handleChange}
                    required
                    rows={4}
                    className="w-full resize-none rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100"
                  />
                </div>

                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <label className="mb-2 block text-sm font-semibold text-slate-700">
                      Version
                    </label>
                    <input
                      type="text"
                      name="version"
                      placeholder="Ex: v1.0.0"
                      value={formData.version}
                      onChange={handleChange}
                      required
                      className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100"
                    />
                  </div>

                  <div>
                    <label className="mb-2 block text-sm font-semibold text-slate-700">
                      Developer
                    </label>
                    <input
                      type="text"
                      name="developer"
                      placeholder="Ex: Internal Team"
                      value={formData.developer}
                      onChange={handleChange}
                      required
                      className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100"
                    />
                  </div>
                </div>

                <div className="flex flex-wrap gap-3 pt-2">
                  <button
                    type="submit"
                    disabled={submitting}
                    className="rounded-2xl bg-blue-600 px-5 py-3 font-semibold text-white shadow-md transition hover:bg-blue-700 hover:shadow-lg disabled:cursor-not-allowed disabled:opacity-70"
                  >
                    {submitting
                      ? editId
                        ? "Updating..."
                        : "Adding..."
                      : editId
                      ? "Update API"
                      : "Add API"}
                  </button>

                  <button
                    type="button"
                    onClick={resetForm}
                    className="rounded-2xl border border-slate-300 bg-white px-5 py-3 font-semibold text-slate-700 transition hover:bg-slate-100"
                  >
                    Clear
                  </button>

                  {editId && (
                    <button
                      type="button"
                      onClick={resetForm}
                      className="rounded-2xl border border-amber-300 bg-amber-50 px-5 py-3 font-semibold text-amber-700 transition hover:bg-amber-100"
                    >
                      Cancel Edit
                    </button>
                  )}
                </div>
              </form>
            </div>
          </div>

          <div className="lg:col-span-2">
            <div className="mb-6 rounded-[28px] border border-slate-200/80 bg-white p-6 shadow-lg">
              <div className="mb-5 flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
                <div>
                  <h2 className="text-2xl font-bold text-slate-900">
                    Search & Filter
                  </h2>
                  <p className="mt-1 text-sm text-slate-500">
                    Find APIs by keyword or narrow them by category.
                  </p>
                </div>

                <div className="flex items-center gap-3 self-start xl:self-auto">
                  <div className="rounded-full bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700">
                    {filteredApis.length} result{filteredApis.length !== 1 ? "s" : ""}
                  </div>
                </div>
              </div>

              <div className="grid gap-4 md:grid-cols-[1.6fr_1fr_auto]">
                <input
                  type="text"
                  placeholder="Search by name, category, description, version, or developer"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100"
                />

                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition"
                >
                  <option value="All">All Categories</option>

                  {categories
                    .filter((cat) => cat !== "All")
                    .map((category) => (
                      <option key={category} value={category}>
                        {category}
                      </option>
                    ))}
                </select>

                <button
                  type="button"
                  onClick={() => {
                    setSearchTerm("");
                    setSelectedCategory("All");
                  }}
                  className="rounded-2xl border border-slate-300 bg-white px-5 py-3 font-semibold text-slate-700 transition hover:bg-slate-100"
                >
                  Reset
                </button>
              </div>
            </div>

            <div className="mb-4 flex items-center justify-between gap-4">
              <div>
                <h2 className="text-2xl font-bold text-slate-900">Available APIs</h2>
                <p className="mt-1 text-sm text-slate-500">
                  Browse and manage your saved API and microservice entries.
                </p>
              </div>
            </div>

            {loading && (
              <div className="grid gap-6 md:grid-cols-2">
                {[1, 2, 3, 4].map((item) => (
                  <div
                    key={item}
                    className="animate-pulse rounded-[28px] border border-slate-200 bg-white p-6 shadow-lg"
                  >
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
                <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-slate-100 text-2xl">
                  🔎
                </div>
                <h3 className="mt-4 text-xl font-semibold text-slate-800">
                  No APIs found
                </h3>
                <p className="mt-2 text-slate-500">
                  Try a different search term or add a new API entry.
                </p>
              </div>
            )}

            {!loading && filteredApis.length > 0 && (
              <div className="grid gap-6 md:grid-cols-2">
                {filteredApis.map((api) => (
                  <div
                    key={api.id}
                    className="group rounded-[28px] border border-slate-200 bg-white p-6 shadow-lg transition duration-300 hover:-translate-y-1 hover:shadow-2xl"
                  >
                    <div className="mb-5 flex items-start justify-between gap-3">
                      <div className="min-w-0">
                        <h3 className="truncate text-xl font-bold text-slate-900">
                          {api.name}
                        </h3>
                        <div className="mt-3 flex flex-wrap gap-2">
                          <span className="inline-block rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-700">
                            {api.category}
                          </span>
                          <span className="inline-block rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">
                            {api.version}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="space-y-4 text-sm text-slate-700">
                      <div>
                        <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">
                          Description
                        </p>
                        <p className="leading-6 text-slate-700">{api.description}</p>
                      </div>

                      <div>
                        <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">
                          Developer
                        </p>
                        <p className="font-medium text-slate-900">{api.developer}</p>
                      </div>
                    </div>

                    <div className="mt-6 flex gap-3">
                      <button
                        onClick={() => handleEdit(api)}
                        className="rounded-2xl bg-amber-500 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-amber-600"
                      >
                        Edit
                      </button>

                      <button
                        onClick={() => handleDelete(api.id)}
                        className="rounded-2xl bg-red-500 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-red-600"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;