import os
from collections import defaultdict

_pinecone_indexes: dict = {}


def use_mock() -> bool:
    return os.getenv("USE_MOCK_PROVIDERS", "false").lower() == "true"


class _MockEmbeddingData:
    def __init__(self): self.embedding = [0.0] * 1536

class _MockEmbeddingResponse:
    def __init__(self): self.data = [_MockEmbeddingData()]

class _MockEmbeddings:
    def create(self, model, input): return _MockEmbeddingResponse()

class _MockChatMessage:
    def __init__(self, q): self.content = f"[Mock] Simulated answer for: {q!r}"

class _MockChoice:
    def __init__(self, q): self.message = _MockChatMessage(q)

class _MockCompletion:
    def __init__(self, msgs): self.choices = [_MockChoice(msgs[-1]["content"][:60])]

class _MockCompletions:
    def create(self, model, messages, **kw): return _MockCompletion(messages)

class _MockChat:
    def __init__(self): self.completions = _MockCompletions()

class _MockOpenAI:
    def __init__(self):
        self.embeddings = _MockEmbeddings()
        self.chat = _MockChat()

_mock_store: dict = defaultdict(list)

class _MockMatch:
    def __init__(self, v):
        self.id = v.get("id", "") if isinstance(v, dict) else getattr(v, "id", "")
        self.score = 0.92
        self.metadata = v.get("metadata", {}) if isinstance(v, dict) else getattr(v, "metadata", {})

class _MockIndex:
    def __init__(self, key): self._key = key
    def upsert(self, vectors): _mock_store[self._key].extend(vectors)
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


def get_openai_client():
    if use_mock():
        return _MockOpenAI()
    from openai import OpenAI
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])