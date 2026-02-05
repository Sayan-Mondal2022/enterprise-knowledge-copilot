from flask import Flask, request, jsonify
from flask_cors import CORS
from endee import Endee, Precision
from validators import (
    validate_index_name, 
    validate_dimension, 
    validate_vector, 
    validate_top_k, 
    validate_choice
)

app = Flask(__name__)
CORS(app)

# Initialize Endee client
client = Endee()

# get_json can return None if the body is not valid JSON, so we can use a helper function to handle that case
def get_json_or_error():
    data = request.get_json(silent=True)
    if not data:
        return None, jsonify({
            "error": "Invalid or missing JSON body"
        }), 400
    return data, None, None

# -----------------------------
# Create Index
@app.route("/index/create", methods=["POST"])
def create_index():
    try:
        data, err_resp, err_status = get_json_or_error()
        if err_resp is not None:
            return err_resp, err_status

        index_name = data.get("index_name")
        error = validate_index_name(index_name)
        if error:
            return jsonify({
                "error": error
            }), 400


        dimension = data.get("dimension")
        error = validate_dimension(dimension)
        if error:
            return jsonify({
                "error": error
            }), 400

        # These are optional with defaults
        space_type_options = {"cosine", "l2", "ip"}
        space_type = data.get("space_type", "cosine").lower()
        error = validate_choice(space_type, space_type_options)
        if error:
            return jsonify({
                "error": error
            }), 400

        precision_options = {"int8d", "int16d", "float16", "float32", "binary"}
        precision = data.get("precision", "int8d").lower()
        error = validate_choice(precision, precision_options)
        if error:
            return jsonify({
                "error": error
            }), 400

        client.create_index(
            name=index_name,
            dimension=dimension,
            space_type=space_type,
            precision=Precision[precision]
        )

        return jsonify({
            "status": "index created", 
            "index_name": index_name
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# Get Index: (Mostly called internally, but can be used for validation)
@app.route("/index/get", methods=["POST"])
def get_index():
    try:
        data, err_resp, err_status = get_json_or_error()
        if err_resp is not None:
            return err_resp, err_status
        
        index_name = data.get("index_name")
        error = validate_index_name(index_name)
        if error:
            return jsonify({
                "error": error
            }), 400

        index = client.get_index(name=index_name)

        return jsonify({"status": "index loaded", "index_name": index_name})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Upsert Embedded Vectors
@app.route("/index/upsert", methods=["POST"])
def upsert_vectors():
    try:
        data, err_resp, err_status = get_json_or_error()
        if err_resp is not None:
            return err_resp, err_status

        index_name = data.get("index_name")
        error = validate_index_name(index_name)
        if error:
            return jsonify({
                "error": error
            }), 400
        
        embedded_vectors = data.get("embedded_vectors")
        if not embedded_vectors or not isinstance(embedded_vectors, list):
            return jsonify({
                "error": "embedded_vectors is required and must be a list"
            }), 400

        index = client.get_index(name=index_name)

        dimension = index.dimension
        if dimension != len(embedded_vectors[0]["vector"]):
            return jsonify({
                "error": f"embedded_vectors should be of the dimensions {dimension}"
            }), 400
         
        index.upsert(embedded_vectors)
        return jsonify({"status": "vectors upserted", "count": len(embedded_vectors)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# Query Index
@app.route("/index/query", methods=["POST"])
def query_index():
    try:
        data, err_resp, err_status = get_json_or_error()
        if err_resp is not None:
            return err_resp, err_status

        index_name = data.get("index_name")
        error = validate_index_name(index_name)
        if error:
            return jsonify({
                "error": error
            }), 400
        
        vector = data.get("vector")
        error = validate_vector(vector)
        if error:
            return jsonify({
                "error": error
            }), 400
        
        index = client.get_index(name=index_name)
        dimension = index.dimension
        if dimension != len(vector):
            return jsonify({
                "error": f"vectors should be of the dimensions {dimension}"
            }), 400

        top_k = data.get("top_k", 5)
        error = validate_top_k(top_k)
        if error:
            return jsonify({
                "error": error
            }), 400

        include_vectors = data.get("include_vectors", False)
        if not isinstance(include_vectors, bool):
            return jsonify({
                "error": "include_vectors must be a Boolean Value"
            }), 400

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
                "text": r.get("meta", {}).get("text"),
                "description": r.get("meta", {}).get("description", ""),
                "title": r.get("meta").get("title", "")
            }
            for r in raw_results
        ]

        return jsonify({
            "index_name": index_name,
            "top_k": top_k,
            "results": cleaned_results
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# Run Server
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)