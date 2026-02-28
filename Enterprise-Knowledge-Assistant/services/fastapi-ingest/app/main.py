from fastapi import FastAPI
from pinecone import Pinecone
import os, uuid
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(env_path)

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

app = FastAPI(title="Enterprise Knowledge Assistant - Ingest Service")

@app.post("/ingest")
def ingest_document(content: str):
    doc_id = str(uuid.uuid4())

    # Store text in Pinecone (auto embedding enabled)
    index.upsert([
        {
            "id": doc_id,
            "metadata": {"text": content}
        }
    ])

    return {
        "status": "Document ingested successfully",
        "id": doc_id,
        "content": content
    }