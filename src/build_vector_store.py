from pathlib import Path

import chromadb
import pandas as pd
from sentence_transformers import SentenceTransformer

from build_documents import load_job_documents


# Find the project root even if you run this script from inside src/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load the cleaned job postings as text documents
jobs = load_job_documents(
    str(PROJECT_ROOT / "data" / "jobs.db")
)

# Load the embedding model used for semantic search
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Create or open the local Chroma database
client = chromadb.PersistentClient(
    path=str(PROJECT_ROOT / "data" / "chroma")
)

# Use cosine distance to compare job and query embeddings
collection = client.get_or_create_collection(
    name="naukri_jobs",
    configuration={"hnsw": {"space": "cosine"}},
)


def metadata_text(value):
    """Convert a missing or blank value into text Chroma can store."""
    if pd.isna(value):
        return "Unknown"

    value = str(value).strip()
    return value if value else "Unknown"


# Add postings in smaller groups to limit memory use
batch_size = 500

for start in range(0, len(jobs), batch_size):
    batch = jobs.iloc[start : start + batch_size]

    documents = batch["document"].tolist()
    document_ids = batch["document_id"].astype(str).tolist()

    # Create one 384-number vector for each job document
    embeddings = model.encode_document(
        documents,
        show_progress_bar=False,
    )

    # Chroma metadata must contain simple values such as strings
    metadatas = [
        {
            "title": metadata_text(row["Job Title"]),
            "location": metadata_text(row["Location"]),
            "role": metadata_text(row["Role"]),
        }
        for _, row in batch.iterrows()
    ]

    # Save this batch; upsert safely updates existing IDs on reruns
    collection.upsert(
        ids=document_ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
    )

    completed = min(start + batch_size, len(jobs))
    print(f"Indexed {completed}/{len(jobs)} postings")

print(f"Total documents in Chroma: {collection.count()}")