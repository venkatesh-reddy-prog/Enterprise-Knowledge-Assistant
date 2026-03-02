import os
from typing import Any

from app.utils import get_openai_client, get_pinecone_index, use_mock

TOP_K = int(os.getenv("TOP_K", 3))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 1000))
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
LLM_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

SYSTEM_PROMPT = """You are an enterprise knowledge assistant. Answer the user's question using ONLY the
provided context passages. If the context does not contain enough information, say so clearly.
Always cite the source document filenames when you use them."""

QA_PROMPT = """Context passages:
{context}

Question: {question}

Answer:"""


def embed_question(question: str) -> list[float]:
    if use_mock():
        return [0.0] * 1536
    client = get_openai_client()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=[question])
    return response.data[0].embedding


def retrieve_chunks(question_vector: list[float], tenant_id: str) -> list[dict]:
    index = get_pinecone_index(tenant_id)
    results = index.query(vector=question_vector, top_k=TOP_K, include_metadata=True)
    matches = getattr(results, "matches", results.get("matches", []))
    return [
        {
            "text": m.get("metadata", {}).get("text", "") if isinstance(m, dict) else m.metadata.get("text", ""),
            "filename": m.get("metadata", {}).get("filename", "unknown") if isinstance(m, dict) else m.metadata.get("filename", "unknown"),
            "score": m.get("score", 0) if isinstance(m, dict) else m.score,
        }
        for m in matches
    ]


def generate_answer(question: str, chunks: list[dict]) -> str:
    if use_mock():
        if chunks:
            excerpts = " | ".join(c["text"][:100] for c in chunks)
            return f"[Mock answer] Based on your documents: {excerpts}..."
        return "[Mock answer] No relevant documents found for your question."

    client = get_openai_client()
    context = "\n\n".join(f"[Source: {c['filename']}]\n{c['text']}" for c in chunks)
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": QA_PROMPT.format(context=context, question=question)},
        ],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    return response.choices[0].message.content


async def answer_question(question: str, tenant_id: str) -> dict[str, Any]:
    question_vector = embed_question(question)
    chunks = retrieve_chunks(question_vector, tenant_id)
    answer = generate_answer(question, chunks)
    sources = [
        {"filename": c["filename"], "excerpt": c["text"][:200], "score": round(c["score"], 4)}
        for c in chunks
    ]
    return {"answer": answer, "sources": sources}