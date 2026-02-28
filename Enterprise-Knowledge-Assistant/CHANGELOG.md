# Changelog

## Initial Release - 2024-01-01

### Created Files and Structure

#### Project Root
- `README.md`: Comprehensive documentation with setup instructions
- `LICENSE`: MIT License
- `.env.example`: Environment variable template
- `docker-compose.dev.yml`: Local development Docker Compose configuration
- `Makefile`: Development commands (start-dev, run-tests, build-images)
- `requirements-dev.txt`: Development dependencies
- `.pre-commit-config.yaml`: Pre-commit hooks configuration
- `.gitignore`: Git ignore patterns
- `pytest.ini`: Pytest configuration
- `CHANGELOG.md`: This file

#### Docker
- `docker/base.Dockerfile`: Base Docker image with non-root user

#### Django Frontend (`services/django-frontend/`)
- `Dockerfile`: Django service container
- `requirements.txt`: Django dependencies
- `project/manage.py`: Django management script
- `project/eka/`: Django project settings and URLs
- `project/tenants/`: Tenant management app (models, admin, views, templates)
- `project/documents/`: Document management app (models, admin, views, templates)
- `project/chat/`: Chat interface app (views, templates)
- `project/templates/`: HTML templates (base, upload, chat, tenant list)
- `project/fixtures/sample_users.json`: Sample user and tenant data
- Migrations for tenants and documents models

#### FastAPI Ingest Service (`services/fastapi-ingest/`)
- `Dockerfile`: Ingest service container
- `requirements.txt`: FastAPI and processing dependencies
- `app/main.py`: FastAPI application with ingest endpoint
- `app/ingest.py`: Document processing logic (extraction, chunking, embedding, Pinecone)
- `app/utils.py`: Utility functions (Pinecone index management, mock providers)

#### FastAPI Query Service (`services/fastapi-query/`)
- `Dockerfile`: Query service container
- `requirements.txt`: FastAPI and RAG dependencies
- `app/main.py`: FastAPI application with query endpoint
- `app/retriever.py`: RAG retrieval logic (LangChain, Pinecone, OpenAI)
- `app/prompts.py`: Prompt templates for QA
- `app/utils.py`: Utility functions (Pinecone index management, mock providers)

#### Shared Services
- `services/shared/mock_providers.py`: Mock OpenAI and Pinecone providers

#### Infrastructure Scripts (`infra-scripts/`)
- `create_pinecone_index.py`: Script to create Pinecone index for tenant
- `upload_sample_docs.py`: Script to upload sample documents
- `cleanup_tenant.py`: Script to clean up tenant data

#### Kubernetes Manifests (`deploy/k8s/`)
- `django-deploy.yaml`: Django frontend deployment and service
- `fastapi-ingest-deploy.yaml`: Ingest service deployment and service
- `fastapi-query-deploy.yaml`: Query service deployment and service
- `postgres-deploy.yaml`: PostgreSQL deployment, service, and PVC
- `minio-deploy.yaml`: MinIO deployment, service, and PVC
- `kong-deploy.yaml`: Kong API Gateway deployment and configuration
- `secrets-example.yaml`: Example Kubernetes secrets and configmaps

#### Tests (`tests/`)
- `conftest.py`: Pytest configuration and fixtures
- `test_ingest.py`: Tests for ingest service
- `test_retriever.py`: Tests for query service
- `test_django_views.py`: Tests for Django views
- `test_integration.py`: Integration tests and smoke tests

#### CI/CD
- `.github/workflows/ci.yml`: GitHub Actions CI pipeline (lint, test, build)

#### Documentation (`docs/`)
- `architecture.md`: Detailed architecture documentation

### Key Features Implemented

1. **Multi-tenant Architecture**
   - Tenant isolation at database, vector store, and object storage levels
   - `X-Tenant-ID` header-based routing

2. **Document Processing**
   - Support for PDF, DOCX, TXT, and images (with optional OCR)
   - Configurable text chunking (size and overlap)
   - OpenAI embeddings generation
   - Pinecone vector storage

3. **RAG Query System**
   - LangChain RetrievalQA chain
   - OpenAI GPT-4 for answer generation
   - Source attribution with excerpts

4. **Mock Providers**
   - Mock OpenAI and Pinecone for local development
   - No API keys required for testing

5. **Observability**
   - Prometheus metrics endpoints
   - Structured JSON logging
   - Health check endpoints

6. **Containerization**
   - Dockerfiles for all services
   - Docker Compose for local development
   - Non-root user in containers

7. **Kubernetes Deployment**
   - Complete K8s manifests for all services
   - ConfigMaps and Secrets examples
   - Kong API Gateway configuration

8. **Testing**
   - Unit tests for all services
   - Integration tests
   - Smoke tests
   - Mock providers for test isolation

### Assumptions Made

1. **Sample File Path**: The sample document path `file:///mnt/data/f8068984-15db-4e27-b6c7-19e0237fdc54.png` is referenced in the upload script. This file should exist on the system or be created for testing.

2. **OCR Support**: OCR (pytesseract) is optional. If not available, images will be stored with a placeholder message.

3. **Database Migrations**: Django migrations are included but will need to be run on first setup.

4. **Default Tenant**: A default tenant `tenant_default` is created in fixtures for quick testing.

5. **Service URLs**: Services communicate via Docker service names in docker-compose, and via service names in Kubernetes.

6. **Python Version**: All code uses Python 3.11.

7. **LangChain Version**: Using LangChain 0.1.0 (early version). In production, you may want to use a more recent stable version.

8. **OpenAI Models**: Default models are GPT-4 for LLM and text-embedding-ada-002 for embeddings. These can be configured via environment variables.

### Next Steps for Users

1. Copy `.env.example` to `.env` and fill in API keys (or set `USE_MOCK_PROVIDERS=true`)
2. Run `docker compose -f docker-compose.dev.yml up --build`
3. Create a Pinecone index: `python infra-scripts/create_pinecone_index.py --tenant tenant_default`
4. Upload sample docs: `python infra-scripts/upload_sample_docs.py --tenant tenant_default --file "file:///mnt/data/f8068984-15db-4e27-b6c7-19e0237fdc54.png"`
5. Query the system via curl or Django UI
6. Run tests: `pytest`

### Known Limitations

1. OCR requires tesseract-ocr system package (not included in Docker image)
2. Django admin password needs to be set manually (fixture uses a placeholder)
3. Kong configuration is basic - may need customization for production
4. No authentication middleware for FastAPI services (relies on Django or Kong)
5. MinIO bucket creation is manual (not automated in startup)

