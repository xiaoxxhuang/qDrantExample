from flask import Flask, request, jsonify
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize

# Initialize the encoder and Qdrant client
encoder = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient("http://localhost:6333")

# Initialize the Flask app
app = Flask(__name__)

# Define the query endpoint
@app.route("/query", methods=["POST"])
def query_qdrant():
    try:
        # Parse the request JSON
        data = request.json
        query_text = data.get("query", "")
        collection_name = data.get("collection_name", "")  # Default score threshold
        score_threshold = data.get("score_threshold", 0.5)  # Default score threshold
        limit = data.get("limit", 3)
        filter = data.get("filter","")

        if not query_text:
            return jsonify({"error": "Query text is required"}), 400
        if not collection_name:
            return jsonify({"error": "Collection name is required"}), 400

        # Encode the query and perform the Qdrant query
        query_vector = encoder.encode(query_text).reshape(1, -1)
        normalized_vector = normalize(query_vector)[0]
        query_params = {
            "collection_name": collection_name,
            "query": normalized_vector,
            "score_threshold": score_threshold,
            "limit": limit
        }

        if filter:
            query_params["query_filter"] = filter

        hits = client.query_points(**query_params).points

        # Format the results
        results = [
            {"payload": hit.payload, "score": hit.score}
            for hit in hits
        ]

        return jsonify({"results": results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)