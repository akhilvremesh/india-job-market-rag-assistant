from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Open the saved collection and the same embedding model used for indexing
client = chromadb.PersistentClient(
    path=str(PROJECT_ROOT / "data" / "chroma")
)
collection = client.get_collection(name="naukri_jobs")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def search_jobs(query, number_of_results=5, location=None):
    """Find job postings whose text is semantically similar to the query."""
    query_embedding = model.encode_query([query]).tolist()

    filters = None
    if location:
        filters = {"location": location}

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=number_of_results,
        where=filters,
        include=["documents", "metadatas", "distances"],
    )

    for index, document_id in enumerate(results["ids"][0]):
        metadata = results["metadatas"][0][index]
        distance = results["distances"][0][index]

        print(f"\nResult {index + 1}")
        print(f"ID: {document_id}")
        print(f"Title: {metadata['title']}")
        print(f"Role: {metadata['role']}")
        print(f"Location: {metadata['location']}")
        print(f"Cosine distance: {distance:.3f}")
        print(results["documents"][0][index])


if __name__ == "__main__":
    search_jobs("data analyst", number_of_results=5, location="Bengaluru")