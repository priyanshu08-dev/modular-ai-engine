# Roadmap

This document defines the long-term development plan for the **Modular AI Engine**.

Unlike the changelog, which records completed work, this roadmap focuses on the **current project state, future milestones, strategic objectives, and long-term vision**.

The project follows a milestone-driven, phase-based development process where every milestone delivers a stable, production-ready subsystem before moving to the next stage.

The roadmap is intentionally adaptive. As the architecture evolves, milestones may be reordered if doing so results in a cleaner or more maintainable design.

---

# Current Version

**v0.6.0**

---

# Current Status

## Development Status

🚧 Active Development

## Current Phase

✅ **Phase 3 — Knowledge & Retrieval**

## Current Milestone

⏳ **M11 — Chunking Pipeline**

## Last Completed Milestone

✅ **M10 — Document Upload & Processing**

---

# Overall Progress

```text
█████████████░░░░░░░

Phase Progress

Phase 1  ✅ 100%
Phase 2  ✅ 100%
Phase 3  ✅ 20%
Phase 4  ⬜ 0%
Phase 5  ⬜ 0%

Overall Project ≈ 63%
```

The foundational architecture of the Modular AI Engine has been established.

The remaining work primarily focuses on expanding AI capabilities—including knowledge retrieval, reasoning, orchestration, tooling, and production readiness—without requiring major architectural restructuring.

---

# Development Phases

---

# Phase 1 — Foundation

**Status:** ✅ Completed

### Objective

Build a clean, scalable backend architecture capable of supporting future AI capabilities without requiring major redesigns.

### Milestones

- ✅ M1 — Project Initialization
- ✅ M2 — FastAPI Foundation
- ✅ M3 — AI Chat Integration
- ✅ M4 — Provider Abstraction
- ✅ M5 — AI Engine
- ✅ M6 — Project Documentation

---

# Phase 2 — Core AI Engine

**Status:** ✅ Completed

### Objective

Transform the AI Engine into a modular execution platform capable of supporting advanced AI workflows.

### Milestones

- ✅ M7 — Execution Pipeline
- ✅ M8 — Conversation Memory & LangChain Message Pipeline
- ✅ M9 — Streaming Responses
- ✅ M10 — Document Upload & Processing

---

# Phase 3 — Knowledge & Retrieval

**Status:** 🚧 In Progress

### Objective

Enable the AI Engine to understand, retrieve, and reason over uploaded knowledge sources.

---

## M11 — Chunking Pipeline

**Status**

⏳ Next

### Objectives

- Chunk domain model
- ChunkManager
- Recursive text splitting
- Configurable chunk size
- Configurable chunk overlap
- Metadata inheritance
- Chunk validation

---

## M12 — Embeddings

### Objectives

- Generate vector embeddings
- Embedding abstraction
- Provider-independent embedding interface
- Batch embedding support

---

## M13 — ChromaDB Integration

### Objectives

- Persistent vector storage
- Similarity search
- Metadata filtering
- Collection management

---

## M14 — Retrieval Pipeline

### Objectives

- Semantic retrieval
- Top-K search
- Metadata-aware retrieval
- Retrieval abstraction
- Configurable ranking

---

## M15 — Retrieval-Augmented Generation (RAG)

### Objectives

- Context retrieval
- Prompt augmentation
- Context-aware AI responses
- Retrieval orchestration
- Source attribution
- Configurable retrieval strategies

---

# Phase 4 — Intelligence

**Status:** ⬜ Planned

### Objective

Transform the AI Engine from a conversational backend into a full AI reasoning platform.

---

## M16 — LangGraph Integration

### Objectives

- Workflow orchestration
- Stateful execution
- Dynamic routing
- Decision making
- Graph-based workflows

---

## M17 — Tool Calling

### Planned Tools

- Web Search
- SQL
- Calculator
- Python Execution
- Custom Tools

---

## M18 — Multi-Agent Workflows

### Planned Agents

- Research Agent
- Document Analysis Agent
- Report Generation Agent
- Planning Agent
- Domain-Specific Agents

---

# Phase 5 — Production

**Status:** ⬜ Planned

### Objective

Prepare the Modular AI Engine for production deployment and long-term maintainability.

---

## M19 — Testing

### Objectives

- Unit Tests
- Integration Tests
- API Tests
- Pipeline Tests
- Provider Tests

---

## M20 — Docker

### Objectives

- Dockerfile
- Docker Compose
- Containerized Development
- Production Containers

---

## M21 — CI/CD

### Objectives

- GitHub Actions
- Automated Testing
- Automated Quality Checks
- Deployment Pipelines

---

## M22 — Monitoring & Observability

### Objectives

- Structured Logging
- Metrics
- Request Tracing
- Performance Monitoring
- Error Tracking
- Health Monitoring

---

# Version 1 Goals

The first stable release should provide a production-grade modular AI backend capable of supporting multiple intelligent applications.

---

## Core AI

### Completed

- Multi-provider architecture
- AI Engine
- Execution Pipeline
- Conversation Memory
- Streaming Responses

### Planned Enhancements

- Workflow orchestration
- Tool Calling
- LangGraph integration

---

## Knowledge Processing

### Completed

- Document Upload
- PDF Parsing
- DOCX Parsing
- TXT Parsing
- Markdown Parsing

### Planned

- PPTX Support
- OCR
- Additional document formats

---

## Retrieval

Planned capabilities include:

- Embeddings
- Vector Database
- Semantic Retrieval
- Retrieval Pipeline
- Retrieval-Augmented Generation (RAG)

---

## Intelligence

The platform should support:

- LangGraph
- Tool Calling
- Workflow Routing
- Multi-Agent Systems
- Autonomous Reasoning

---

## API

The backend should provide:

- Production-ready FastAPI architecture
- Stable REST APIs
- Streaming endpoints
- Clean modular architecture
- Extensible provider integration

---

# Future Backlog

The following ideas are intentionally deferred until Version 1 reaches feature completeness.

---

## AI Platform

- Intelligent Provider Routing
- Prompt Registry
- Prompt Versioning
- Dynamic Prompt Loading
- AI Analytics Dashboard
- Token Usage Tracking
- Cost Tracking
- Latency Tracking
- Benchmark APIs

---

## Additional AI Capabilities

- OCR
- Speech-to-Text
- Text-to-Speech
- Vision Models
- Image Understanding
- Multimodal Workflows

---

## Infrastructure

- Redis
- PostgreSQL
- Elasticsearch
- Object Storage (S3 Compatible)
- Distributed Memory
- Distributed Vector Storage

---

## Domain Modules

- Healthcare Copilot
- Research Copilot
- Legal Assistant
- Education Assistant
- Enterprise Knowledge Assistant
- Business Intelligence Assistant

---

# Engineering Workflow

Every milestone follows the same development philosophy:

1. Architecture & Design
2. Implementation
3. Testing
4. Stable Git Commit
5. Documentation Update

Only thoroughly tested and stable milestones are considered complete.

---

# Engineering Philosophy

The roadmap is intentionally adaptive rather than rigid.

Good architecture always takes priority over following a predefined schedule.

If a better engineering solution is discovered during development, milestones may be reordered or expanded before implementation, provided that the overall architectural direction remains consistent.

Every milestone is expected to deliver:

- A stable implementation
- Production-quality code
- Updated documentation
- Clear separation of responsibilities
- Minimal technical debt

---

# Long-Term Vision

The long-term objective is to evolve **Modular AI Engine** from a reusable AI backend into a complete AI reasoning platform.

The final system should support:

- Multiple AI providers
- Retrieval-Augmented Generation (RAG)
- Workflow orchestration
- Conversation memory
- Tool execution
- Autonomous agents
- Intelligent routing
- Multi-agent collaboration
- Domain-specific copilots
- Scalable AI execution

while maintaining a clean, modular, extensible, and provider-independent architecture.

The architecture is intentionally designed so that each new capability can be integrated incrementally without requiring major changes to the existing system.