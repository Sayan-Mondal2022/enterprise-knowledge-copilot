from flask import Flask, request, jsonify
from flask_cors import CORS
from endee import Endee, Precision

app = Flask(__name__)
CORS(app)

# Initialize Endee client
client = Endee()

# -----------------------------
# Create Index
@app.route("/index/create", methods=["POST"])
def create_index():
    data = request.get_json()

    name = data.get("name")
    dimension = data.get("dimension")
    space_type = data.get("space_type", "cosine")
    precision = data.get("precision", "INT8D")

    client.create_index(
        name=name,
        dimension=dimension,
        space_type=space_type,
        precision=Precision[precision]
    )

    return jsonify({"status": "index created", "index_name": name})


# -----------------------------
# Get Index: (Mostly called internally, but can be used for validation)
@app.route("/index/get", methods=["POST"])
def get_index():
    data = request.get_json()
    name = data.get("name")

    index = client.get_index(name=name)

    return jsonify({"status": "index loaded", "index_name": name})


# -----------------------------
# Upsert Embedded Vectors
@app.route("/index/upsert", methods=["POST"])
def upsert_vectors():
    data = request.get_json()

    index_name = data.get("index_name")
    embedded_vectors = data.get("embedded_vectors")

    index = client.get_index(name=index_name)
    index.upsert(embedded_vectors)

    return jsonify({"status": "vectors upserted", "count": len(embedded_vectors)})


# -----------------------------
# Query Index
@app.route("/index/query", methods=["POST"])
def query_index():
    data = request.get_json()

    index_name = data.get("index_name")
    vector = data.get("vector")
    top_k = data.get("top_k", 5)
    include_vectors = data.get("include_vectors", False)

    index = client.get_index(name=index_name)

    raw_results = index.query(
        vector=vector,
        top_k=top_k,
        include_vectors=include_vectors
    )

    # Normalize response
    cleaned_results = [
        {
            "id": r.get("id"),
            "similarity": r.get("similarity"),
            "distance": r.get("distance"),
            "text": r.get("meta", {}).get("content"),
        }
        for r in raw_results
    ]

    return jsonify({
        "index_name": index_name,
        "top_k": top_k,
        "results": cleaned_results
    })


# -----------------------------
# Run Server
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)