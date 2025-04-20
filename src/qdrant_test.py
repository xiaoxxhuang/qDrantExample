from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient("http://localhost:6333")

hits = client.query_points(
    collection_name="temp",
    query=encoder.encode("What?").tolist(),
    score_threshold=0.5
).points

for hit in hits:
    print(hit.payload, "score:", hit.score)

# hits = client.query_points(
#     collection_name="my_books",
#     query=encoder.encode("alien invasion").tolist(),
#     query_filter=models.Filter(
#         must=[models.FieldCondition(key="year", range=models.Range(gte=2000))]
#     ),
#     limit=1,
# ).points
#
# for hit in hits:
#     print(hit.payload, "score:", hit.score)
