# Enterprise Knowledge Assistant

A multi-tenant Enterprise Knowledge Assistant with Django frontend, FastAPI microservices, Pinecone vector search, OpenAI GPT, LangChain orchestration, MinIO object storage, and PostgreSQL metadata.

## Architecture

- **Frontend**: Django 4.2+ with authentication and tenant management
- **Ingest Service**: FastAPI service for document processing and vectorization
- **Query Service**: FastAPI service for RAG-based question answering
- **Vector Store**: Pinecone for semantic search
- **LLM**: OpenAI GPT via LangChain
- **Storage**: MinIO for object storage, PostgreSQL for metadata
- **API Gateway**: Kong for ingress and routing

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- OpenAI API Key (or set `USE_MOCK_PROVIDERS=true` for local dev)
- Pinecone API Key and Environment (or set `USE_MOCK_PROVIDERS=true`)

### Local Development Setup

1. **Open the project folder in VS Code**
   ```bash
   code enterprise-knowledge-assistant
   ```

2. **Copy environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and fill in your API keys, or set `USE_MOCK_PROVIDERS=true` for local development without real API keys.

3. **Start all services**
   ```bash
   docker compose -f docker-compose.dev.yml up --build
   ```
   This will start:
   - Django frontend on http://localhost:8000
   - Query service on http://localhost:8100
   - Ingest service on http://localhost:8200
   - PostgreSQL on localhost:5432
   - MinIO on http://localhost:9000

4. **Create a Pinecone index (optional, if not using mocks)**
   ```bash
   python infra-scripts/create_pinecone_index.py --tenant tenant_default
   ```

5. **Upload sample documents**
   ```bash
   python infra-scripts/upload_sample_docs.py --tenant tenant_default --file "file:///mnt/data/f8068984-15db-4e27-b6c7-19e0237fdc54.png"
   ```

6. **Query the knowledge base**
   ```bash
   curl -X POST http://localhost:8100/query \
     -H "Content-Type: application/json" \
     -H "X-Tenant-ID: tenant_default" \
     -d '{"question":"What is in the sample document?"}'
   ```

7. **Run tests**
   ```bash
   pytest
   ```

## Project Structure

```
enterprise-knowledge-assistant/
├── services/
│   ├── django-frontend/     # Django web application
│   ├── fastapi-ingest/       # Document ingestion service
│   └── fastapi-query/        # Query/retrieval service
├── deploy/k8s/               # Kubernetes manifests
├── infra-scripts/              # Infrastructure setup scripts
├── tests/                      # Test suite
└── docs/                       # Documentation
```

## Environment Variables

Key environment variables (see `.env.example` for full list):

- `OPENAI_API_KEY`: OpenAI API key for embeddings and LLM
- `PINECONE_API_KEY`: Pinecone API key
- `PINECONE_ENV`: Pinecone environment
- `USE_MOCK_PROVIDERS`: Set to `true` to use mock providers (no real API calls)
- `MINIO_ACCESS_KEY`: MinIO access key
- `MINIO_SECRET_KEY`: MinIO secret key
- `POSTGRES_DB`: PostgreSQL database name
- `POSTGRES_USER`: PostgreSQL username
- `POSTGRES_PASSWORD`: PostgreSQL password

## Development Commands

```bash
# Start development environment
make start-dev
# or
docker compose -f docker-compose.dev.yml up --build

# Run tests
make run-tests
# or
pytest

# Build Docker images
make build-images
# or
docker compose -f docker-compose.dev.yml build
```

## Testing

The test suite includes:
- Unit tests for ingest service
- Unit tests for query service
- Integration tests for Django views
- Mock providers for OpenAI and Pinecone (used by default in tests)

Run tests with:
```bash
pytest
```

## Kubernetes Deployment

Kubernetes manifests are provided in `deploy/k8s/`:

- `django-deploy.yaml`: Django frontend deployment
- `fastapi-ingest-deploy.yaml`: Ingest service deployment
- `fastapi-query-deploy.yaml`: Query service deployment
- `kong-deploy.yaml`: Kong API Gateway configuration
- `postgres-deploy.yaml`: PostgreSQL deployment
- `minio-deploy.yaml`: MinIO deployment
- `secrets-example.yaml`: Example secrets (replace with real values)

Apply manifests:
```bash
kubectl apply -f deploy/k8s/
```

## Tenant Isolation

Each tenant has:
- Isolated Pinecone index: `eka-index-{tenant_id}`
- Isolated PostgreSQL schema/rows (via tenant_id foreign keys)
- Isolated MinIO bucket/prefix (via tenant_id in path)

## API Endpoints

### Ingest Service
- `POST /ingest`: Upload and process documents
  - Headers: `X-Tenant-ID: <tenant_id>`
  - Body: multipart/form-data with `file` field

### Query Service
- `POST /query`: Query the knowledge base
  - Headers: `X-Tenant-ID: <tenant_id>`
  - Body: `{"question": "your question"}`

### Health Checks
- `GET /healthz`: Health check endpoint (all services)

## License

See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

