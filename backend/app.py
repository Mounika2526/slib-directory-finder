from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

# Database configuration
database_url = os.environ.get("DATABASE_URL")

if database_url:
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+pg8000://", 1)
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+pg8000://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "apis.db")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class ApiEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    version = db.Column(db.String(50), nullable=False)
    developer = db.Column(db.String(100), nullable=False)
    risk_level = db.Column(db.String(20), nullable=False, default="Medium")

    programming_language = db.Column(db.String(100), nullable=True)
    framework = db.Column(db.String(100), nullable=True)
    cost = db.Column(db.String(50), nullable=True)
    latency = db.Column(db.String(50), nullable=True)
    scalability = db.Column(db.String(100), nullable=True)
    design_pattern = db.Column(db.String(100), nullable=True)
    sample_code = db.Column(db.Text, nullable=True)


def calculate_risk(version):
    if not version or version.strip() == "":
        return "Medium"

    version = version.lower().strip()

    if version in ["not available", "unknown", "n/a"]:
        return "Medium"

    if version.startswith("v0") or version.startswith("0."):
        return "High"

    return "Low"


def normalize_text(value):
    return value.strip().lower() if value else ""


def detect_category(repo_data):
    topics = repo_data.get("topics", [])
    description = (repo_data.get("description") or "").lower()
    language = (repo_data.get("language") or "").lower()
    name = (repo_data.get("name") or "").lower()

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
        "blockchain": "Blockchain"
    }

    # 1. Try GitHub topics first
    for topic in topics:
        topic_lower = topic.lower()
        if topic_lower in topic_map:
            return topic_map[topic_lower]

    # 2. Try description keywords
    if "payment" in description or "billing" in description:
        return "Payments"
    if "auth" in description or "authentication" in description or "oauth" in description:
        return "Authentication"
    if "security" in description or "secure" in description:
        return "Security"
    if "machine learning" in description or "deep learning" in description or "artificial intelligence" in description or " ai " in f" {description} ":
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

    # 3. Try repo name keywords
    if "api" in name:
        return "API"
    if "auth" in name:
        return "Authentication"
    if "search" in name:
        return "Search"
    if "payment" in name:
        return "Payments"

    # 4. Fallback by programming language
    if language in ["javascript", "typescript", "html", "css"]:
        return "Frontend"
    if language in ["python", "java", "go", "ruby", "php", "c#", "rust"]:
        return "Backend"

    return "Software Tool"


@app.route("/")
def home():
    return jsonify({"message": "Backend is running!"})


@app.route("/api/test")
def test():
    return jsonify({"message": "API is working"})


@app.route("/api/apis", methods=["GET"])
def get_apis():
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
            "sample_code": api.sample_code
        })

    return jsonify(result)


@app.route("/api/apis", methods=["POST"])
def add_api():
    data = request.get_json()

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

    if not all([name, category, description, version, developer]):
        return jsonify({"error": "Name, category, description, version, and developer are required"}), 400

    existing_api = ApiEntry.query.filter(
        db.func.lower(ApiEntry.name) == normalize_text(name),
        db.func.lower(ApiEntry.developer) == normalize_text(developer)
    ).first()

    if existing_api:
        return jsonify({"error": "This API entry already exists"}), 409

    new_api = ApiEntry(
        name=name,
        category=category,
        description=description,
        version=version,
        developer=developer,
        risk_level=calculate_risk(version),
        programming_language=programming_language or None,
        framework=framework or None,
        cost=cost or None,
        latency=latency or None,
        scalability=scalability or None,
        design_pattern=design_pattern or None,
        sample_code=sample_code or None
    )

    db.session.add(new_api)
    db.session.commit()

    return jsonify({"message": "API added successfully"}), 201


@app.route("/api/apis/<int:id>", methods=["PUT"])
def update_api(id):
    api = ApiEntry.query.get(id)

    if not api:
        return jsonify({"error": "API not found"}), 404

    data = request.get_json()

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

    if not all([name, category, description, version, developer]):
        return jsonify({"error": "Name, category, description, version, and developer are required"}), 400

    duplicate_api = ApiEntry.query.filter(
        db.func.lower(ApiEntry.name) == normalize_text(name),
        db.func.lower(ApiEntry.developer) == normalize_text(developer),
        ApiEntry.id != id
    ).first()

    if duplicate_api:
        return jsonify({"error": "Another API entry with the same name and developer already exists"}), 409

    api.name = name
    api.category = category
    api.description = description
    api.version = version
    api.developer = developer
    api.risk_level = calculate_risk(version)

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
    api = ApiEntry.query.get(id)

    if not api:
        return jsonify({"error": "API not found"}), 404

    db.session.delete(api)
    db.session.commit()

    return jsonify({"message": "API deleted successfully"})


@app.route("/api/github-fetch", methods=["POST"])
def github_fetch():
    data = request.get_json()
    repo = data.get("repo", "").strip()

    if not repo:
        return jsonify({"error": "Repository is required. Use format owner/repo"}), 400

    if "/" not in repo:
        return jsonify({"error": "Invalid format. Use owner/repo"}), 400

    github_url = f"https://api.github.com/repos/{repo}"
    headers = {
        "Accept": "application/vnd.github.mercy-preview+json"
    }

    try:
        repo_res = requests.get(github_url, headers=headers, timeout=10)

        if repo_res.status_code != 200:
            return jsonify({"error": "GitHub repository not found"}), 404

        repo_data = repo_res.json()

        release_url = f"https://api.github.com/repos/{repo}/releases/latest"
        release_res = requests.get(release_url, headers=headers, timeout=10)

        version = "Not available"
        if release_res.status_code == 200:
            release_data = release_res.json()
            version = release_data.get("tag_name", "Not available")

        result = {
            "name": repo_data.get("name", ""),
            "category": detect_category(repo_data),
            "description": repo_data.get("description", "") or "No description available",
            "version": version,
            "developer": repo_data.get("owner", {}).get("login", "") or "Unknown",
            "risk_level": calculate_risk(version),
            "programming_language": repo_data.get("language", "") or "",
            "framework": "",
            "cost": "Unknown",
            "latency": "Unknown",
            "scalability": "Unknown",
            "design_pattern": "",
            "sample_code": ""
        }

        return jsonify(result), 200

    except requests.RequestException:
        return jsonify({"error": "Failed to connect to GitHub API"}), 500


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)