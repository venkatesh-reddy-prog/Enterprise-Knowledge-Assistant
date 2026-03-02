import io
import os
import uuid
from collections import defaultdict

_pinecone_indexes: dict = {}


def use_mock() -> bool:
    return os.getenv("USE_MOCK_PROVIDERS", "false").lower() == "true"


class _MockEmbeddingData:
    def __init__(self, i): self.embedding = [0.1 * (i % 10)] * 1536

class _MockEmbeddingResponse:
    def __init__(self, texts): self.data = [_MockEmbeddingData(i) for i, _ in enumerate(texts)]

class _MockEmbeddings:
    def create(self, model, input): return _MockEmbeddingResponse(input)

class _MockOpenAI:
    def __init__(self): self.embeddings = _MockEmbeddings()

_mock_store: dict = defaultdict(list)

class _MockPineconeIndex:
    def __init__(self, key): self._key = key
    def upsert(self, vectors): _mock_store[self._key].extend(vectors)
    def query(self, vector, top_k=3, include_metadata=True):
        class R:
            def __init__(s): s.matches = []
        r = R()
        for v in _mock_store[self._key][:top_k]:
            class M:
                id = v.get("id", "") if isinstance(v, dict) else v.id
                score = 0.92
                metadata = v.get("metadata", {}) if isinstance(v, dict) else {}
            r.matches.append(M())
        return r

class _MockMinIO:
    def __init__(self): self._buckets: dict = defaultdict(dict)
    def put_object(self, bucket, name, data, length, **kw):
        self._buckets[bucket][name] = data.read() if hasattr(data, "read") else data
    def make_bucket(self, b): self._buckets.setdefault(b, {})
    def bucket_exists(self, b): return b in self._buckets


def get_pinecone_index(tenant_id: str):
    if use_mock():
        return _MockPineconeIndex(f"eka-index-{tenant_id}")
    if tenant_id not in _pinecone_indexes:
        from pinecone import Pinecone, ServerlessSpec
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        index_name = f"eka-index-{tenant_id}"
        existing = [i.name for i in pc.list_indexes()]
        if index_name not in existing:
            pc.create_index(
                name=index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
        _pinecone_indexes[tenant_id] = pc.Index(index_name)
    return _pinecone_indexes[tenant_id]


def get_openai_client():
    if use_mock():
        return _MockOpenAI()
    from openai import OpenAI
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def get_minio_client():
    if use_mock():
        return _MockMinIO()
    from minio import Minio
    return Minio(
        os.getenv("MINIO_ENDPOINT", "minio:9000"),
        access_key=os.getenv("MINIO_ROOT_USER", "minioadmin"),
        secret_key=os.getenv("MINIO_ROOT_PASSWORD", "minioadmin"),
        secure=os.getenv("MINIO_USE_SSL", "false").lower() == "true",
    )