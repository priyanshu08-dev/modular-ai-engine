# Modular AI Engine

> A production-grade modular AI reasoning engine designed to power intelligent applications across multiple domains.

---

# Overview

**Modular AI Engine** is a reusable AI backend built using modern AI engineering principles.

Unlike traditional chatbot applications, this project is designed as an **AI execution platform** that serves as the reasoning layer for multiple products and industries.

Rather than coupling AI capabilities directly into an application, Modular AI Engine provides a clean, extensible backend that can evolve independently while exposing a stable API to client applications.

The architecture is intentionally modular, allowing new AI capabilities to be added without requiring major changes to the surrounding application.

---

# Why This Project Exists

Most AI applications today are tightly coupled to a specific Large Language Model (LLM), provider, or business workflow.

A typical architecture looks like this:

```text
User
   │
   ▼
API
   │
   ▼
LLM
```

While this approach works for simple chatbots, it becomes difficult to maintain as applications grow.

Adding capabilities such as:

- Conversation Memory
- Streaming Responses
- Retrieval-Augmented Generation (RAG)
- Tool Calling
- Workflow Orchestration
- Multi-Agent Systems

often requires significant architectural changes.

Modular AI Engine follows a different philosophy.

Instead of building another chatbot, it provides a reusable AI execution platform capable of powering many different applications through a stable and extensible architecture.

---

# Potential Applications

The engine is designed to support AI-powered applications across multiple domains, including:

- 🏥 Healthcare Assistants
- 🎓 Educational Platforms
- 📚 Research Copilots
- ⚖️ Legal Assistants
- 🏢 Enterprise AI Systems
- 📈 Business Intelligence
- 🤖 Domain-Specific AI Copilots
- 🧠 Personal AI Assistants

---

# Key Features

## Backend

- FastAPI backend
- Application Factory pattern
- Environment-based configuration
- Health monitoring endpoint
- Interactive Swagger API documentation

---

## AI Engine

- Modular AI execution engine
- Execution Pipeline architecture
- Provider abstraction layer
- Conversation Memory
- Streaming Responses
- Server-Sent Events (SSE)
- LangChain integration
- Conversation ID support
- Provider-independent architecture

---

## Document Processing

Currently supports:

- Document Upload API
- PDF parsing
- DOCX parsing
- TXT parsing
- Markdown parsing
- MIME type detection
- Automatic metadata extraction
- UUID-based upload storage
- Standardized document representation
- Recursive document chunking
- Configurable chunk size and overlap
- Configurable separator hierarchy
- Retrieval-ready chunk generation
- Provider-independent embedding generation
- Batch embedding generation
- Configurable embedding providers
- Standardized embedding abstractions

---

## Provider Support

### LLM Providers

#### Currently Supported

- ✅ Groq

#### Planned

- OpenAI
- Gemini

### Embedding Providers

#### Currently Supported

- ✅ Gemini
- ✅ OpenAI

---

# API Endpoints

Current endpoints:

```text
GET  /health

POST /chat

POST /documents/parse
```

---

# Technology Stack

## Backend

- Python 3.14
- FastAPI
- Uvicorn

## AI

- LangChain
- LangChain Text Splitters
- LangChain Google GenAI
- LangChain OpenAI

## Planned AI Technologies

- LangGraph
- ChromaDB

## Dependency Management

- uv
- pyproject.toml

---

# Project Structure

```text
app/

├── api/
├── chunking/
├── config/
├── document/
├── embeddings/
├── engine/
├── providers/
├── schemas/
├── services/
└── main.py
```

The project follows a layered architecture with clearly separated responsibilities, enabling the AI Engine to evolve independently from the API and application layers.

Complete architectural documentation is available in **PROJECTGUIDE.md**.

---

# Getting Started

## Clone the Repository

```bash
git clone <repository-url>
cd modular-ai-engine
```

---

## Install Dependencies

```bash
uv sync
```

---

## Configure Environment

Create a `.env` file in the project root.

Example:

```env
LLM_PROVIDER=groq
EMBEDDING_PROVIDER=gemini

GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
```

---

## Run the Development Server

```bash
uv run uvicorn app.main:app --reload
```

---

## API Documentation

After starting the server:

Swagger UI

```text
http://127.0.0.1:8000/docs
```

ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

# Current Status

**Version**

```
v0.7.0
```

**Status**

🚧 Active Development

The foundational architecture of the Modular AI Engine now includes:

- Modular AI Engine
- Execution Pipeline
- Conversation Memory
- Streaming Responses
- Provider Abstraction
- Document Processing
- Recursive Chunking Pipeline
- Provider-Independent Embedding Pipeline

The engine now supports a complete knowledge preparation workflow that transforms uploaded documents into standardized document objects, retrieval-ready chunks, and provider-independent vector embeddings, establishing the foundation for vector database integration, semantic retrieval, and Retrieval-Augmented Generation (RAG).

For detailed project progress and milestone tracking, see **ROADMAP.md**.

---

# Documentation

Project documentation is organized into dedicated documents, each with a specific responsibility.

| Document | Purpose |
|----------|---------|
| **README.md** | Project overview, features, setup, and quick start |
| **PROJECTGUIDE.md** | Complete technical handbook covering architecture, request flows, component responsibilities, engineering principles, and extension points |
| **ROADMAP.md** | Project planning, milestones, progress, future objectives, and long-term development strategy |
| **CHANGELOG.md** | Chronological history of completed milestones, architectural changes, and released features |

This separation keeps the documentation maintainable while avoiding duplication between documents.

---

# Long-Term Vision

The long-term objective is to evolve Modular AI Engine from a reusable AI backend into a complete AI reasoning platform capable of supporting:

- Multiple AI providers
- Retrieval-Augmented Generation (RAG) built on the completed document parsing, chunking, and embedding pipeline
- Workflow orchestration
- Tool Calling
- Multi-Agent Systems
- Intelligent request routing
- Domain-specific copilots
- Scalable AI execution

The architecture is intentionally designed so these capabilities can be introduced incrementally without major changes to the existing codebase.

---

# Contributing

The project follows a milestone-based engineering workflow focused on producing stable, production-quality software.

Contributors are encouraged to review **PROJECTGUIDE.md** before making architectural or structural changes to ensure consistency with the project's engineering principles.

---

# License

This project is currently under active development.

License information will be added before the first stable release.