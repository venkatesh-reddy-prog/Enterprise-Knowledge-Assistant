import os
import httpx
from collections import defaultdict

_pinecone_indexes: dict = {}

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
OLLAMA_LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL", "deepseek-coder")


def use_mock() -> bool:
    return os.getenv("USE_MOCK_PROVIDERS", "false").lower() == "true"


_mock_store: dict = defaultdict(list)


class _MockMatch:
    def __init__(self, v):
        self.id = v.get("id", "")
        self.score = 0.92
        self.metadata = v.get("metadata", {})


class _MockIndex:
    def __init__(self, key):
        self._key = key

    def upsert(self, vectors):
        _mock_store[self._key].extend(vectors)

    def query(self, vector, top_k=3, include_metadata=True):
        class R:
            matches = [_MockMatch(v) for v in _mock_store[self._key][:top_k]]

        return R()


def get_pinecone_index(tenant_id: str):
    if use_mock():
        return _MockIndex(f"eka-index-{tenant_id}")

    if tenant_id not in _pinecone_indexes:
        from pinecone import Pinecone

        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        _pinecone_indexes[tenant_id] = pc.Index(f"eka-index-{tenant_id}")

    return _pinecone_indexes[tenant_id]


def ollama_chat(prompt: str) -> str:
    response = httpx.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": OLLAMA_LLM_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=60,
    )

    response.raise_for_status()
    data = response.json()
    return data["response"]