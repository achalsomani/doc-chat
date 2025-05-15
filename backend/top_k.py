from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def retrieve_top_chunks(
    query_embedding: list[float], chunks: list[dict], top_k: int = 3
) -> list[dict]:
    embeddings = [item["embedding"] for item in chunks]
    query_vector = np.array(query_embedding).reshape(1, -1)
    stored_vectors = np.array(embeddings)
    similarities = cosine_similarity(query_vector, stored_vectors)[0]
    ranked = sorted(zip(similarities, chunks), key=lambda x: x[0], reverse=True)
    return [{"id": item["id"], "chunk": item["chunk"]} for _, item in ranked[:top_k]]
