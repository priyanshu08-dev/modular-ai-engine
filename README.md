# Modular AI Engine

> A production-grade modular AI reasoning engine designed to power intelligent applications across multiple domains.

---

## Overview

**Modular AI Engine** is a reusable AI backend built with modern AI engineering principles.

Unlike traditional chatbot applications, this project is designed as an **AI platform** that can serve as the reasoning layer for different products and industries.

Possible applications include:

* 🏥 Healthcare assistants
* 🎓 Educational platforms
* 📚 Research copilots
* ⚖️ Legal assistants
* 🏢 Enterprise AI systems
* 📈 Business intelligence
* 🤖 Domain-specific AI copilots

The goal is to build a backend that remains independent of any single application while supporting multiple AI providers, Retrieval-Augmented Generation (RAG), workflow orchestration, and future AI capabilities.

---

# Project Vision

Traditional AI applications are often tightly coupled to a single model or use case.

Example:

```text
User
   │
   ▼
API
   │
   ▼
LLM
```

This project follows a different philosophy.

Instead of building another chatbot, we are building an **AI execution platform**.

Current architecture:

```text
Client
   │
   ▼
FastAPI
   │
   ▼
API Layer
   │
   ▼
Service Layer
   │
   ▼
AI Engine
   │
   ▼
Provider Factory
   │
   ▼
LLM Provider
```

As the project evolves, additional capabilities such as memory, RAG, LangGraph, and tools will plug into the AI Engine without changing the API layer.

---

# Current Features

## Backend

* FastAPI
* Application Factory pattern
* Environment-based configuration
* Health endpoint
* Swagger API documentation

---

## AI

- AI Engine orchestration layer
- Modular Execution Pipeline
- Conversation Memory
- Streaming Responses
- Server-Sent Events
- MemoryManager
- LangChain message-based execution
- Conversation ID support
- Provider abstraction
- Multi-provider architecture
- LangChain integration
- Groq integration

The AI Engine now supports stateful multi-turn conversations through a modular memory subsystem. Conversation history is represented using LangChain messages, enabling future capabilities such as Streaming, Retrieval-Augmented Generation (RAG), Tool Calling, and LangGraph workflows without changing the API layer.

---

## Providers

Current:

* ✅ Groq

Planned:

* OpenAI
* Gemini

---

## API

Implemented endpoints:

```text
GET  /health

POST /chat
```

---

## Configuration

* Environment variable management
* Pydantic Settings
* Provider configuration through `.env`

---

# Current Project Structure

```text
backend/

app/
│
├── api/
├── config/
├── engine/
│   ├── pipeline/
│   │   └── steps/
│   ├── execution_context.py
│   ├── core.py
│   └── prompt_manager.py
├── providers/
├── schemas/
├── services/
│
└── main.py
```

The `engine` package contains the core reasoning components, including the AI Engine, Execution Pipeline, and shared execution context.

---

# Technology Stack

## Backend

* Python 3.14
* FastAPI
* Uvicorn

## AI

* LangChain

## Planned

* LangGraph
* ChromaDB

## Dependency Management

* uv
* pyproject.toml

---

# Current Architecture

```text
Client

↓

FastAPI

↓

API Router

↓

Chat Service

↓

AI Engine

↓

Execution Pipeline

↓

Memory Step

↓

Provider Step
        │
        ├── execute()
        └── stream()

↓

Provider

↓

LLM
```

The Execution Pipeline now manages both conversation memory and provider execution while remaining fully modular.

## Request Flow

```text
Client

↓

FastAPI

↓

ChatService

↓

AIEngine

↓

ExecutionPipeline

↓

MemoryStep

↓

ProviderStep

↓

ProviderFactory

↓

Configured Provider

↓

LLM

↓

StreamingResponse
```

## Current Capabilities

- Real-time streaming AI responses
- Provider-independent streaming
- Conversation-aware streaming
- SSE protocol

# Conversation Memory

The Modular AI Engine now supports stateful conversations through a dedicated memory subsystem.

Each conversation is identified using a unique `conversation_id`.

The execution pipeline automatically retrieves previous conversation history, constructs the LangChain message list, invokes the configured provider, and stores the updated conversation.

This architecture keeps the AI Engine lightweight while allowing future memory implementations such as Redis, PostgreSQL, Vector Stores, or LangGraph State to replace the in-memory implementation without changing the engine.



# Development Principles

The project follows a small set of engineering principles.

* Build an AI platform instead of a chatbot.
* Keep responsibilities separated.
* Depend on abstractions instead of implementations.
* Build incrementally through stable milestones.
* Avoid unnecessary abstractions.
* Create files only when they provide real architectural value.

---

# Roadmap

### Completed

- ✅ Project Initialization
- ✅ FastAPI Foundation
- ✅ AI Chat Integration
- ✅ Provider Abstraction
- ✅ AI Engine
- ✅ Project Documentation
- ✅ Execution Pipeline
- ✅ Conversation Memory & LangChain Message Pipeline


### Planned

* Document Upload
* Document Parsing
* Embeddings
* ChromaDB Integration
* Retrieval Pipeline
* Retrieval-Augmented Generation (RAG)
* LangGraph Integration
* Tool Calling
* Multi-Agent Workflows
* Production Hardening

---

# Current Progress

Overall project completion:

~48%

The foundational architecture of the Modular AI Engine has been established, including the AI Engine, modular Execution Pipeline, provider abstraction, and project documentation.

Future milestones focus on expanding AI capabilities—such as Conversation Memory, Retrieval-Augmented Generation (RAG), Streaming, Tool Calling, and LangGraph—without requiring significant architectural changes.

---

# Documentation

Project documentation:

* README.md
* ARCHITECTURE.md
* PROJECTGUIDE.md
* ROADMAP.md
* CHANGELOG.md

Documentation evolves alongside the codebase. Every completed milestone includes synchronized updates to architecture, implementation guides, roadmap, and change history to keep the project documentation accurate and maintainable.

---

# Long-Term Vision

The long-term objective is to evolve this project from an AI backend into a complete AI reasoning platform capable of:

* Multi-provider support
* Retrieval-Augmented Generation (RAG)
* Workflow orchestration
* Tool calling
* Multi-agent systems
* Domain-specific copilots
* Intelligent request routing
* Scalable AI execution

The architecture is intentionally designed so these capabilities can be added without major changes to the existing codebase.

---

# Execution Pipeline

The AI Engine follows a modular execution pipeline where each stage is responsible for a single aspect of AI request processing.

```text
ExecutionContext

↓

ExecutionPipeline

↓

PromptStep

↓

ProviderStep

↓

AI Response
```

This design keeps the AI Engine lightweight while allowing future capabilities such as Conversation Memory, Retrieval-Augmented Generation (RAG), Tool Calling, Streaming, and LangGraph orchestration to be added without modifying the core engine.

---

# Project Status

🚧 Active Development

The project is under active development and follows a milestone-based workflow where each completed milestone produces:

* Working code
* Tested functionality
* Stable Git commit
* Updated documentation
