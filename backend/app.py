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
        database_url = database_url.replace("postgres://", "postgresql://", 1)
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
            "risk_level": api.risk_level
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

    if not all([name, category, description, version, developer]):
        return jsonify({"error": "All fields are required"}), 400

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
        risk_level=calculate_risk(version)
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

    if not all([name, category, description, version, developer]):
        return jsonify({"error": "All fields are required"}), 400

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

    try:
        repo_res = requests.get(github_url, timeout=10)

        if repo_res.status_code != 200:
            return jsonify({"error": "GitHub repository not found"}), 404

        repo_data = repo_res.json()

        release_url = f"https://api.github.com/repos/{repo}/releases/latest"
        release_res = requests.get(release_url, timeout=10)

        version = "Not available"
        if release_res.status_code == 200:
            release_data = release_res.json()
            version = release_data.get("tag_name", "Not available")

        result = {
            "name": repo_data.get("name", ""),
            "category": repo_data.get("language", "Software Component") or "Software Component",
            "description": repo_data.get("description", "") or "No description available",
            "version": version,
            "developer": repo_data.get("owner", {}).get("login", "") or "Unknown",
            "risk_level": calculate_risk(version)
        }

        return jsonify(result), 200

    except requests.RequestException:
        return jsonify({"error": "Failed to connect to GitHub API"}), 500


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)