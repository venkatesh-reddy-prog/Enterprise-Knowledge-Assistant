🧠 Enterprise Knowledge Assistant
AI-Powered Semantic Search & Knowledge Retrieval Platform

Enterprise Knowledge Assistant is a scalable AI platform that enables organizations to perform intelligent, context-aware search across internal documents using vector embeddings and Retrieval-Augmented Generation (RAG).

Built to simulate a production-grade internal knowledge system used in modern enterprises.

🌍 What Problem Does It Solve?

Traditional search systems rely on keyword matching.
They fail when:

Documents are unstructured

Queries are semantic in nature

Large knowledge bases grow rapidly

Users expect natural-language answers instead of document links

This system enables semantic retrieval + grounded AI responses, ensuring relevant and explainable answers from enterprise data.

🏛 System Architecture Overview
User Query
    ↓
React Frontend
    ↓
Spring Boot Query Service
    ↓
Vector Similarity Search (Pinecone)
    ↓
Context Retrieval (Top-K Chunks)
    ↓
LLM Response Generation (OpenAI)
    ↓
Grounded AI Answer
🧩 Core Capabilities
📄 Intelligent Document Ingestion

Upload internal documents (PDF / text-based)

Automatic chunking strategy

Embedding generation using OpenAI

Vector storage in Pinecone

Metadata persistence in PostgreSQL

🔎 Semantic Query Processing

Converts user query into embeddings

Retrieves top-K semantically relevant chunks

Injects context into LLM prompt

Produces grounded, enterprise-aware responses

⚡ Scalable Microservices Design

Dedicated ingestion pipeline (FastAPI)

Independent query service (Spring Boot)

Stateless architecture

Easily horizontally scalable

🛠 Technology Stack
Backend Services

Java – Spring Boot (Query APIs)

Python – FastAPI (Ingestion Service)

RESTful Microservices Architecture

AI & Vector Infrastructure

OpenAI API (Embeddings + LLM)

Pinecone (Vector Database)

RAG (Retrieval-Augmented Generation)

Data Layer

PostgreSQL (Metadata & Logs)

Pinecone (Embeddings Index)

Frontend

React.js (User Interface)

DevOps

Docker (Containerization)

Environment-based configuration

CI/CD-ready service structure

🔁 How a Query Works (End-to-End Flow)

User submits a natural language question

Backend generates embedding for the query

Pinecone retrieves semantically similar document chunks

Retrieved context is injected into the LLM prompt

OpenAI generates a grounded response

Answer is returned to the frontend

This minimizes hallucinations and ensures responses are based on company data.

📦 Repository Structure
enterprise-knowledge-assistant/
 ├── frontend/
 │   ├── src/
 │   ├── components/
 │   └── package.json
 │
 ├── services/
 │   ├── query-service/ (Spring Boot)
 │   ├── ingestion-service/ (FastAPI)
 │   └── shared/
 │
 ├── docker-compose.yml
 └── README.md
🚀 Running Locally
1️⃣ Clone Repository
git clone https://github.com/venkatesh-reddy-prog/enterprise-knowledge-assistant.git
cd enterprise-knowledge-assistant
2️⃣ Configure Environment Variables

Create .env file:

OPENAI_API_KEY=your_key
PINECONE_API_KEY=your_key
PINECONE_ENV=your_env
PINECONE_INDEX=your_index
3️⃣ Start Services
docker-compose up --build

Or run individual services via:

Spring Boot

FastAPI

React

🔐 Security & Configuration

Secure API key handling via environment variables

Modular configuration for model upgrades

Separation of ingestion & query pipelines

Production-ready service layering

📈 Performance & Design Considerations

Efficient chunking strategy for embedding optimization

Asynchronous ingestion pipeline

Low-latency vector similarity search

Stateless backend services

Containerized multi-service architecture

🎯 Ideal Use Cases

Internal knowledge base search

HR policy assistant

Engineering documentation retrieval

Legal document search

Procurement intelligence systems

🧪 Challenges Solved

Embedding consistency across large documents

Vector index optimization

Prompt engineering for grounded responses

Managing async ingestion vs real-time querying

Environment configuration across multi-service deployment

🏗 Deployment Model
React Frontend
      ↓
Spring Boot Query Service
      ↓
FastAPI Ingestion Service
      ↓
Pinecone Vector Database
      ↓
OpenAI API

Fully containerized for cloud deployment (Render / AWS / GCP ready).

🧠 Concepts Demonstrated

Distributed Microservices Architecture

Retrieval-Augmented Generation (RAG)

Vector Databases & Embeddings

REST API Design

AI + Backend Integration

Containerized Deployment

Scalable Enterprise System Design

👨‍💻 Author

B. Venkatesh Reddy
Backend & AI Systems Engineer
GitHub: https://github.com/venkatesh-reddy-prog

⭐ Support

If you found this project useful or interesting, consider giving it a ⭐ on GitHub.
