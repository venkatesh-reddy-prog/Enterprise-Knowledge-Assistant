"""
Document processing logic: extraction → chunking → embedding → Pinecone + MinIO
"""
import io
import os
from typing import Any

from app.utils import get_minio_client, get_openai_client, get_pinecone_index, use_mock

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 100))
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "documents")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def extract_text(content: bytes, content_type: str, filename: str) -> str:
    if content_type == "text/plain":
        return content.decode("utf-8", errors="ignore")

    if content_type == "application/pdf":
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(content))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except ImportError:
            raise RuntimeError("pypdf not installed. Add it to requirements.txt.")

    if content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        try:
            import docx
            doc = docx.Document(io.BytesIO(content))
            return "\n".join(p.text for p in doc.paragraphs)
        except ImportError:
            raise RuntimeError("python-docx not installed. Add it to requirements.txt.")

    if content_type in ("image/png", "image/jpeg", "image/jpg"):
        try:
            import pytesseract
            from PIL import Image
            img = Image.open(io.BytesIO(content))
            return pytesseract.image_to_string(img)
        except (ImportError, Exception):
            return f"[Image file: {filename} — OCR unavailable]"

    return f"[Unsupported type: {content_type}]"


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    if not text.strip():
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def embed_texts(texts: list[str]) -> list[list[float]]:
    if use_mock():
        return [[0.0] * 1536 for _ in texts]
    client = get_openai_client()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


def store_in_minio(content: bytes, doc_id: str, tenant_id: str, filename: str) -> str:
    client = get_minio_client()
    object_name = f"{tenant_id}/{doc_id}/{filename}"
    try:
        client.put_object(MINIO_BUCKET, object_name, io.BytesIO(content), length=len(content))
    except Exception:
        client.make_bucket(MINIO_BUCKET)
        client.put_object(MINIO_BUCKET, object_name, io.BytesIO(content), length=len(content))
    return object_name


async def process_document(
    content: bytes,
    filename: str,
    content_type: str,
    doc_id: str,
    tenant_id: str,
) -> dict[str, Any]:
    minio_path = store_in_minio(content, doc_id, tenant_id, filename)
    text = extract_text(content, content_type, filename)
    chunks = chunk_text(text)
    if not chunks:
        chunks = [f"[Empty document: {filename}]"]
    embeddings = embed_texts(chunks)
    index = get_pinecone_index(tenant_id)
    vectors = [
        {
            "id": f"{doc_id}_{i}",
            "values": embeddings[i],
            "metadata": {
                "text": chunk,
                "doc_id": doc_id,
                "filename": filename,
                "tenant_id": tenant_id,
                "chunk_index": i,
            },
        }
        for i, chunk in enumerate(chunks)
    ]
    index.upsert(vectors=vectors)
    return {"chunks_stored": len(chunks), "minio_path": minio_path}