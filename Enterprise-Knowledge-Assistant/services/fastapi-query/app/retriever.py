import os
import httpx
from typing import Any

from app.utils import get_pinecone_index, ollama_chat, use_mock

TOP_K = int(os.getenv("TOP_K", 5))

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")

SYSTEM_PROMPT = """You are an enterprise knowledge assistant.

Use the provided context to answer the question.

Rules:
- Only answer using the context.
- If the context does not contain the answer say "I don't know".
"""


def embed_question(question: str) -> list[float]:
    if use_mock():
        return [0.0] * 768

    response = httpx.post(
        f"{OLLAMA_BASE_URL}/api/embeddings",
        json={
            "model": OLLAMA_EMBED_MODEL,
            "prompt": question,
        },
        timeout=60,
    )

    response.raise_for_status()
    return response.json()["embedding"]


def retrieve_chunks(question_vector: list[float], tenant_id: str) -> list[dict]:
    index = get_pinecone_index(tenant_id)

    results = index.query(vector=question_vector, top_k=TOP_K, include_metadata=True)

    matches = getattr(results, "matches", [])

    return [
        {
            "text": m.metadata.get("text", ""),
            "filename": m.metadata.get("filename", "unknown"),
            "score": m.score,
        }
        for m in matches
    ]


def generate_answer(question: str, chunks: list[dict]) -> str:
    context = "\n\n".join(
        f"[Source: {c['filename']}]\n{c['text']}" for c in chunks
    )

    prompt = f"""{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}

Answer:
"""

    return ollama_chat(prompt)


async def answer_question(question: str, tenant_id: str) -> dict[str, Any]:
    question_vector = embed_question(question)

    chunks = retrieve_chunks(question_vector, tenant_id)

    answer = generate_answer(question, chunks)

    sources = [
        {"filename": c["filename"], "excerpt": c["text"][:200], "score": round(c["score"], 4)}
        for c in chunks
    ]

    return {"answer": answer, "sources": sources}