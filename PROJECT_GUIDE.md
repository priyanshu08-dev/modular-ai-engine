# Project Guide

> Complete technical handbook for the **Modular AI Engine**.

This document serves as the authoritative technical reference for developers contributing to the Modular AI Engine. It explains the internal architecture, engineering principles, component responsibilities, request lifecycles, design decisions, and extension points that make up the platform.

Unlike **README.md**, which provides a high-level project overview, this guide focuses on **how the system works internally** and **why the architecture has been designed the way it has**.

The objective is to ensure that any contributor can understand, extend, and maintain the system without reverse engineering the codebase.

---

# Current Purpose

The Modular AI Engine is **not** a chatbot application.

It is a reusable, production-grade AI execution platform designed to serve as the reasoning layer for multiple kinds of software systems.

Instead of embedding AI logic directly inside an application, client applications communicate with a stable API while the AI Engine performs all reasoning internally.

The architecture is intentionally modular so that new AI capabilities can be introduced without requiring major changes to existing application layers.

The long-term goal is to evolve the project into a complete AI reasoning platform capable of supporting advanced workflows while maintaining a clean, maintainable architecture.

---

# Design Philosophy

Traditional AI applications often follow a tightly coupled architecture where the application communicates directly with a specific Large Language Model.

A simplified architecture typically looks like this:

```text
User
   │
   ▼
API
   │
   ▼
LLM
```

Although this approach works for small chatbot applications, it becomes increasingly difficult to maintain as new AI capabilities are introduced.

Features such as:

* Conversation Memory
* Streaming Responses
* Retrieval-Augmented Generation (RAG)
* Tool Calling
* Workflow Orchestration
* Multi-Agent Systems
* Intelligent Routing

often require significant modifications to application logic.

The Modular AI Engine takes a fundamentally different approach.

Rather than building an application around a model, it introduces a dedicated AI execution layer responsible for coordinating every AI capability.

The surrounding application remains largely unchanged while the execution engine continues to evolve.

---

# High-Level Architecture

The current architecture separates application concerns into independent layers.

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
                ┌────────┴────────┐
                ▼                 ▼
           AI Engine      Document Processing
                │                 │
                ▼                 ▼
      Execution Pipeline      Chunking
                │                 │
                └────────┬────────┘
                         ▼
                  Provider Layer
                         │
                         ▼
                         LLM
```

Each layer owns a single responsibility.

The API layer never performs AI reasoning.

The Service layer coordinates business workflows without embedding implementation details.

The AI Engine orchestrates conversational reasoning while remaining provider-independent.

The Document Processing subsystem transforms uploaded files into standardized `Document` objects.

The Chunking subsystem converts standardized documents into retrieval-ready chunks without depending on file formats or parsing implementations.

Providers remain responsible only for communicating with external AI services.

This separation enables every subsystem to evolve independently while preserving stable interfaces across the application.

---

# Architectural Principles

The architecture is built around several fundamental principles.

## 1. Separation of Responsibilities

Every component should have one clearly defined responsibility.

Examples:

* API handles HTTP.
* Services coordinate business workflows.
* AI Engine orchestrates reasoning.
* Providers communicate with external LLMs.
* Document subsystem processes uploaded files.

No layer should assume responsibilities belonging to another.

---

## 2. Provider Independence

The application should never depend directly on a specific AI provider.

Instead, providers are selected through the Provider Factory, allowing the engine to support multiple LLM vendors without changing business logic.

Current implementation supports:

* Groq

Planned providers include:

* OpenAI
* Gemini

Future providers should integrate by implementing the existing provider interface rather than modifying the AI Engine.

---

## 3. Extensibility

The architecture is designed so that future capabilities can be introduced as independent modules.

Examples include:

* Retrieval-Augmented Generation (RAG)
* Tool Calling
* LangGraph Workflows
* Multi-Agent Systems
* Advanced Memory Backends
* Workflow Routing

The goal is to extend the system through composition rather than modification.

---

## 4. Stable Interfaces

Public interfaces between layers should remain stable even as internal implementations evolve.

For example:

* API endpoints should remain unchanged while execution logic evolves.
* Services should remain unaware of provider implementations.
* Providers should be replaceable without affecting application code.
* Memory implementations should be interchangeable without changing the execution pipeline.

---

## 5. Incremental Evolution

The project is developed through stable milestones.

Each milestone introduces one major capability while preserving existing functionality.

This minimizes architectural churn and ensures that the platform remains production-ready throughout development.

---

# Request Lifecycle

Every user request follows a predictable execution path through the system.

```text
Client
        │
        ▼
FastAPI
        │
        ▼
API Router
        │
        ▼
Service Layer
        │
        ▼
AIEngine
        │
        ▼
ExecutionContext
        │
        ▼
ExecutionPipeline
        │
        ├───────────────┐
        ▼               │
MemoryStep              │
        ▼               │
ProviderStep            │
        │               │
        ├── execute()   │
        └── stream()    │
        ▼
ProviderFactory
        │
        ▼
Configured Provider
        │
        ▼
Large Language Model
        │
        ▼
StreamingResponse / Standard Response
        │
        ▼
Client
```

The AI Engine serves as the orchestration layer and delegates work to the Execution Pipeline.

Each pipeline step focuses on a single responsibility, allowing the pipeline to evolve without changing the engine itself.

---

# Streaming Request Lifecycle

Streaming follows the same architectural path as synchronous execution.

Only the provider execution stage changes.

```text
Client
        │
        ▼
FastAPI
        │
        ▼
ChatService
        │
        ▼
AIEngine.stream()
        │
        ▼
ExecutionPipeline.stream()
        │
        ▼
MemoryStep.execute()
        │
        ▼
ProviderStep.stream()
        │
        ▼
Configured Provider
        │
        ▼
Large Language Model
        │
        ▼
Server-Sent Events (SSE)
        │
        ▼
StreamingResponse
        │
        ▼
Client
```

This design avoids maintaining two completely separate execution paths.

Instead, streaming and synchronous execution share nearly identical orchestration logic, reducing complexity and improving maintainability.

---

# Document Processing Lifecycle

The document subsystem follows an independent processing workflow that converts uploaded files into standardized domain objects before any downstream knowledge-processing occurs.

```text
Client
    │
    ▼
Document API
    │
    ▼
DocumentService
    │
    ▼
DocumentStorage
    │
    ▼
DocumentManager
    │
    ▼
DocumentDetector
    │
    ▼
DocumentParserFactory
    │
    ▼
BaseDocumentParser
    │
    ▼
Concrete Parser
(PDF / DOCX / TXT / Markdown)
    │
    ▼
Document
    │
    ▼
ChunkManager
    │
    ▼
Chunking Strategy
    │
    ▼
ChunkingResult
```

The parsing subsystem and the chunking subsystem remain independent.

Document Processing is responsible only for producing standardized `Document` objects.

The Chunking subsystem operates exclusively on those domain objects to generate retrieval-ready chunks for future embedding and retrieval pipelines.

---

# Relationship Between Major Subsystems

The project currently consists of several independent but cooperating subsystems.

```text
                           Modular AI Engine
                                   │
      ┌────────────────────────────┼────────────────────────────┐
      │                            │                            │
      ▼                            ▼                            ▼
 API Layer                   AI Engine              Document Processing
      │                            │                            │
      ▼                            ▼                            ▼
Service Layer            Execution Pipeline         DocumentManager
      │                            │                            │
      ▼                            ▼                            ▼
 Schemas               Memory / Providers          Chunking Pipeline
                                                     │
                                                     ▼
                                                Retrieval Foundation
```

Each subsystem owns a clearly defined architectural boundary.

The AI Engine is responsible for reasoning and orchestration.

The Document Processing subsystem is responsible for knowledge ingestion.

The Chunking subsystem forms the bridge between document ingestion and future retrieval capabilities such as embeddings, vector databases, semantic search, and Retrieval-Augmented Generation (RAG).

Stable interfaces between these subsystems allow future capabilities to be added through extension rather than modification.

---

# Why This Architecture?

The architecture intentionally favors **composition over coupling**.

Instead of embedding every capability inside one large AI service, responsibilities are distributed across focused components that can evolve independently.

As future milestones introduce capabilities such as:

* Chunking
* Embeddings
* Vector Databases
* Retrieval
* Retrieval-Augmented Generation (RAG)
* LangGraph
* Tool Calling
* Multi-Agent Systems

the AI Engine should require minimal structural changes.

Most new functionality will integrate by extending existing abstractions rather than rewriting existing components.

Examples include:

- New PipelineSteps
- Additional Provider implementations
- New Memory backends
- Additional Document parsers
- New Chunking strategies
- Embedding providers
- Retrieval engines
- Tool execution
- Workflow orchestration

The introduction of the Chunking subsystem reinforces this philosophy by separating document ingestion from retrieval preparation. Future retrieval capabilities will build upon standardized chunks without requiring modifications to either the document processing pipeline or the AI Engine.


# 2. Project Structure

The Modular AI Engine follows a layered, modular architecture where each package is responsible for one well-defined aspect of the system.

The directory structure is intentionally designed to keep business logic independent from infrastructure concerns, allowing each subsystem to evolve without impacting the rest of the application.

Current project structure:

```text
app/
│
├── api/
├── chunking/
│   ├── strategies/
│   ├── manager.py
│   ├── models.py
│   └── exceptions.py
│
├── config/
├── document/
├── engine/
│   ├── memory/
│   ├── pipeline/
│   │   ├── steps/
│   │   └── base.py
│   ├── execution_context.py
│   └── core.py
│
├── providers/
├── schemas/
├── services/
│
└── main.py
```

Every package has a clearly defined responsibility. Code should always be added to the layer that naturally owns the responsibility instead of creating shortcuts between components.

---

# Layer Responsibilities

The backend is organized into multiple logical layers.

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
   ├──────────────┐
   ▼              ▼
AI Engine   Document Processing
   │              │
   ▼              ▼
Execution     Chunking
Pipeline         │
   │             ▼
   ▼       Retrieval Foundation
Provider
   │
   ▼
External AI Services
```

Each layer communicates only with the layer directly beneath or the subsystem it owns.

This structure preserves clear dependency direction while enabling the document ingestion and AI reasoning pipelines to evolve independently.

---

# Package Responsibilities

---

## api/

### Purpose

The API layer is responsible for exposing HTTP endpoints to external clients.

It acts as the public interface of the application.

### Responsibilities

* Define API routes
* Receive HTTP requests
* Validate request payloads
* Call appropriate services
* Serialize responses
* Return HTTP status codes
* Handle API-level errors

### Never Responsible For

* AI reasoning
* Business logic
* Provider communication
* Prompt generation
* Document parsing

The API layer should remain extremely lightweight.

Example request flow:

```text
POST /chat
        │
        ▼
ChatService
```

---

## config/

### Purpose

Centralize every configurable aspect of the application.

No configuration should be hardcoded anywhere else.

### Responsibilities

* Environment variables
* Application settings
* Provider configuration
* Feature flags
* Runtime configuration
* Development configuration

Typical configuration includes:

* Application name
* Debug mode
* Active provider
* API keys
* Upload settings
* Future retrieval configuration

All application components should import configuration from this package.

---

## services/

### Purpose

The Service layer represents the application's business use cases.

Services coordinate workflows between multiple subsystems but should never implement those subsystems themselves.

Current examples include:

* ChatService
* DocumentService

### Responsibilities

* Coordinate application workflows
* Validate business operations
* Delegate AI work to the AI Engine
* Delegate document processing
* Return standardized results

### Never Responsible For

* Direct LLM communication
* Prompt construction
* Memory implementation
* Provider selection
* File parsing

A service should orchestrate—not execute.

Example:

```text
API
        │
        ▼
ChatService
        │
        ▼
AIEngine
```

---

## engine/

### Purpose

The Engine package is the core of the Modular AI Engine.

It is responsible for orchestrating every AI execution.

All reasoning capabilities eventually pass through this package.

### Current Responsibilities

* Create ExecutionContext
* Execute the Execution Pipeline
* Coordinate conversation memory
* Support synchronous execution
* Support streaming execution
* Return final responses
* Coordinate future AI capabilities

The Engine does **not** perform provider-specific work.

Instead, it delegates responsibilities to independent pipeline components.

---

### Internal Structure

```text
engine/

├── core.py
├── execution_context.py
│
├── memory/
│
├── pipeline/
│   ├── pipeline.py
│   ├── context.py
│   ├── base.py
│   └── steps/
```

As the project grows, additional AI capabilities will primarily be implemented inside this package.

---

## engine/memory/

### Purpose

Provide a provider-independent memory subsystem.

### Responsibilities

* Conversation management
* Conversation history
* Storage abstraction
* Memory persistence
* Future memory backends

Current implementation:

* MemoryManager
* BaseMemoryStore
* InMemoryStore

Future implementations may include:

* RedisMemoryStore
* PostgreSQLMemoryStore
* VectorMemoryStore
* LangGraph State

The AI Engine should never depend on a particular storage implementation.

---

## engine/pipeline/

### Purpose

Coordinate AI execution through independent execution stages.

Each stage owns exactly one responsibility.

Current pipeline:

```text
ExecutionPipeline

        │

        ▼

MemoryStep

        ▼

ProviderStep
```

Future pipeline:

```text
ExecutionPipeline

        ▼

RoutingStep

        ▼

MemoryStep

        ▼

RetrieverStep

        ▼

RAGStep

        ▼

ToolStep

        ▼

ProviderStep
```

This architecture allows new capabilities to be added without modifying existing steps.

---

## providers/

### Purpose

Provide a uniform interface to external AI providers.

### Current Provider

* Groq

### Planned Providers

* OpenAI
* Gemini

### Responsibilities

* Authentication
* Model configuration
* LangChain model creation
* Streaming implementation
* Provider-specific communication

### Never Responsible For

* Business logic
* Routing
* Prompt management
* Conversation management
* API responses

The rest of the application should never know which provider is active.

---

## document/

### Purpose

Provide a complete document processing subsystem.

This package is entirely independent from the AI Engine and focuses exclusively on processing uploaded documents.

### Responsibilities

* Document storage
* File validation
* MIME detection
* Parser selection
* Metadata extraction
* Domain model creation

The document subsystem is intentionally modular so that additional document formats can be supported with minimal changes.

---

## chunking/

### Purpose

Provide a provider-independent document chunking subsystem.

The chunking package transforms standardized `Document` domain objects into retrieval-ready chunks that can be consumed by future embedding generation, vector databases, semantic retrieval, and Retrieval-Augmented Generation (RAG).

By isolating chunking from document parsing, the project preserves a clean separation between knowledge ingestion and knowledge preparation.

---

### Responsibilities

* Coordinate document chunking
* Apply configurable chunking strategies
* Generate standardized Chunk domain models
* Preserve document metadata across chunks
* Produce retrieval-ready output
* Support future chunking algorithms

The chunking subsystem never parses uploaded files.

It operates exclusively on standardized `Document` objects produced by the Document Processing subsystem.

---

### Internal Structure

```text
chunking/

├── manager.py
├── models.py
├── exceptions.py
└── strategies/
    ├── base.py
    ├── recursive.py
    └── semantic.py
```

The package follows a modular architecture where orchestration, domain models, and chunking algorithms remain independent.

---

### Design Philosophy

Rather than embedding chunking logic into the document processing pipeline, chunk generation is treated as its own architectural concern.

This separation provides several advantages:

* Parser independence
* Strategy-based extensibility
* Easier testing
* Cleaner retrieval pipeline
* Future semantic chunking support
* Provider-independent preprocessing

As future milestones introduce embeddings and retrieval, the chunking subsystem should require little or no structural modification.

---

## schemas/

### Purpose

Define API contracts.

Schemas represent the public interface of the application.

### Responsibilities

* Request models
* Response models
* Validation
* Serialization
* API data contracts

Schemas should never contain business logic.

Their responsibility is limited to describing data entering and leaving the application.

---

# ChunkManager

## Purpose

ChunkManager coordinates the complete chunk generation workflow.

Instead of embedding splitting logic throughout the application, it centralizes orchestration while delegating the actual chunking algorithm to interchangeable strategies.

---

## Responsibilities

* Receive standardized Document objects
* Select the configured chunking strategy
* Coordinate chunk generation
* Build ChunkingResult
* Preserve document metadata
* Return retrieval-ready chunks

ChunkManager does not implement any chunking algorithm itself.

Its responsibility is orchestration rather than execution.

---

# Chunk Domain Model

## Purpose

Chunking converts a single Document into multiple standardized Chunk objects.

Conceptually:

```text
Document

      │

      ▼

Chunk 1
Chunk 2
Chunk 3
Chunk 4
...
```

Every Chunk represents a small, self-contained portion of the original document while preserving sufficient metadata to reconstruct its origin.

Current chunk metadata includes:

* Chunk identifier
* Document identifier
* Chunk index
* Character offsets
* Chunk content

Future metadata may include:

* Token count
* Page number
* Section hierarchy
* Heading information
* Semantic score
* Embedding identifier

Standardizing chunk metadata allows future retrieval systems to operate consistently regardless of document format.

---

# ChunkingResult

## Purpose

Provide a standardized return object for the chunking subsystem.

Rather than returning raw collections of chunks, every chunking operation produces a ChunkingResult.

---

## Responsibilities

* Store generated chunks
* Preserve document-level metadata
* Report chunk statistics
* Provide a stable interface for downstream pipelines

Future milestones such as embedding generation and retrieval will consume ChunkingResult instead of interacting directly with chunking implementations.

---

# Chunking Strategies

The chunking subsystem follows the Strategy Pattern.

Instead of coupling the application to a single chunking algorithm, ChunkManager delegates chunk generation to interchangeable strategies.

Current strategy:

* RecursiveChunkingStrategy

Future strategies may include:

* SemanticChunkingStrategy
* TokenBasedChunkingStrategy
* MarkdownAwareChunkingStrategy
* HTMLStructureChunkingStrategy
* CodeAwareChunkingStrategy

Supporting a new chunking algorithm should require implementing a new strategy rather than modifying existing orchestration logic.

---

# RecursiveChunkingStrategy

## Purpose

Provide the default chunking implementation for the platform.

The strategy uses LangChain's RecursiveCharacterTextSplitter to produce retrieval-ready chunks while respecting configurable chunk sizes, overlap, and separator hierarchy.

---

## Responsibilities

* Split standardized document text
* Preserve logical text boundaries where possible
* Apply configurable chunk size
* Apply configurable chunk overlap
* Preserve separator hierarchy
* Build standardized Chunk models

The implementation is intentionally independent of document formats, allowing the same algorithm to operate on every supported document type.

---

# Future Chunking Strategies

The Strategy Pattern allows specialized chunking algorithms to be introduced without modifying ChunkManager or downstream retrieval components.

Examples include:

* Semantic chunking
* Structure-aware chunking
* Heading-aware chunking
* Code-aware chunking
* Token-aware chunking
* Language-specific chunking

Each implementation should conform to the same strategy interface, ensuring consistent orchestration while allowing the chunking algorithm itself to evolve independently.

---

## main.py

### Purpose

Application entry point.

Responsibilities include:

* Creating the FastAPI application
* Registering routers
* Initializing application lifecycle
* Configuring startup and shutdown events
* Bootstrapping the backend

No business logic should exist inside this file.

---

# Dependency Direction

Dependencies always flow downward.

```text
main.py
        │
        ▼
api/
        │
        ▼
services/
        │
        ▼
engine/
        │
        ▼
providers/
        │
        ▼
LangChain
        │
        ▼
External Provider APIs
```

The document subsystem follows its own dependency chain.

```text
api/
        │
        ▼
services/
        │
        ▼
document/
        │
        ▼
Parsers
        │
        ▼
External Parsing Libraries
```

Higher-level layers may depend on lower layers.

Lower-level layers must **never** import higher layers.

This rule prevents circular dependencies and preserves architectural boundaries.

---

# Package Interaction

The following diagram illustrates how the primary packages interact during execution.

```text
                Client
                   │
                   ▼
              FastAPI API
                   │
                   ▼
               api/
                   │
                   ▼
             services/
          ┌────────┴────────┐
          ▼                 ▼
     engine/           document/
          │                 │
          ▼                 ▼
    providers/         parsers/
          │
          ▼
      LangChain
          │
          ▼
     AI Providers
```

Although the Engine and Document subsystems are independent, they are intentionally designed to integrate naturally in future milestones.

For example, once Retrieval-Augmented Generation (RAG) is introduced, the AI Engine will retrieve processed document knowledge through well-defined interfaces instead of directly coupling itself to the document subsystem.

---

# Layer Design Rules

Every package in the project follows a common set of architectural rules.

### Rule 1 — One Responsibility Per Package

Every package should answer one architectural question.

Examples:

* **api/** → How does the outside world communicate with the system?
* **services/** → What business workflow is being performed?
* **engine/** → How is AI reasoning executed?
* **providers/** → Which AI provider is being used?
* **document/** → How are documents processed?

---

### Rule 2 — Depend on Abstractions

Whenever possible, components should depend on interfaces rather than concrete implementations.

Examples include:

* ProviderFactory
* BaseMemoryStore
* BaseDocumentParser

This allows implementations to change without affecting higher layers.

---

### Rule 3 — Keep Layers Independent

Every layer should evolve independently.

Adding:

* a new provider,
* a new parser,
* a new memory backend,
* a new retrieval engine,

should require changes only within the subsystem that owns that responsibility.

---

### Rule 4 — Prefer Extension Over Modification

New capabilities should be introduced by extending the architecture instead of rewriting existing components.

Examples include:

* Adding a new PipelineStep
* Adding a new Provider
* Adding a new Document Parser
* Adding a new MemoryStore

This philosophy minimizes regression risk while keeping the architecture scalable.

---

# Architectural Goal

The project structure is intentionally designed to remain stable as the system grows.

Future milestones should primarily introduce **new modules** rather than requiring significant modifications to existing ones.

This stability allows the Modular AI Engine to evolve from a simple AI backend into a complete reasoning platform while preserving clean boundaries, maintainability, and long-term extensibility.



# 3. Core AI Engine

The **AI Engine** is the heart of the Modular AI Engine platform.

Rather than directly communicating with Large Language Models (LLMs), the AI Engine serves as an orchestration layer responsible for coordinating every AI-related operation through a modular execution pipeline.

This architectural separation allows the system to evolve from a simple conversational backend into a complete AI reasoning platform without requiring major structural changes.

---

# AI Engine Overview

The AI Engine is intentionally lightweight.

Its responsibility is **not** to perform every AI operation itself, but rather to coordinate the execution of specialized components.

Current responsibilities include:

* Building the execution context
* Initializing pipeline execution
* Supporting synchronous execution
* Supporting streaming execution
* Returning completed responses
* Delegating provider communication
* Coordinating conversation memory
* Acting as the central entry point for AI reasoning

The AI Engine should never become a monolithic class containing provider logic, prompt generation, memory implementation, or retrieval logic.

Instead, these capabilities are delegated to dedicated subsystems.

---

# AI Execution Lifecycle

Every AI request follows the same lifecycle.

```text
Client
        │
        ▼
ChatService
        │
        ▼
AIEngine
        │
        ▼
ExecutionContext
        │
        ▼
ExecutionPipeline
        │
        ▼
Pipeline Steps
        │
        ▼
Provider
        │
        ▼
LLM
        │
        ▼
Response
```

The AI Engine itself does not perform reasoning.

It simply coordinates execution.

---

# AIEngine

## Purpose

The AIEngine acts as the central orchestration layer for every AI request.

Every capability introduced into the platform should integrate with the AIEngine instead of bypassing it.

---

## Current Responsibilities

* Accept execution requests
* Create ExecutionContext
* Invoke ExecutionPipeline
* Support synchronous execution
* Support streaming execution
* Return standardized responses
* Coordinate conversation memory
* Maintain provider independence

---

## Future Responsibilities

As the platform evolves, the AIEngine will coordinate additional capabilities such as:

* Retrieval-Augmented Generation (RAG)
* Tool Calling
* LangGraph workflows
* Multi-Agent coordination
* Workflow routing
* Planning
* AI analytics
* Token accounting

The AIEngine should coordinate these capabilities without implementing them directly.

---

# ExecutionContext

## Purpose

ExecutionContext represents the complete state of a single AI execution.

Instead of passing multiple objects through the pipeline, every pipeline step receives and updates the same shared execution context.

This creates a consistent execution model while keeping components loosely coupled.

---

## Current Responsibilities

ExecutionContext currently stores:

* Conversation ID
* User input
* LangChain message history
* Final response
* Execution metadata

Each pipeline step can safely read from or update the shared context.

---

## Future Responsibilities

ExecutionContext is expected to evolve into the central state container for the entire reasoning engine.

Future fields may include:

* Retrieved documents
* Chunk references
* Embeddings
* Tool outputs
* Workflow state
* Streaming metadata
* Token usage
* Latency metrics
* Provider information
* Execution traces
* Reasoning metadata

This design allows new capabilities to be introduced without changing existing method signatures.

---

# Execution Pipeline

## Purpose

The Execution Pipeline coordinates AI execution through independent execution stages.

Rather than embedding every operation inside the AIEngine, responsibilities are distributed across specialized pipeline steps.

This makes the execution flow easier to understand, test, extend, and maintain.

---

## Current Pipeline

```text
ExecutionPipeline

        │

        ▼

MemoryStep

        ▼

ProviderStep
```

Each step performs one well-defined responsibility before passing the updated ExecutionContext to the next step.

---

## Why a Pipeline?

A pipeline architecture provides several advantages.

### Separation of Concerns

Each pipeline step owns exactly one responsibility.

### Extensibility

New capabilities can be introduced without modifying existing steps.

### Testability

Pipeline steps can be tested independently.

### Reusability

Execution stages can be reused across different workflows.

### Maintainability

Complex reasoning is divided into small, understandable components.

---

# PipelineStep

Every execution stage inherits from a common PipelineStep abstraction.

Each PipelineStep is responsible for one operation only.

Examples include:

* Memory management
* Retrieval
* Tool execution
* Provider invocation

The base PipelineStep provides shared execution behavior while allowing specialized implementations to override functionality when necessary.

---

# MemoryStep

## Purpose

MemoryStep is responsible for preparing the conversation before AI execution.

Responsibilities include:

* Loading conversation history
* Building LangChain messages
* Creating new conversations
* Updating ExecutionContext
* Delegating persistence to MemoryManager

MemoryStep never communicates directly with providers.

---

# ProviderStep

## Purpose

ProviderStep is responsible for interacting with the configured AI provider.

It is the only pipeline step that communicates directly with Large Language Models.

---

## Current Responsibilities

* Retrieve configured provider
* Execute synchronous requests
* Execute streaming requests
* Update conversation history
* Persist conversation state
* Update ExecutionContext
* Return provider responses

---

## Streaming Behavior

ProviderStep is currently the only execution stage with custom streaming behavior.

All other pipeline steps inherit the default streaming implementation supplied by the Pipeline framework.

This design minimizes duplicated streaming logic while allowing provider communication to remain specialized.

---

# Streaming Architecture

Streaming is treated as a first-class execution model.

Rather than maintaining two different execution paths, synchronous execution and streaming execution share almost identical orchestration.

Current streaming flow:

```text
Client

        │

        ▼

ChatService

        ▼

AIEngine.stream()

        ▼

ExecutionPipeline.stream()

        ▼

MemoryStep.execute()

        ▼

ProviderStep.stream()

        ▼

Configured Provider

        ▼

Large Language Model

        ▼

Server-Sent Events (SSE)

        ▼

StreamingResponse

        ▼

Client
```

Current streaming events include:

* metadata
* token
* done

Planned future events include:

* retrieval
* tool_start
* tool_end
* reasoning
* progress
* error

---

# Conversation Memory Architecture

The platform supports stateful multi-turn conversations through a dedicated memory subsystem.

The memory architecture is intentionally independent from both providers and the AI Engine.

```text
Client

        │

        ▼

Conversation ID

        │

        ▼

MemoryManager

        │

        ▼

MemoryStore

        │

        ▼

Conversation History

        │

        ▼

ExecutionContext
```

Every conversation is identified using a unique `conversation_id`.

The execution pipeline automatically:

1. Retrieves conversation history.
2. Builds LangChain message objects.
3. Invokes the configured provider.
4. Stores the updated conversation.

The AIEngine itself remains unaware of the underlying storage implementation.

---

# Memory Subsystem

## Purpose

Provide provider-independent conversation persistence.

---

## Current Components

* MemoryManager
* BaseMemoryStore
* InMemoryStore

---

## MemoryManager

Coordinates the entire conversation lifecycle.

Responsibilities include:

* Create conversations
* Retrieve conversations
* Persist conversations
* Manage memory implementations

---

## BaseMemoryStore

Defines the interface every memory backend must implement.

Current implementations depend only on this abstraction.

---

## InMemoryStore

Current development implementation.

Stores conversations in application memory.

Suitable for development and testing.

---

## Future Memory Backends

The abstraction allows additional storage implementations without modifying the execution pipeline.

Examples include:

* RedisMemoryStore
* PostgreSQLMemoryStore
* VectorMemoryStore
* LangGraph State

---

# Provider Architecture

The provider subsystem isolates all provider-specific behavior from the rest of the application.

```text
AIEngine

        ▼

ExecutionPipeline

        ▼

ProviderStep

        ▼

ProviderFactory

        ▼

Configured Provider

        ▼

LangChain Model

        ▼

LLM
```

No component outside the provider layer should communicate directly with an external AI provider.

---

# ProviderFactory

## Purpose

Create the provider configured for the current application.

Configuration originates from:

```text
.env

↓

LLM_PROVIDER=groq
```

Current provider selection:

```text
ProviderFactory

        ▼

GroqProvider
```

Future selection:

```text
ProviderFactory

        ▼

GroqProvider

OpenAIProvider

GeminiProvider
```

Changing providers should never require modifications to:

* API
* Services
* AIEngine
* Execution Pipeline

Only configuration should change.

---

# Provider Implementations

Every provider implementation follows the same contract.

Current implementation:

* GroqProvider

Future implementations:

* OpenAIProvider
* GeminiProvider
* Local LLM providers
* Enterprise AI providers

Each provider is responsible only for:

* Authentication
* Model initialization
* Streaming implementation
* Provider-specific configuration

Providers should never contain business logic or workflow orchestration.

---

# Object Relationships

The following ownership hierarchy illustrates how the primary AI components interact.

```text
FastAPI

        │

        ▼

API Router

        │

        ▼

ChatService

        │

        ▼

AIEngine

        │

        ▼

ExecutionPipeline

        │

 ┌──────┴─────────┐
 ▼                ▼

MemoryStep   ProviderStep

                    │

                    ▼

             ProviderFactory

                    │

                    ▼

          Configured Provider

                    │

                    ▼

              LangChain Model

                    │

                    ▼

                  LLM
```

Each component owns only the responsibility directly beneath it.

This ownership model keeps dependencies directional, responsibilities isolated, and future extensions straightforward.

---

# Architectural Extension Points

The Core AI Engine has been intentionally designed to grow through extension rather than modification.

Future capabilities should integrate at clearly defined extension points.

Examples include:

* New PipelineSteps
* Additional Providers
* New MemoryStore implementations
* Retrieval subsystem
* Tool execution
* Workflow orchestration
* LangGraph integration
* Multi-Agent coordination

The AIEngine should remain stable while the surrounding execution ecosystem evolves.

This principle is fundamental to the long-term maintainability of the Modular AI Engine.



# 4. Document Processing Architecture

The **Document Processing subsystem** is responsible for transforming uploaded files into standardized internal representations that serve as the foundation for the platform's knowledge pipeline.

Unlike the AI Engine, which focuses on reasoning, the Document subsystem focuses on **ingestion, validation, parsing, metadata extraction, normalization, and document preparation**.

Once a document has been standardized, responsibility is handed to the independent **Chunking subsystem**, which prepares the document for downstream retrieval workflows.

This separation ensures that document parsing, chunk generation, embedding generation, vector storage, and retrieval remain independent architectural concerns that can evolve without affecting one another.

---

# Design Philosophy

Documents are treated as **domain objects**, not merely uploaded files.

Regardless of the original format, every supported document is transformed into the same internal representation.

This provides several advantages:

* Provider independence
* Format independence
* Consistent downstream processing
* Simplified retrieval pipelines
* Easier testing
* Easier support for additional document formats

The AI Engine never needs to understand how a PDF differs from a DOCX file.

It simply receives a standardized `Document` object.

---

# Document Processing Lifecycle

Every uploaded document follows the same processing pipeline.

```text
Client
    │
    ▼
Document API
    │
    ▼
DocumentService
    │
    ▼
DocumentStorage
    │
    ▼
DocumentManager
    │
    ▼
DocumentDetector
    │
    ▼
DocumentParserFactory
    │
    ▼
BaseDocumentParser
    │
    ▼
Concrete Parser
(PDF / DOCX / TXT / Markdown)
    │
    ▼
Document
    │
    ▼
ChunkManager
    │
    ▼
Chunking Strategy
    │
    ▼
Chunk[]
    │
    ▼
ChunkingResult
```

Each stage owns exactly one responsibility before passing standardized output to the next subsystem.

The document pipeline ends with a standardized `Document` domain model.

The Chunking subsystem begins from that point onward, preparing retrieval-ready chunks without introducing any dependency on file formats or parser implementations.

---

# Supported Document Types

The current implementation supports:

| Format   | Status      |
| -------- | ----------- |
| PDF      | ✅ Supported |
| DOCX     | ✅ Supported |
| TXT      | ✅ Supported |
| Markdown | ✅ Supported |

Future planned support includes:

* PPTX
* HTML
* CSV
* Excel
* Images (OCR)
* Rich Text Format (RTF)
* EPUB
* Additional enterprise document formats

Adding support for new formats should not require changes outside the parser subsystem.

---

# DocumentService

## Purpose

DocumentService represents the business layer responsible for document processing.

It coordinates the complete upload workflow while delegating implementation details to specialized components.

---

## Responsibilities

* Receive uploaded files
* Coordinate document processing
* Delegate storage
* Delegate parsing
* Return standardized responses

DocumentService does **not** parse files directly.

Instead, it orchestrates the document processing workflow.

---

# DocumentStorage

## Purpose

Persist uploaded files before processing.

Separating storage from parsing provides several advantages:

* Easier testing
* Future cloud storage support
* Reusable storage layer
* Better separation of concerns

---

## Responsibilities

* Create upload directories
* Generate UUID-based filenames
* Save uploaded bytes
* Return saved file paths
* Manage temporary uploads

Current implementation stores documents on the local filesystem.

Future implementations may support:

* Amazon S3
* Azure Blob Storage
* Google Cloud Storage
* Network storage
* Distributed storage systems

The rest of the application should remain unaware of the storage implementation.

---

# DocumentManager

## Purpose

DocumentManager orchestrates the complete parsing workflow.

Rather than embedding detection and parsing logic into one class, it coordinates specialized components.

---

## Responsibilities

* Coordinate parsing
* Detect document type
* Select parser
* Build Document domain model
* Return standardized output

DocumentManager never performs parsing itself.

It delegates parsing to parser implementations selected by the factory.

---

# DocumentDetector

## Purpose

Determine the actual document type.

Rather than relying solely on filename extensions, detection is performed using MIME type inspection.

Current implementation uses:

* `python-magic`

This approach is significantly more reliable than checking file extensions.

---

## Responsibilities

* Inspect uploaded files
* Determine MIME type
* Identify supported formats
* Reject unsupported documents
* Support parser selection

The detector acts as the first validation stage of the parsing pipeline.

---

# DocumentParserFactory

## Purpose

Select the correct parser implementation.

Instead of scattering format checks throughout the application, parser selection is centralized.

---

## Responsibilities

* Map MIME types
* Instantiate parser implementations
* Return BaseDocumentParser subclasses
* Keep parser registration centralized

The factory follows the **Factory Pattern**, allowing new parser implementations to be introduced without modifying the orchestration logic.

---

# BaseDocumentParser

## Purpose

Provide shared parsing behavior for every document parser.

Every parser follows the same overall workflow while implementing only the format-specific extraction logic.

This follows the **Template Method Pattern**.

---

## Shared Responsibilities

* Read document
* Extract text
* Extract metadata
* Build standardized Document model
* Return parsed output

Each parser overrides only the steps that differ for its file format.

---

# Concrete Parser Implementations

---

## PDFParser

### Responsibilities

* Extract text using **pypdf**
* Read document metadata
* Build Document model

---

## DOCXParser

### Responsibilities

* Extract text using **python-docx**
* Preserve metadata
* Build Document model

---

## TXTParser

### Responsibilities

* Read plain text files
* Generate metadata
* Build Document model

---

## MarkdownParser

### Responsibilities

* Read Markdown documents
* Preserve formatting where appropriate
* Generate metadata
* Build Document model

---

# Document Domain Model

The parser subsystem converts every supported file into a common domain object.

Conceptually:

```text
PDF
DOCX
TXT
Markdown

      │

      ▼

Standardized Document

      │

      ▼

ChunkManager
```

Regardless of the original format, every downstream subsystem operates on the same `Document` representation.

This abstraction completely isolates future AI capabilities from document-specific parsing logic.

The Document object therefore acts as the contract between document ingestion and knowledge preparation.

---

# Document Metadata

Every parsed document produces standardized metadata that remains associated with the document throughout downstream processing.

Current metadata includes:

* Document identifier
* Filename
* MIME type
* File size
* Upload information
* Parser information

This metadata is inherited by the Chunking subsystem, allowing every generated chunk to maintain traceability back to its source document.

Future metadata may additionally include:

* Author
* Creation date
* Modification date
* Language
* Reading time
* Section count
* Token count
* Document statistics

Keeping document metadata standardized ensures that embeddings, retrieval systems, and Retrieval-Augmented Generation (RAG) can operate consistently across all supported document formats.

---

# Validation Pipeline

Before parsing begins, every uploaded document passes through validation.

Current validation includes:

* Empty file detection
* Maximum file size validation
* MIME type validation
* Supported format validation

Future validation may include:

* Malware scanning
* Password-protected document detection
* Duplicate detection
* Content safety checks
* Corruption detection

Validation occurs before parser execution to avoid unnecessary processing.

---

# DocumentMapper

## Purpose

Separate domain models from API models.

The parser subsystem should never return API responses directly.

Instead:

```text
Document Domain Model

        │

        ▼

DocumentMapper

        │

        ▼

API Response
```

This separation keeps serialization concerns outside the business logic.

---

# Object Relationships

The document processing subsystem follows a layered ownership hierarchy.

```text
Document API
      │
      ▼
DocumentService
      │
      ▼
DocumentStorage
      │
      ▼
DocumentManager
      │
      ▼
DocumentDetector
      │
      ▼
DocumentParserFactory
      │
      ▼
BaseDocumentParser
      │
      ▼
Concrete Parser
      │
      ▼
Document
      │
      ▼
ChunkManager
      │
      ▼
Chunking Strategy
      │
      ▼
ChunkingResult
```

Each component owns only the responsibility immediately beneath it.

Document Processing owns document ingestion.

Chunking owns retrieval preparation.

This clear separation keeps both subsystems independently extensible while establishing a stable interface between them.

---

# Design Patterns

The Document subsystem intentionally employs well-known software engineering patterns.

## Factory Pattern

Used by:

* DocumentParserFactory

Purpose:

Create the appropriate parser without exposing parser selection logic to higher layers.

---

## Template Method Pattern

Used by:

* BaseDocumentParser

Purpose:

Define the overall parsing algorithm while allowing subclasses to implement format-specific extraction.

---

## Layered Architecture

Used throughout the subsystem.

Purpose:

Separate storage, detection, parsing, mapping, and API concerns.

---

# Integration with the AI Engine

The Document Processing and Chunking subsystems now provide the complete knowledge preparation pipeline for the platform.

The current architecture is:

```text
Upload
    │
    ▼
Document
    │
    ▼
Chunking
    │
    ▼
ChunkingResult
```

Future milestones will extend this pipeline without modifying its existing stages:

```text
ChunkingResult
      │
      ▼
Embeddings
      │
      ▼
Vector Database
      │
      ▼
Retriever
      │
      ▼
Retrieval Pipeline
      │
      ▼
RAG
      │
      ▼
AI Engine
```

Because each subsystem communicates through standardized domain models, future capabilities can be introduced by extension rather than architectural restructuring.

---

# Architectural Goals

The Document subsystem has been designed around four primary goals:

### 1. Format Independence

The AI Engine should never depend on document formats.

---

### 2. Extensibility

Supporting a new file type should primarily require implementing a new parser and registering it in the parser factory.

---

### 3. Reusability

The subsystem should be reusable by any future feature that requires document ingestion, including:

* Knowledge bases
* Search
* Retrieval
* Summarization
* Report generation
* Multi-agent workflows

---

### 4. Long-Term Stability

The Document Processing and Chunking subsystems together establish the permanent foundation for knowledge ingestion within the Modular AI Engine.

As Embeddings, Vector Databases, Retrieval, and Retrieval-Augmented Generation (RAG) are introduced, these foundational stages should remain largely unchanged.

Future milestones are expected to extend the pipeline rather than modify existing components, preserving stable interfaces and minimizing architectural churn.




# 5. Chunking Architecture

The **Chunking subsystem** serves as the bridge between document ingestion and knowledge retrieval.

Once the Document Processing subsystem has transformed an uploaded file into a standardized `Document` object, responsibility is transferred to the Chunking subsystem.

Rather than operating on uploaded files, chunking works exclusively with domain models, making it completely independent of document formats, parser implementations, and storage mechanisms.

This separation ensures that retrieval preparation evolves independently from document ingestion.

---

# Design Philosophy

Chunking is treated as its own architectural subsystem rather than a utility function inside document parsing.

The guiding principle is simple:

> Documents are parsed once.
>
> Documents may be chunked many different ways.

Keeping these responsibilities separate allows new chunking algorithms to be introduced without affecting document parsing or downstream retrieval.

---

# Responsibilities

The Chunking subsystem is responsible for:

* Transforming Documents into retrieval-ready chunks
* Coordinating configurable chunking strategies
* Preserving document metadata
* Producing standardized Chunk domain models
* Returning a consistent ChunkingResult
* Preparing knowledge for downstream embedding generation

It is **not** responsible for:

* Uploading files
* Detecting MIME types
* Parsing documents
* Generating embeddings
* Communicating with vector databases
* Retrieval
* AI reasoning

Those concerns belong to their own dedicated subsystems.

---

# Chunking Lifecycle

Every standardized Document follows the same chunk generation workflow.

```text
Document
    │
    ▼
ChunkManager
    │
    ▼
Configured Chunking Strategy
    │
    ▼
Chunk Generation
    │
    ▼
Chunk Domain Models
    │
    ▼
ChunkingResult
```

Each stage performs exactly one responsibility.

The ChunkManager coordinates the workflow while the configured strategy performs the actual chunk generation.

---

# Chunking Workflow

Conceptually the subsystem performs the following sequence.

```text
Document

      │

      ▼

Extract Text

      │

      ▼

Apply Chunking Strategy

      │

      ▼

Generate Chunk Objects

      │

      ▼

Attach Metadata

      │

      ▼

Build ChunkingResult
```

Only standardized domain models flow between these stages.

The workflow therefore remains independent of file format, parser implementation, or future embedding providers.

---

# Domain Models

The Chunking subsystem currently consists of three primary domain models.

## Document

Represents a fully parsed document produced by the Document Processing subsystem.

Acts as the input to chunk generation.

---

## Chunk

Represents one retrieval unit.

Each chunk contains:

* Chunk identifier
* Parent document identifier
* Chunk index
* Chunk content
* Character boundaries
* Metadata

Every downstream retrieval component operates on Chunk objects rather than raw document text.

---

## ChunkingResult

Represents the standardized output of the subsystem.

Instead of returning raw collections, every chunking operation returns a ChunkingResult containing:

* Generated chunks
* Processing metadata
* Chunk statistics

This provides a stable contract for future embedding pipelines.

---

# Strategy Pattern

The Chunking subsystem follows the Strategy Pattern.

Rather than coupling the project to one splitting algorithm, ChunkManager delegates chunk generation to interchangeable strategies.

```text
ChunkManager
      │
      ▼
BaseChunkingStrategy
      │
 ┌────┴───────────────┐
 ▼                    ▼
Recursive        Semantic
Strategy         Strategy
```

Supporting a new chunking algorithm requires implementing another strategy instead of modifying orchestration logic.

This minimizes regression risk while keeping the subsystem extensible.

---

# RecursiveChunkingStrategy

The current implementation uses LangChain's RecursiveCharacterTextSplitter.

Responsibilities include:

* Respect configurable chunk sizes
* Respect configurable overlap
* Preserve separator hierarchy
* Split documents into retrieval-sized units
* Produce standardized Chunk objects

The implementation is intentionally document-format independent.

Whether the source originated from a PDF, DOCX, TXT, or Markdown file is irrelevant once a standardized Document has been produced.

---

# Configuration

Chunk generation is entirely configuration driven.

Current configuration includes:

* Chunk size
* Chunk overlap
* Separator hierarchy
* Separator preservation

Future configuration may include:

* Token-aware chunking
* Language-specific rules
* Heading-aware chunking
* Semantic similarity thresholds
* Adaptive chunk sizing

Configuration should evolve without requiring changes to ChunkManager itself.

---

# Future Evolution

The current recursive implementation establishes only the first stage of the retrieval pipeline.

Future milestones are expected to extend the subsystem with:

* Semantic chunking
* Code-aware chunking
* Markdown-aware chunking
* HTML-aware chunking
* Token-based chunking
* AI-assisted chunking

Each implementation should conform to the same strategy interface.

As a result, downstream components such as Embedding Generation and Retrieval remain completely unaware of the specific chunking algorithm used.

---

# Architectural Benefits

Separating chunk generation into its own subsystem provides several long-term advantages.

## Separation of Concerns

Document parsing and chunk generation evolve independently.

---

## Extensibility

New chunking algorithms require new strategies rather than architectural rewrites.

---

## Reusability

Multiple retrieval pipelines can reuse the same standardized Chunk objects.

---

## Testability

Chunking can be validated independently from document parsing and embedding generation.

---

## Maintainability

Every subsystem owns one architectural responsibility.

This keeps the overall platform modular, easier to reason about, and significantly easier to extend as future milestones introduce embeddings, vector databases, retrieval, and Retrieval-Augmented Generation (RAG).

---

# 6. Engineering Principles & Development Philosophy

Software architecture is not defined solely by classes and folders—it is shaped by the engineering principles that guide every design decision.

The Modular AI Engine is built around a small set of architectural rules that prioritize maintainability, extensibility, readability, and long-term stability over rapid feature accumulation.

These principles should guide every future contribution to the project.

---

# Core Engineering Principles

---

## 1. Build an AI Platform, Not an AI Application

The primary objective of this project is **not** to build a chatbot.

Instead, the goal is to build a reusable AI execution platform capable of powering many different applications.

The platform should be equally capable of supporting:

* Chat applications
* Healthcare assistants
* Educational systems
* Enterprise copilots
* Research assistants
* Legal assistants
* Business intelligence platforms
* Future domain-specific AI products

Every architectural decision should move the platform closer to this vision.

---

## 2. Separation of Responsibilities

Every component should have one clearly defined responsibility.

For example:

| Component       | Responsibility              |
| --------------- | --------------------------- |
| API             | HTTP communication          |
| Services        | Business workflows          |
| AI Engine       | AI orchestration            |
| Pipeline Steps  | Individual execution stages |
| Providers       | External AI communication   |
| Memory          | Conversation persistence    |
| Document System | Knowledge ingestion         |

Whenever a component begins taking on multiple unrelated responsibilities, it should be refactored into smaller focused components.

---

## 3. Depend on Abstractions

Higher-level components should never depend directly on concrete implementations.

Instead, they should rely on interfaces and abstractions.

Examples include:

* ProviderFactory
* BaseMemoryStore
* BaseDocumentParser
* PipelineStep

This makes components:

* Easier to replace
* Easier to test
* Easier to extend
* Less tightly coupled

---

## 4. Composition Over Modification

New functionality should primarily be introduced by extending the architecture rather than rewriting existing components.

Examples include:

Instead of modifying the AIEngine:

* Add a new PipelineStep.

Instead of modifying parser logic:

* Create a new parser implementation.

Instead of changing memory behavior:

* Add a new MemoryStore.

This significantly reduces regression risk.

---

## 5. Provider Independence

No application layer outside the provider subsystem should know which AI provider is currently active.

Changing:

```text
LLM_PROVIDER=groq
```

to

```text
LLM_PROVIDER=openai
```

should not require modifications to:

* API
* Services
* AIEngine
* Execution Pipeline
* Memory
* Document subsystem

Only configuration should change.

---

## 6. Incremental Evolution

Large architectural rewrites should be avoided.

Instead, the system evolves through stable milestones.

Each milestone should:

* Solve one architectural problem
* Introduce one major capability
* Preserve existing functionality
* Maintain backwards compatibility where practical

---

## 7. Stable Public Interfaces

Internal implementations may evolve.

Public interfaces should remain stable whenever possible.

Examples include:

* REST endpoints
* API schemas
* Provider interfaces
* Memory interfaces
* Parser interfaces
* Pipeline abstractions

Stable interfaces reduce the impact of architectural changes.

---

## 8. Minimize Technical Debt

Features should never be merged simply because they work.

They should also:

* Follow architectural conventions
* Respect existing abstractions
* Maintain readability
* Remain testable
* Support future extension

Long-term maintainability always takes priority over short-term convenience.

---

# Design Patterns

Several well-established software engineering patterns are intentionally used throughout the project.

---

## Factory Pattern

Used by:

* ProviderFactory
* DocumentParserFactory

Purpose:

Centralize object creation while hiding implementation details.

Benefits:

* Loose coupling
* Easier extension
* Simplified dependency management

---

## Template Method Pattern

Used by:

* BaseDocumentParser

Purpose:

Define a common parsing workflow while allowing subclasses to customize format-specific behavior.

---

## Strategy Pattern

Used by:

* Provider implementations
* Memory implementations
* Document parser implementations
* Chunking strategies

Examples include:

* Provider implementations
* BaseMemoryStore implementations
* BaseDocumentParser implementations
* BaseChunkingStrategy implementations

Each implementation follows a common interface while providing specialized behavior.

This architecture allows new providers, parsers, memory backends, and chunking algorithms to be introduced without modifying orchestration logic.

---

## Pipeline Pattern

Used by:

* ExecutionPipeline

Purpose:

Break complex execution into independent stages.

Benefits include:

* Simplicity
* Testability
* Extensibility
* Reusability

---

## Layered Architecture

The entire project follows a layered architecture.

Each layer communicates only with the layer immediately beneath it.

This minimizes coupling while improving maintainability.

---

# Dependency Rules

Maintaining correct dependency direction is essential.

Dependencies must always flow downward.

```text
Application
      │
      ▼
API
      │
      ▼
Services
      │
      ├─────────────┐
      ▼             ▼
AI Engine     Document Processing
      │             │
      ▼             ▼
Providers     Chunking
      │             │
      ▼             ▼
External AI    Future Retrieval
```

Lower layers must never import higher layers.

Examples:

✅ API → Services

✅ Services → AI Engine

✅ Services → Document Processing

✅ Document Processing → Chunking

✅ AI Engine → Providers

❌ Providers → Services

❌ Chunking → Document Processing

❌ Engine → API

❌ Providers → Engine

Following these rules preserves subsystem independence and prevents circular dependencies.

---

# Coding Guidelines

Future contributions should follow these conventions.

---

## Create Files Intentionally

Files should only be created when they represent a meaningful architectural responsibility or are expected to grow.

Avoid unnecessary abstractions.

A small project with excessive files quickly becomes difficult to navigate.

---

## Prefer Readability

Code should optimize for clarity over cleverness.

Readable code is easier to maintain than highly optimized but difficult-to-understand implementations.

Future contributors should understand the intent of a component without extensive explanation.

---

## Keep Classes Focused

Classes should remain small and focused.

Large classes often indicate multiple responsibilities and should be split into dedicated components.

---

## Avoid Business Logic Leakage

Business logic should never appear inside:

* API routers
* Providers
* Configuration
* Schemas
* Storage components

Business workflows belong in the Service layer or AI Engine orchestration.

---

## Favor Explicitness

Prefer explicit architecture over hidden behavior.

Examples:

Good:

* Dedicated PipelineStep
* Dedicated Provider
* Dedicated MemoryStore

Avoid:

* Hidden side effects
* Global state
* Implicit execution

Explicit architecture is easier to reason about and debug.

---

# Development Workflow

Every milestone follows the same engineering workflow.

```text
Architecture
      │
      ▼
Implementation
      │
      ▼
Testing
      │
      ▼
Documentation
      │
      ▼
Git Commit
```

A milestone is considered complete only when:

* Implementation is stable
* Functionality has been tested
* Documentation has been updated
* Architecture remains consistent
* Existing functionality continues to work
* Public interfaces remain stable

This workflow ensures that documentation evolves alongside the codebase and that architectural quality is maintained throughout development.

---

# Extension Guidelines

The Modular AI Engine has been intentionally designed for continuous architectural evolution.

Future capabilities should integrate through existing extension points rather than modifying established subsystems.

## AI Engine

New reasoning capabilities should be introduced as PipelineSteps.

Examples:

* RoutingStep
* RetrieverStep
* RAGStep
* ToolStep
* PlanningStep
* AgentStep

---

## Providers

Supporting a new AI provider should require:

* Creating a provider implementation
* Registering it in ProviderFactory

---

## Memory

Supporting a new persistence backend should require implementing BaseMemoryStore.

Examples:

* Redis
* PostgreSQL
* Vector Store
* LangGraph State

---

## Document Processing

Supporting a new document format should require:

* Creating a parser
* Registering it in DocumentParserFactory

---

## Chunking

Supporting a new chunking algorithm should require:

* Implementing BaseChunkingStrategy
* Registering the strategy
* Configuring ChunkManager

Examples:

* Semantic chunking
* Token-aware chunking
* Markdown-aware chunking
* HTML-aware chunking
* Code-aware chunking

---

## Retrieval

The retrieval subsystem will consume standardized ChunkingResult objects.

Conceptually:

```text
ChunkingResult
      │
      ▼
Embeddings
      │
      ▼
Vector Database
      │
      ▼
Retriever
      │
      ▼
RAG
```

Each subsystem should evolve independently while communicating through stable domain models.

---

# Long-Term Architectural Evolution

The project has been intentionally designed for gradual, milestone-driven evolution.

The expected progression is:

```text
Chat Backend
      │
      ▼
AI Engine
      │
      ▼
Conversation Memory
      │
      ▼
Streaming
      │
      ▼
Document Processing
      │
      ▼
Chunking              ✅ Completed
      │
      ▼
Embedding Generation  ← Current Next Milestone
      │
      ▼
Vector Database
      │
      ▼
Retriever
      │
      ▼
Retrieval Pipeline
      │
      ▼
Retrieval-Augmented Generation (RAG)
      │
      ▼
LangGraph
      │
      ▼
Tool Calling
      │
      ▼
Multi-Agent Systems
      │
      ▼
Complete AI Reasoning Platform
```

Each stage extends previously established architectural foundations.

Rather than repeatedly restructuring the application, new capabilities should integrate through stable abstractions such as PipelineSteps, Providers, Memory implementations, Document Processing, and Chunking.

---

# Guiding Philosophy

The success of the Modular AI Engine will ultimately be measured not by the number of implemented features, but by how easily new capabilities can be integrated while preserving modularity, stability, and architectural clarity.

Every milestone should strengthen existing abstractions rather than replace them.

The addition of the Document Processing and Chunking subsystems demonstrates this philosophy by extending the platform's capabilities without requiring fundamental changes to the AI Engine or other established components.

This commitment to incremental evolution ensures that the project can grow into a complete AI reasoning platform while remaining maintainable, extensible, and production-ready.
