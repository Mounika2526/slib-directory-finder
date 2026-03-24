import { useEffect, useState } from "react";

function App() {
  const [apis, setApis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchTerm, setSearchTerm] = useState("");

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

    fetch("http://127.0.0.1:5000/api/apis")
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

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:5000/api/apis", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        throw new Error("Failed to add API");
      }

      setFormData({
        name: "",
        category: "",
        description: "",
        version: "",
        developer: "",
      });

      fetchApis();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (id) => {
    setError("");

    try {
      const res = await fetch(`http://127.0.0.1:5000/api/apis/${id}`, {
        method: "DELETE",
      });

      if (!res.ok) {
        throw new Error("Failed to delete API");
      }

      fetchApis();
    } catch (err) {
      setError(err.message);
    }
  };

  const filteredApis = apis.filter((api) =>
    api.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    api.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
    api.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
    api.version.toLowerCase().includes(searchTerm.toLowerCase()) ||
    api.developer.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div
      style={{
        padding: "30px",
        fontFamily: "Arial",
        maxWidth: "900px",
        margin: "0 auto",
      }}
    >
      <h1>SBOM Finder</h1>

      <h2>Add New API</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: "30px" }}>
        <input
          type="text"
          name="name"
          placeholder="API Name"
          value={formData.name}
          onChange={handleChange}
          required
          style={{
            display: "block",
            marginBottom: "10px",
            width: "100%",
            padding: "8px",
          }}
        />
        <input
          type="text"
          name="category"
          placeholder="Category"
          value={formData.category}
          onChange={handleChange}
          required
          style={{
            display: "block",
            marginBottom: "10px",
            width: "100%",
            padding: "8px",
          }}
        />
        <input
          type="text"
          name="description"
          placeholder="Description"
          value={formData.description}
          onChange={handleChange}
          required
          style={{
            display: "block",
            marginBottom: "10px",
            width: "100%",
            padding: "8px",
          }}
        />
        <input
          type="text"
          name="version"
          placeholder="Version"
          value={formData.version}
          onChange={handleChange}
          required
          style={{
            display: "block",
            marginBottom: "10px",
            width: "100%",
            padding: "8px",
          }}
        />
        <input
          type="text"
          name="developer"
          placeholder="Developer"
          value={formData.developer}
          onChange={handleChange}
          required
          style={{
            display: "block",
            marginBottom: "10px",
            width: "100%",
            padding: "8px",
          }}
        />

        <button type="submit" style={{ padding: "10px 16px" }}>
          Add API
        </button>
      </form>

      <h2>Search APIs</h2>
      <input
        type="text"
        placeholder="Search by name, category, description, version, or developer"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        style={{
          display: "block",
          marginBottom: "20px",
          width: "100%",
          padding: "10px",
        }}
      />

      <h2>Available APIs</h2>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {!loading && !error && filteredApis.length === 0 && <p>No APIs found.</p>}

      {!loading && !error && filteredApis.length > 0 && (
        <div>
          {filteredApis.map((api) => (
            <div
              key={api.id}
              style={{
                border: "1px solid #ccc",
                padding: "15px",
                marginBottom: "15px",
                borderRadius: "8px",
              }}
            >
              <h3>{api.name}</h3>
              <p><strong>Category:</strong> {api.category}</p>
              <p><strong>Description:</strong> {api.description}</p>
              <p><strong>Version:</strong> {api.version}</p>
              <p><strong>Developer:</strong> {api.developer}</p>

              <button
                onClick={() => handleDelete(api.id)}
                style={{
                  marginTop: "10px",
                  padding: "6px 12px",
                  backgroundColor: "red",
                  color: "white",
                  border: "none",
                  borderRadius: "4px",
                  cursor: "pointer",
                }}
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;