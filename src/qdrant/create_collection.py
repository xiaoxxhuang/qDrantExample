from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import argparse

parser = argparse.ArgumentParser(description="Create a Qdrant collection.")
parser.add_argument("--collection", type=str, required=True, help="The collection name")
args = parser.parse_args()
collection_name = args.collection

# Initialize the encoder and Qdrant client
encoder = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient("http://localhost:6333")

# Create a collection
client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=encoder.get_sentence_embedding_dimension(),
        distance=models.Distance.COSINE
    )
)
