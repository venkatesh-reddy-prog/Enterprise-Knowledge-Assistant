# 🧠 Enterprise Knowledge Assistant  
### AI-Powered Semantic Search & Knowledge Retrieval Platform

Enterprise Knowledge Assistant is a scalable AI platform that enables organizations to perform intelligent, context-aware search across internal documents using vector embeddings and Retrieval-Augmented Generation (RAG).

Built to simulate a production-grade internal knowledge system used in modern enterprises.

---

## 🌍 Problem Statement

Traditional keyword-based search systems fail when:

- Documents are unstructured
- Queries require contextual understanding
- Knowledge bases scale rapidly
- Users expect natural language answers instead of document links

This system enables **semantic retrieval + grounded AI responses**, ensuring accurate and explainable answers from enterprise data.

---

## 🏛 High-Level Architecture

![Enterprise_Knowledge_Assistant_Architecture](docs/screenshots/Enterprise_Knowledge_Assistant_Architecture.png)

---

## 📌 Core Features

- 📂 Document ingestion & automatic chunking
- 🧠 Embedding generation using OpenAI
- 🔎 Semantic vector similarity search with Pinecone
- 🤖 Retrieval-Augmented Generation (RAG)
- ⚡ Low-latency query processing
- 🧩 Microservices-based architecture
- 🐳 Docker containerized deployment
- 🌐 Full-stack implementation

---

## 🏗 Tech Stack

### Backend Services
- Java (Spring Boot)
- Python (FastAPI)
- REST APIs
- Maven

### AI & Vector Infrastructure
- OpenAI API (Embeddings + LLM)
- Pinecone (Vector Database)
- RAG Architecture

### Data Layer
- PostgreSQL (Metadata storage)
- Pinecone (Vector index)

### Frontend
- React.js

### DevOps
- Docker
- Environment-based configuration
- CI/CD-ready architecture

---

## 🔁 Query Execution Flow

1. User submits a natural language question  
2. Backend generates query embedding  
3. Pinecone retrieves top-K relevant document chunks  
4. Retrieved context is injected into LLM prompt  
5. LLM generates a grounded response  
6. Answer returned to frontend  

This reduces hallucinations and ensures responses are based on enterprise data.

---

## 📂 Project Structure

```
enterprise-knowledge-assistant/
 ├── frontend/
 │   ├── src/
 │   └── package.json
 │
 ├── services/
 │   ├── query-service/        (Spring Boot)
 │   ├── ingestion-service/    (FastAPI)
 │   └── shared/
 │
 ├── docker-compose.yml
 └── README.md
```

---

## 🚀 Running Locally

### 1️⃣ Clone Repository

```bash
git clone https://github.com/venkatesh-reddy-prog/enterprise-knowledge-assistant.git
cd enterprise-knowledge-assistant
```

### 2️⃣ Configure Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_key
PINECONE_API_KEY=your_key
PINECONE_ENV=your_env
PINECONE_INDEX=your_index
```

### 3️⃣ Start Services

```bash
docker-compose up --build
```

Or run services individually:
- Spring Boot (Query Service)
- FastAPI (Ingestion Service)
- React Frontend

---

## 🔐 Security & Configuration

- Secure API key management via environment variables
- Modular service separation
- Independent ingestion & query pipelines
- Scalable stateless microservices

---

## 📈 Design Considerations

- Efficient document chunking strategy
- Asynchronous ingestion pipeline
- Optimized embedding storage
- Low-latency similarity retrieval
- Containerized multi-service architecture

---

## 🎯 Use Cases

- Internal enterprise knowledge search
- HR policy assistant
- Engineering documentation retrieval
- Legal document semantic search
- Procurement & compliance intelligence

---

## 🧠 Key Concepts Demonstrated

- Distributed Microservices Architecture
- Retrieval-Augmented Generation (RAG)
- Vector Databases & Embeddings
- REST API Design
- AI + Backend Integration
- Dockerized Deployment
- Enterprise System Design

---

## 👨‍💻 Author

**B. Venkatesh Reddy**  
Backend & AI Systems Engineer  
GitHub: https://github.com/venkatesh-reddy-prog  

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
