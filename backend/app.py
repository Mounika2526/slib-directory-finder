from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

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
            "developer": api.developer
        })

    return jsonify(result)


@app.route("/api/apis", methods=["POST"])
def add_api():
    data = request.get_json()

    new_api = ApiEntry(
        name=data["name"],
        category=data["category"],
        description=data["description"],
        version=data["version"],
        developer=data["developer"]
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

    api.name = data["name"]
    api.category = data["category"]
    api.description = data["description"]
    api.version = data["version"]
    api.developer = data["developer"]

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


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)