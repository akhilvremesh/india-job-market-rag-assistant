import chromadb
import pandas as pd
from sentence_transformers import SentenceTransformer
from build_documents import load_job_documents


def metadata_text(value):
    """Make a metadata value safe to store in Chroma."""
    if pd.isna(value):
        return "Unknown"

    value = str(value).strip()
    return value if value else "Unknown"


# Load three sample job documents.
sample_jobs = load_job_documents().head(3)
documents = sample_jobs["document"].tolist()
document_ids = sample_jobs["document_id"].tolist()

# Create vectors for the three documents.
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = model.encode_document(documents, show_progress_bar=False)

# Open persistent Chroma storage and create a cosine-search collection.
client = chromadb.PersistentClient(path="data/chroma")
collection = client.get_or_create_collection(
    name="naukri_jobs_demo",
    configuration={"hnsw": {"space": "cosine"}},
)

# Keep useful details with each document for filtering and citations.
metadatas = []
for _, job in sample_jobs.iterrows():
    metadatas.append(
        {
            "title": metadata_text(job["Job Title"]),
            "location": metadata_text(job["Location"]),
            "role": metadata_text(job["Role"]),
        }
    )

# Add or update the three records; rerunning this script won't duplicate them.
collection.upsert(
    ids=document_ids,
    documents=documents,
    embeddings=embeddings.tolist(),
    metadatas=metadatas,
)

print(f"Documents in Chroma collection: {collection.count()}")
# Search for a research executive job in Gurgaon.
query_text = "Find a research executive job in Gurgaon"
query_embedding = model.encode_query([query_text])

results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=3,
    where={"location": "Gurgaon"},
    include=["documents", "metadatas", "distances"],
)

# Print each matching posting and its metadata.
if not results["ids"][0]:
    print("No matching postings found.")
else:
    for index, result_id in enumerate(results["ids"][0]):
        print(f"\nID: {result_id}")
        print(f"Metadata: {results['metadatas'][0][index]}")
        print(f"Cosine distance: {results['distances'][0][index]}")
        print(f"Document:\n{results['documents'][0][index]}")