from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import json
import uuid

encoder = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient("http://localhost:6333")

def upload_points(collection_name, chunks):
    client.upload_points(
        collection_name=collection_name,
        points=[
            models.PointStruct(
                id=str(uuid.uuid4()),
                vector=encoder.encode(f"{doc['topic']} {json.dumps(doc['content'])}").tolist(),
                payload=doc
            )
            for idx, doc in enumerate(chunks)
        ],
    )