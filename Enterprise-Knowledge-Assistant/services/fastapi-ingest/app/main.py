import logging
import os
import uuid
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import PlainTextResponse

from app.ingest import process_document

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "msg": "%(message)s"}',
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Enterprise Knowledge Assistant - Ingest Service",
    version="1.0.0",
    description="Document ingestion and vectorization service",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

INGEST_COUNTER = Counter("ingest_requests_total", "Total ingest requests", ["tenant_id", "status"])
INGEST_DURATION = Histogram("ingest_duration_seconds", "Ingest processing duration", ["tenant_id"])


@app.get("/healthz")
def health():
    return {"status": "ok", "service": "ingest"}


@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return generate_latest()


@app.post("/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    x_tenant_id: Optional[str] = Header(default="tenant_default"),
):
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-ID header is required")

    allowed_types = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
        "image/png",
        "image/jpeg",
        "image/jpg",
    }
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type: {file.content_type}. Allowed: pdf, docx, txt, png, jpeg",
        )

    doc_id = str(uuid.uuid4())
    logger.info(f"Starting ingest tenant={x_tenant_id} doc_id={doc_id} file={file.filename}")

    with INGEST_DURATION.labels(tenant_id=x_tenant_id).time():
        try:
            content = await file.read()
            result = await process_document(
                content=content,
                filename=file.filename,
                content_type=file.content_type,
                doc_id=doc_id,
                tenant_id=x_tenant_id,
            )
            INGEST_COUNTER.labels(tenant_id=x_tenant_id, status="success").inc()
            logger.info(f"Ingest complete doc_id={doc_id} chunks={result['chunks_stored']}")
            return {
                "status": "Document ingested successfully",
                "doc_id": doc_id,
                "filename": file.filename,
                "tenant_id": x_tenant_id,
                "chunks_stored": result["chunks_stored"],
                "minio_path": result.get("minio_path"),
            }
        except Exception as e:
            INGEST_COUNTER.labels(tenant_id=x_tenant_id, status="error").inc()
            logger.error(f"Ingest failed doc_id={doc_id} error={str(e)}")
            raise HTTPException(status_code=500, detail=f"Ingest failed: {str(e)}")