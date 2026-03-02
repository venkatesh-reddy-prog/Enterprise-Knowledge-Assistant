import logging
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, generate_latest
from pydantic import BaseModel
from starlette.responses import PlainTextResponse

from app.retriever import answer_question

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "msg": "%(message)s"}',
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Enterprise Knowledge Assistant - Query Service",
    version="1.0.0",
    description="RAG-based question answering service",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

QUERY_COUNTER = Counter("query_requests_total", "Total query requests", ["tenant_id", "status"])
QUERY_DURATION = Histogram("query_duration_seconds", "Query processing duration", ["tenant_id"])


# 🔹 Accept both "question" and "query" (Django sends "query")
class QuestionRequest(BaseModel):
    question: Optional[str] = None
    query: Optional[str] = None

    def get_question(self) -> str:
        return (self.question or self.query or "").strip()


@app.get("/")
def root():
    return {"message": "Query Service Running 🚀"}


@app.get("/healthz")
def health():
    return {"status": "ok", "service": "query"}


@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return generate_latest()


@app.post("/query")
async def query_knowledge_base(
    body: QuestionRequest,
    x_tenant_id: Optional[str] = Header(default="tenant_default"),
):
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-ID header is required")

    # Get question from either "question" or "query"
    question_text = body.get_question()
    if not question_text:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    logger.info(f"Query tenant={x_tenant_id} question={question_text[:80]!r}")

    with QUERY_DURATION.labels(tenant_id=x_tenant_id).time():
        try:
            result = await answer_question(question=question_text, tenant_id=x_tenant_id)
            QUERY_COUNTER.labels(tenant_id=x_tenant_id, status="success").inc()

            return {
                "question": question_text,
                "answer": result["answer"],
                "sources": result.get("sources", []),
                "tenant_id": x_tenant_id,
            }

        except Exception as e:
            QUERY_COUNTER.labels(tenant_id=x_tenant_id, status="error").inc()
            logger.error(f"Query failed tenant={x_tenant_id} error={str(e)}")
            raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.post("/ask")
async def ask_question(
    body: QuestionRequest,
    x_tenant_id: Optional[str] = Header(default="tenant_default"),
):
    return await query_knowledge_base(body, x_tenant_id)