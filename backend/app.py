"""
app.py — Flask Backend for SLIB Finder: API & Microservices Directory

Provides a REST API for managing software library entries (APIs and microservices).

Endpoints:
    GET    /                        — Health check
    GET    /api/test                — API connectivity test
    GET    /api/apis                — Retrieve all API entries
    POST   /api/apis                — Create a new API entry
    PUT    /api/apis/<id>           — Update an existing API entry
    DELETE /api/apis/<id>           — Delete an API entry
    POST   /api/github-fetch        — Auto-fill form data from a GitHub repository

Database:
    - Uses SQLite locally (apis.db) for development
    - Supports PostgreSQL (via pg8000 driver) for production deployments (e.g. Render)
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import requests

# ─────────────────────────────────────────────
# APP INITIALIZATION
# ─────────────────────────────────────────────

app = Flask(__name__)

# Allow cross-origin requests from the React frontend (running on a different port/domain)
CORS(app)

# ─────────────────────────────────────────────
# DATABASE CONFIGURATION
# Supports both local SQLite and production PostgreSQL.
# The DATABASE_URL environment variable is set automatically by platforms like Render.
# ─────────────────────────────────────────────

database_url = os.environ.get("DATABASE_URL")

if database_url:
    # Render provides postgres:// URLs, but SQLAlchemy requires postgresql+pg8000://
    # so we rewrite the scheme accordingly
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+pg8000://", 1)
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+pg8000://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    # Fall back to a local SQLite database file for development
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "apis.db")

# Disable modification tracking to save memory (we don't need SQLAlchemy's event system)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ─────────────────────────────────────────────
# DATABASE MODEL
# Represents a single API or microservice entry in the directory.
# ─────────────────────────────────────────────

class ApiEntry(db.Model):
    """
    SQLAlchemy model for an API or microservice entry.

    Required fields: name, category, description, version, developer
    Optional fields: programming_language, framework, cost, latency,
                     scalability, design_pattern, sample_code
    Computed field:  risk_level (derived from version string)
    """

    id = db.Column(db.Integer, primary_key=True)

    # Core required fields
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    version = db.Column(db.String(50), nullable=False)
    developer = db.Column(db.String(100), nullable=False)

    # Risk level is computed from the version string on save/update
    risk_level = db.Column(db.String(20), nullable=False, default="Medium")

    # Optional metadata fields
    programming_language = db.Column(db.String(100), nullable=True)
    framework = db.Column(db.String(100), nullable=True)
    cost = db.Column(db.String(50), nullable=True)
    latency = db.Column(db.String(50), nullable=True)
    scalability = db.Column(db.String(100), nullable=True)
    design_pattern = db.Column(db.String(100), nullable=True)
    sample_code = db.Column(db.Text, nullable=True)  # Text allows longer code snippets


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def calculate_risk(version):
    """
    Derive a risk level string from a version identifier.

    Rules:
      - Empty / unknown / N/A versions → "Medium" (uncertain stability)
      - Versions starting with 0 (e.g. v0.9, 0.1.2) → "High" (pre-release / unstable)
      - All other versions → "Low" (assumed stable release)

    Args:
        version (str): Version string such as "v1.0.0", "0.3.1", "Not available"

    Returns:
        str: One of "Low", "Medium", or "High"
    """
    if not version or version.strip() == "":
        return "Medium"

    version = version.lower().strip()

    # Treat placeholder values as unknown → medium risk
    if version in ["not available", "unknown", "n/a"]:
        return "Medium"

    # Pre-release versions (major version 0) are considered high risk
    if version.startswith("v0") or version.startswith("0."):
        return "High"

    # Stable release
    return "Low"


def normalize_text(value):
    """
    Lowercase and strip whitespace from a string for case-insensitive comparisons.

    Args:
        value (str | None): Input string

    Returns:
        str: Normalized string, or empty string if value is None
    """
    return value.strip().lower() if value else ""


def detect_category(repo_data):
    """
    Infer the most appropriate category for a GitHub repository.

    Detection priority:
      1. Exact repo name match against known frameworks (e.g. "react" → "Frontend")
      2. GitHub topics (e.g. "microservice" → "Microservice")
      3. Keywords in the repository description
      4. Keywords in the repository name
      5. Primary programming language fallback

    Args:
        repo_data (dict): JSON response from the GitHub /repos/{owner}/{repo} endpoint

    Returns:
        str: Category label such as "API", "Microservice", "Frontend", "Payments", etc.
    """

    topics = repo_data.get("topics", [])
    description = (repo_data.get("description") or "").lower()
    language = (repo_data.get("language") or "").lower()
    name = (repo_data.get("name") or "").lower()

    # Priority 1: exact repo name → known framework category
    framework_map = {
        "flask": "Backend Framework",
        "django": "Backend Framework",
        "fastapi": "Backend Framework",
        "spring": "Backend Framework",
        "express": "Backend Framework",
        "rails": "Backend Framework",
        "laravel": "Backend Framework",
        "react": "Frontend",
        "vue": "Frontend",
        "angular": "Frontend",
    }
    if name in framework_map:
        return framework_map[name]

    # Priority 2: GitHub topic tags → category mapping
    topic_map = {
        "api": "API",
        "rest-api": "API",
        "rest": "API",
        "graphql": "API",
        "microservice": "Microservice",
        "microservices": "Microservice",
        "backend": "Backend",
        "frontend": "Frontend",
        "web": "Web Application",
        "website": "Web Application",
        "ai": "AI/ML",
        "ml": "AI/ML",
        "machine-learning": "AI/ML",
        "deep-learning": "AI/ML",
        "payment": "Payments",
        "payments": "Payments",
        "fintech": "Payments",
        "auth": "Authentication",
        "authentication": "Authentication",
        "oauth": "Authentication",
        "jwt": "Authentication",
        "security": "Security",
        "cybersecurity": "Security",
        "database": "Database",
        "sql": "Database",
        "cloud": "Cloud",
        "aws": "Cloud",
        "devops": "DevOps",
        "docker": "DevOps",
        "kubernetes": "DevOps",
        "analytics": "Analytics",
        "monitoring": "Monitoring",
        "search": "Search",
        "recommendation": "Recommendation System",
        "chatbot": "Chatbot",
        "iot": "IoT",
        "blockchain": "Blockchain",
    }

    for topic in topics:
        topic_lower = topic.lower()
        if topic_lower in topic_map:
            return topic_map[topic_lower]

    # Priority 3: scan the repository description for known keywords
    if "payment" in description or "billing" in description:
        return "Payments"
    if "auth" in description or "authentication" in description or "oauth" in description:
        return "Authentication"
    if "security" in description or "secure" in description:
        return "Security"
    if "machine learning" in description or "deep learning" in description \
            or "artificial intelligence" in description or " ai " in f" {description} ":
        return "AI/ML"
    if "analytics" in description or "dashboard" in description:
        return "Analytics"
    if "search" in description:
        return "Search"
    if "database" in description:
        return "Database"
    if "monitoring" in description:
        return "Monitoring"
    if "microservice" in description:
        return "Microservice"
    if "api" in description or "rest" in description or "graphql" in description:
        return "API"
    if "frontend" in description or "ui" in description:
        return "Frontend"
    if "backend" in description or "server" in description:
        return "Backend"

    # Priority 4: check repo name for common keywords
    if "api" in name:
        return "API"
    if "auth" in name:
        return "Authentication"
    if "search" in name:
        return "Search"
    if "payment" in name:
        return "Payments"

    # Priority 5: fall back to primary programming language
    if language in ["javascript", "typescript", "html", "css"]:
        return "Frontend"
    if language in ["python", "java", "go", "ruby", "php", "c#", "rust"]:
        return "Backend"

    # Default if nothing matched
    return "Software Tool"


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.route("/")
def home():
    """Health check — confirms the backend server is running."""
    return jsonify({"message": "Backend is running!"})


@app.route("/api/test")
def test():
    """Simple connectivity test endpoint for debugging deployments."""
    return jsonify({"message": "API is working"})


@app.route("/api/apis", methods=["GET"])
def get_apis():
    """
    Retrieve all API entries from the database.

    Returns:
        JSON array of all ApiEntry objects with all fields.
        HTTP 200 on success.
    """
    apis = ApiEntry.query.all()
    result = []

    for api in apis:
        result.append({
            "id": api.id,
            "name": api.name,
            "category": api.category,
            "description": api.description,
            "version": api.version,
            "developer": api.developer,
            "risk_level": api.risk_level,
            "programming_language": api.programming_language,
            "framework": api.framework,
            "cost": api.cost,
            "latency": api.latency,
            "scalability": api.scalability,
            "design_pattern": api.design_pattern,
            "sample_code": api.sample_code,
        })

    return jsonify(result)


@app.route("/api/apis", methods=["POST"])
def add_api():
    """
    Create a new API entry in the database.

    Request body (JSON):
        Required: name, category, description, version, developer
        Optional: programming_language, framework, cost, latency,
                  scalability, design_pattern, sample_code

    Returns:
        HTTP 201 with success message on creation.
        HTTP 400 if required fields are missing.
        HTTP 409 if an entry with the same name + developer already exists.
    """
    data = request.get_json()

    # Extract and sanitize required fields
    name = data.get("name", "").strip()
    category = data.get("category", "").strip()
    description = data.get("description", "").strip()
    version = data.get("version", "").strip()
    developer = data.get("developer", "").strip()

    # Extract optional fields (stored as None if empty)
    programming_language = data.get("programming_language", "").strip()
    framework = data.get("framework", "").strip()
    cost = data.get("cost", "").strip()
    latency = data.get("latency", "").strip()
    scalability = data.get("scalability", "").strip()
    design_pattern = data.get("design_pattern", "").strip()
    sample_code = data.get("sample_code", "").strip()

    # Validate that all required fields are present
    if not all([name, category, description, version, developer]):
        return jsonify({"error": "Name, category, description, version, and developer are required"}), 400

    # Prevent duplicate entries (same name + same developer, case-insensitive)
    existing_api = ApiEntry.query.filter(
        db.func.lower(ApiEntry.name) == normalize_text(name),
        db.func.lower(ApiEntry.developer) == normalize_text(developer)
    ).first()

    if existing_api:
        return jsonify({"error": "This API entry already exists"}), 409

    # Create and persist the new entry
    new_api = ApiEntry(
        name=name,
        category=category,
        description=description,
        version=version,
        developer=developer,
        risk_level=calculate_risk(version),      # computed from version string
        programming_language=programming_language or None,
        framework=framework or None,
        cost=cost or None,
        latency=latency or None,
        scalability=scalability or None,
        design_pattern=design_pattern or None,
        sample_code=sample_code or None,
    )

    db.session.add(new_api)
    db.session.commit()

    return jsonify({"message": "API added successfully"}), 201


@app.route("/api/apis/<int:id>", methods=["PUT"])
def update_api(id):
    """
    Update an existing API entry by its ID.

    URL parameter:
        id (int): Primary key of the entry to update

    Request body (JSON):
        Same fields as POST /api/apis. All required fields must be present.

    Returns:
        HTTP 200 with success message on update.
        HTTP 400 if required fields are missing.
        HTTP 404 if no entry with the given id exists.
        HTTP 409 if the updated name + developer conflicts with another entry.
    """
    api = ApiEntry.query.get(id)

    if not api:
        return jsonify({"error": "API not found"}), 404

    data = request.get_json()

    # Extract and sanitize all fields from request body
    name = data.get("name", "").strip()
    category = data.get("category", "").strip()
    description = data.get("description", "").strip()
    version = data.get("version", "").strip()
    developer = data.get("developer", "").strip()
    programming_language = data.get("programming_language", "").strip()
    framework = data.get("framework", "").strip()
    cost = data.get("cost", "").strip()
    latency = data.get("latency", "").strip()
    scalability = data.get("scalability", "").strip()
    design_pattern = data.get("design_pattern", "").strip()
    sample_code = data.get("sample_code", "").strip()

    # Validate required fields
    if not all([name, category, description, version, developer]):
        return jsonify({"error": "Name, category, description, version, and developer are required"}), 400

    # Check for duplicate name+developer on a DIFFERENT entry (exclude self)
    duplicate_api = ApiEntry.query.filter(
        db.func.lower(ApiEntry.name) == normalize_text(name),
        db.func.lower(ApiEntry.developer) == normalize_text(developer),
        ApiEntry.id != id  # exclude the current record from duplicate check
    ).first()

    if duplicate_api:
        return jsonify({"error": "Another API entry with the same name and developer already exists"}), 409

    # Apply changes to the existing record
    api.name = name
    api.category = category
    api.description = description
    api.version = version
    api.developer = developer
    api.risk_level = calculate_risk(version)  # recompute risk if version changed
    api.programming_language = programming_language or None
    api.framework = framework or None
    api.cost = cost or None
    api.latency = latency or None
    api.scalability = scalability or None
    api.design_pattern = design_pattern or None
    api.sample_code = sample_code or None

    db.session.commit()

    return jsonify({"message": "API updated successfully"})


@app.route("/api/apis/<int:id>", methods=["DELETE"])
def delete_api(id):
    """
    Delete an API entry by its ID.

    URL parameter:
        id (int): Primary key of the entry to delete

    Returns:
        HTTP 200 with success message on deletion.
        HTTP 404 if no entry with the given id exists.
    """
    api = ApiEntry.query.get(id)

    if not api:
        return jsonify({"error": "API not found"}), 404

    db.session.delete(api)
    db.session.commit()

    return jsonify({"message": "API deleted successfully"})


@app.route("/api/github-fetch", methods=["POST"])
def github_fetch():
    """
    Fetch metadata from a public GitHub repository and map it to ApiEntry fields.

    Used by the frontend's "Auto Fill" and "Fill & Save" buttons to pre-populate
    the add/edit form without manual data entry.

    Request body (JSON):
        repo (str): Repository in "owner/repo" format (e.g. "facebook/react")

    Process:
        1. Call GET /repos/{owner}/{repo} for general metadata
        2. Call GET /repos/{owner}/{repo}/releases/latest for version tag
        3. Infer category using detect_category()
        4. Compute risk_level using calculate_risk()

    Returns:
        HTTP 200 with a JSON object matching ApiEntry fields.
        HTTP 400 if repo format is invalid or missing.
        HTTP 404 if the GitHub repository does not exist.
        HTTP 500 if the GitHub API request fails (network error, timeout, etc.)
    """
    data = request.get_json()
    repo = data.get("repo", "").strip()

    # Validate input format
    if not repo:
        return jsonify({"error": "Repository is required. Use format owner/repo"}), 400

    if "/" not in repo:
        return jsonify({"error": "Invalid format. Use owner/repo"}), 400

    github_url = f"https://api.github.com/repos/{repo}"

    # Request GitHub topic data (requires mercy-preview media type header)
    headers = {
        "Accept": "application/vnd.github.mercy-preview+json"
    }

    try:
        # Step 1: Fetch main repository metadata
        repo_res = requests.get(github_url, headers=headers, timeout=10)

        if repo_res.status_code != 200:
            return jsonify({"error": "GitHub repository not found"}), 404

        repo_data = repo_res.json()

        # Step 2: Attempt to fetch the latest release tag for version info
        release_url = f"https://api.github.com/repos/{repo}/releases/latest"
        release_res = requests.get(release_url, headers=headers, timeout=10)

        version = "Not available"
        if release_res.status_code == 200:
            release_data = release_res.json()
            version = release_data.get("tag_name", "Not available")

        # Step 3: Build the response object using helper functions
        result = {
            "name": repo_data.get("name", ""),
            "category": detect_category(repo_data),          # inferred from topics/description
            "description": repo_data.get("description", "") or "No description available",
            "version": version,
            "developer": repo_data.get("owner", {}).get("login", "") or "Unknown",
            "risk_level": calculate_risk(version),            # computed from version string
            "programming_language": repo_data.get("language", "") or "",
            "framework": "",                                  # not available from GitHub API
            "cost": "Unknown",                                # not available from GitHub API
            "latency": "Unknown",                             # not available from GitHub API
            "scalability": "Unknown",                         # not available from GitHub API
            "design_pattern": "",                             # not available from GitHub API
            "sample_code": "",                                # not available from GitHub API
        }

        return jsonify(result), 200

    except requests.RequestException:
        # Covers connection errors, timeouts, and other network failures
        return jsonify({"error": "Failed to connect to GitHub API"}), 500


# ─────────────────────────────────────────────
# DATABASE INITIALIZATION
# Creates all tables defined by SQLAlchemy models
# if they don't already exist (safe to run repeatedly)
# ─────────────────────────────────────────────

with app.app_context():
    db.create_all()


# ─────────────────────────────────────────────
# ONE-TIME AUTO SEED
# Imports the seed function from seed_data.py and runs it.
# The seed function checks if data already exists — if yes,
# it skips immediately. Runs once on first deploy, never again.
# ─────────────────────────────────────────────

with app.app_context():
    try:
        from seed_data import seed
        seed()
    except Exception as e:
        print(f"[SEED] Skipped: {e}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
