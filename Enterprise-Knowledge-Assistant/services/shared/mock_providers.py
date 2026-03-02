import io
import uuid
from collections import defaultdict


class MockEmbeddingData:
    def __init__(self, embedding):
        self.embedding = embedding


class MockEmbeddingResponse:
    def __init__(self, texts):
        self.data = [MockEmbeddingData([0.1 * (i % 10)] * 1536) for i, _ in enumerate(texts)]


class MockChatMessage:
    def __init__(self, content):
        self.content = content


class MockChatChoice:
    def __init__(self, content):
        self.message = MockChatMessage(content)


class MockChatCompletion:
    def __init__(self, question):
        self.choices = [MockChatChoice(f"[Mock LLM] Simulated answer to: '{question}'")]


class MockEmbeddings:
    def create(self, model, input):
        return MockEmbeddingResponse(input)


class MockChatCompletions:
    def create(self, model, messages, max_tokens=None, temperature=None):
        question = messages[-1]["content"] if messages else "unknown"
        return MockChatCompletion(question)


class MockOpenAI:
    def __init__(self):
        self.embeddings = MockEmbeddings()
        self.chat = type("Chat", (), {"completions": MockChatCompletions()})()


class MockMatch:
    def __init__(self, id, score, metadata):
        self.id = id
        self.score = score
        self.metadata = metadata


class MockQueryResult:
    def __init__(self, matches):
        self.matches = matches


_mock_store: dict = defaultdict(list)


class MockPineconeIndex:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self._key = f"eka-index-{tenant_id}"

    def upsert(self, vectors):
        _mock_store[self._key].extend(vectors)

    def query(self, vector, top_k=3, include_metadata=True):
        stored = _mock_store[self._key]
        matches = []
        for v in stored[:top_k]:
            metadata = v.get("metadata", {}) if isinstance(v, dict) else {}
            matches.append(MockMatch(
                id=v.get("id", str(uuid.uuid4())) if isinstance(v, dict) else v.id,
                score=0.92,
                metadata=metadata,
            ))
        return MockQueryResult(matches)

    def delete(self, ids=None, delete_all=False):
        if delete_all:
            _mock_store[self._key] = []


class MockMinIO:
    def __init__(self):
        self._buckets: dict = defaultdict(dict)

    def put_object(self, bucket, object_name, data, length, **kwargs):
        self._buckets[bucket][object_name] = data.read() if hasattr(data, "read") else data

    def get_object(self, bucket, object_name):
        return io.BytesIO(self._buckets[bucket].get(object_name, b""))

    def make_bucket(self, bucket):
        if bucket not in self._buckets:
            self._buckets[bucket] = {}

    def bucket_exists(self, bucket):
        return bucket in self._buckets