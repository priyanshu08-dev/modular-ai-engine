# Roadmap

This document describes the long-term development roadmap of the **Modular AI Engine**.

The project follows a **phase-based** development process. Each phase focuses on building one major subsystem of the platform. Every milestone represents a stable, tested checkpoint before moving to the next objective.

The roadmap is intentionally flexible. As the architecture evolves, milestones may be reordered if a better engineering approach is discovered.

---

# Current Version

Current Version

v0.5.0

---

# Current Status

## Current Phase

✅ Phase 1 — Foundation

Current Milestone

✅ M9 — Streaming Responses (Completed)

Next Milestone

M10 — Document Upload & Processing

---

## Overall Progress

```text
███████████░░░░░░░░░

Phase Progress

Phase 1  ✅ 100%
Phase 2  ✅ 50%
Phase 3  ⬜ 0%
Phase 4  ⬜ 0%
Phase 5  ⬜ 0%

Overall Project ≈ 55%
```

The architectural backbone of the project has been completed.

The remaining work focuses primarily on adding AI capabilities rather than restructuring the application.

---

# Phase 1 — Foundation

Objective

Build a clean, production-grade backend architecture that future AI capabilities can plug into.

---

## M1 — Project Initialization

Status

✅ Completed

Delivered

- Git repository
- uv project initialization
- Python environment
- Project structure
- pyproject.toml
- Virtual environment

---

## M2 — FastAPI Foundation

Status

✅ Completed

Delivered

- FastAPI application
- Application Factory
- Lifespan events
- Environment configuration
- Health endpoint
- Swagger documentation

---

## M3 — AI Chat

Status

✅ Completed

Delivered

- Chat endpoint
- Chat service
- LangChain integration
- Groq integration
- First AI conversation

---

## M4 — Provider Abstraction

Status

✅ Completed

Delivered

- Base Provider
- Provider Factory
- Groq provider
- OpenAI placeholder
- Gemini placeholder

Result

Business logic no longer depends on a specific AI provider.

---

## M5 — AI Engine

Status

✅ Completed

Delivered

- AI Engine
- Prompt Manager
- Engine State
- Central AI execution layer

Result

All AI requests now flow through a single execution engine.

---

## M6 — Project Documentation

Status

✅ Completed

Delivered

- README.md
- ARCHITECTURE.md
- ROADMAP.md
- CHANGELOG.md
- PROJECTGUIDE.md

Result

Established a standardized documentation system that evolves alongside the codebase and serves as the single source of truth for architecture, development progress, and engineering decisions.

---

# Phase 2 — Core AI Engine

Objective

Transform the engine into an intelligent execution platform.

---

## M7 — Execution Pipeline

Status

✅ Completed

Delivered

- ExecutionPipeline
- ExecutionContext
- PromptStep
- ProviderStep
- AIEngine refactored into an orchestration layer

Result

The AI Engine now delegates execution through a modular pipeline, making it easy to introduce new capabilities such as Memory, RAG, Tool Calling, Streaming, and LangGraph without modifying the engine itself.

Current Execution Flow

```text
Request
↓
ExecutionContext
↓
ExecutionPipeline
↓
PromptStep
↓
ProviderStep
↓
Response
```

---

## M8 — Conversation Memory & LangChain Message Pipeline

Status

✅ Completed

Delivered

- MemoryManager
- BaseMemoryStore abstraction
- InMemoryStore
- MemoryStep
- Conversation ID support
- LangChain message-based execution context
- Shared application memory

Result

The AI Engine now supports stateful conversations while remaining provider-independent. Conversation history is represented using LangChain message objects, creating a foundation for future capabilities such as Streaming, RAG, Tool Calling, and LangGraph orchestration without requiring major architectural changes.
---

## M9 — Streaming Responses

Goal

Support real-time streaming of AI responses.

Benefits

- Better user experience
- Lower perceived latency
- Improved responsiveness


Delivered

- Streaming AI execution
- Streaming execution pipeline
- Provider-independent streaming
- Streaming ProviderStep
- Server-Sent Events (SSE)
- FastAPI StreamingResponse
- Streaming-first execution architecture

---

# Phase 3 — Knowledge Layer

Objective

Enable Retrieval-Augmented Generation.

---

## M10 — Document Upload

Supported formats

- PDF
- DOCX
- PPTX
- TXT
- Markdown

---

## M11 — Document Processing

Capabilities

- Text extraction
- Cleaning
- Metadata extraction
- Normalization

---

## M12 — Embeddings

Generate vector embeddings for processed documents.

---

## M13 — ChromaDB Integration

Capabilities

- Persistent storage
- Similarity search
- Metadata filtering

---

## M14 — Retrieval Pipeline

Capabilities

- Semantic retrieval
- Top-K search
- Metadata-aware search

---

## M15 — Retrieval-Augmented Generation (RAG)

Execution

```
Question

↓

Retrieve Context

↓

Prompt Construction

↓

LLM

↓

Response
```

---

# Phase 4 — Intelligence

Objective

Transform the AI Engine into a reasoning engine.

---

## M16 — LangGraph Integration

Responsibilities

- Workflow orchestration
- State management
- Routing
- Decision making

---

## M17 — Tool Calling

Planned tools

- Web Search
- SQL
- Calculator
- Python Execution

---

## M18 — Multi-Agent Workflows

Possible agents

- Research Agent
- Document Analysis Agent
- Report Generation Agent
- Domain-specific Agents

---

# Phase 5 — Production

Objective

Prepare the platform for deployment.

---

## M19 — Testing

- Unit Tests
- Integration Tests
- API Tests

---

## M20 — Docker

- Dockerfile
- Docker Compose
- Containerized deployment

---

## M21 — CI/CD

Possible integrations

- GitHub Actions
- Automated testing
- Deployment pipelines

---

## M22 — Monitoring & Observability

Planned

- Structured logging
- Request tracing
- Metrics
- Performance monitoring
- Error tracking

---

# Version 1 Goals

The first stable release should include

## Core AI

Completed

- Multi-provider support
- AI Engine
- Execution Pipeline

Planned

- Conversation Memory
- Streaming Responses

---

## Knowledge

- PDF
- DOCX
- PPTX
- TXT
- Markdown

---

## Retrieval

- Embeddings
- ChromaDB
- Semantic Search
- Retrieval Pipeline
- RAG

---

## Intelligence

- LangGraph
- Tool Calling
- Workflow Routing

---

## API

- Production-ready FastAPI backend
- Swagger documentation
- Clean modular architecture

---

# Future Backlog

These ideas are intentionally postponed until Version 1 is stable.

## AI

- Intelligent Provider Routing
- Prompt Registry
- Prompt Versioning
- Dynamic Prompt Loading
- Benchmark Endpoint
- AI Analytics Dashboard
- Token Usage Tracking
- Cost Tracking
- Latency Tracking

---

## Tools

- OCR
- Speech-to-Text
- Text-to-Speech
- Vision Models

---

## Integrations

- Redis
- PostgreSQL
- Elasticsearch
- S3 Storage

---

## Domain Modules

- Healthcare Copilot
- Research Copilot
- Legal Assistant
- Education Assistant
- Enterprise Knowledge Assistant

---

# Engineering Philosophy

The roadmap is intentionally adaptive.

Good architecture takes priority over following a fixed plan.

If a better design is discovered during development, milestones may be reordered before implementation.

Every milestone follows the same engineering workflow.

```
Architecture

↓

Implementation

↓

Testing

↓

Git Commit

↓

Documentation Update
```

Only tested and stable milestones are considered complete.

---

# Long-Term Vision

The long-term objective is to evolve Modular AI Engine from a reusable AI backend into a complete AI reasoning platform.

The final system should support

- Multiple AI providers
- Retrieval-Augmented Generation
- Workflow orchestration
- Memory
- Tool execution
- Autonomous agents
- Domain-specific copilots

while maintaining a clean, modular and extensible architecture.