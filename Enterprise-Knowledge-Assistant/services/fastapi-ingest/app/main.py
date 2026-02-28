from fastapi import FastAPI

app = FastAPI(title="Enterprise Knowledge Assistant - Ingest Service")

@app.post("/ingest")
def ingest_document(content: str):
    return {
        "status": "Document ingested successfully",
        "content": content
    }