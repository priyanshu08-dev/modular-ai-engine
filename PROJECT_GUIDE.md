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
   │
   ▼
AI Engine
   │
   ▼
Execution Pipeline
   │
   ▼
Provider Layer
   │
   ▼
LLM
```

Each layer owns a single responsibility.

The API layer never performs AI reasoning.

The Service layer never communicates directly with providers.

The AI Engine never knows which provider is currently active.

Providers never contain business logic.

This separation allows every subsystem to evolve independently while maintaining stable interfaces between layers.

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

The document subsystem follows its own independent workflow.

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
Document Domain Model
        │
        ▼
DocumentMapper
        │
        ▼
API Response
```

This layered design isolates storage, detection, parsing, and response mapping into independent components.

Adding support for a new document type should require only:

1. Creating a new parser.
2. Registering it in the parser factory.

No other component should require modification.

---

# Relationship Between Major Subsystems

The project currently consists of several independent but cooperating subsystems.

```text
                   Modular AI Engine
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
      ▼                    ▼                    ▼
 API Layer            AI Engine          Document System
      │                    │                    │
      ▼                    ▼                    ▼
 Service Layer     Execution Pipeline    DocumentManager
      │                    │                    │
      ▼                    ▼                    ▼
 Schemas          Memory / Providers     Storage / Parsers
```

Each subsystem has a clearly defined boundary and communicates through stable interfaces rather than direct implementation dependencies.

This architectural separation enables the platform to continue growing while keeping the codebase understandable, maintainable, and extensible.

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

Most new functionality will integrate by extending existing abstractions—such as adding new pipeline steps, providers, memory implementations, document processors, or retrieval components—rather than rewriting existing code.

This philosophy is the foundation upon which every architectural decision in the Modular AI Engine is built.


# 2. Project Structure

The Modular AI Engine follows a layered, modular architecture where each package is responsible for one well-defined aspect of the system.

The directory structure is intentionally designed to keep business logic independent from infrastructure concerns, allowing each subsystem to evolve without impacting the rest of the application.

Current project structure:

```text
app/
│
├── api/
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
        ▼
AI Engine
        │
        ▼
Providers
        │
        ▼
External AI Services
```

Each layer communicates only with the layer directly beneath it.

This prevents circular dependencies and keeps the architecture maintainable.

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

The **Document Processing subsystem** is responsible for transforming uploaded files into a standardized internal representation that can be consumed by future AI capabilities.

Unlike the AI Engine, which focuses on reasoning, the Document subsystem focuses on **ingestion, validation, parsing, metadata extraction, and normalization**.

It has been intentionally designed as an independent subsystem so that future capabilities such as Chunking, Embeddings, Vector Databases, and Retrieval-Augmented Generation (RAG) can be added without modifying the existing parsing pipeline.

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
DocumentMapper
        │
        ▼
API Response
```

Each component performs exactly one responsibility before handing control to the next stage.

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
```

Regardless of the original format, downstream systems always receive the same representation.

This dramatically simplifies future AI capabilities.

---

# Document Metadata

Every parsed document produces structured metadata.

Current metadata includes:

* Document identifier
* Filename
* MIME type
* File size
* Upload information
* Parser information

Future metadata may include:

* Author
* Creation date
* Modification date
* Language
* Reading time
* Section count
* Token count
* Document statistics

Keeping metadata standardized allows future retrieval systems to operate consistently across all document types.

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

The document subsystem follows a layered ownership hierarchy.

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

DocumentMapper
```

Each component owns only the responsibility immediately beneath it.

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

# Future Integration with the AI Engine

The Document subsystem has been designed to integrate naturally with future AI capabilities.

The planned evolution is:

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

Notice that the existing parsing subsystem remains unchanged.

Each future milestone extends the pipeline by introducing a new processing stage rather than modifying previous ones.

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

As Chunking, Embeddings, Retrieval, and RAG are introduced, the existing document processing pipeline should remain largely unchanged.

This stability ensures that new capabilities build upon a reliable foundation instead of continually restructuring the system.

The Document Processing subsystem therefore serves as the entry point for all knowledge ingestion within the Modular AI Engine and forms the foundation for the platform's future retrieval and reasoning capabilities.




# 5. Engineering Principles & Development Philosophy

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

Used conceptually throughout the provider and parser architecture.

Examples:

* Provider implementations
* Memory implementations
* Parser implementations

Each implementation follows the same interface while providing different behavior.

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

        ▼

Services

        ▼

Engine

        ▼

Providers

        ▼

External Services
```

Lower layers must never import higher layers.

Examples:

✅ API → Services

✅ Services → Engine

✅ Engine → Providers

❌ Providers → Services

❌ Engine → API

❌ Memory → Services

Following these rules prevents circular dependencies and keeps the architecture modular.

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

        ▼

Testing

        ▼

Git Commit

        ▼

Documentation Update
```

A milestone is considered complete only when:

* Implementation is stable
* Functionality has been tested
* Documentation has been updated
* Architecture remains consistent
* Existing functionality continues to work

This workflow ensures that documentation evolves alongside the codebase rather than becoming outdated.

---

# Extension Guidelines

The Modular AI Engine is expected to grow significantly.

Future capabilities should integrate through existing architectural extension points.

Examples include:

## AI Engine

New capabilities should be introduced as PipelineSteps.

Examples:

* RoutingStep
* RetrieverStep
* RAGStep
* ToolStep
* PlanningStep
* AgentStep

---

## Providers

Supporting a new provider should require:

* Creating a new provider implementation.
* Registering it in ProviderFactory.

No other subsystem should require modification.

---

## Memory

Supporting a new storage backend should require implementing BaseMemoryStore.

Examples:

* Redis
* PostgreSQL
* Vector Store
* LangGraph State

---

## Document Processing

Supporting a new file format should require:

* Creating a parser.
* Registering it in DocumentParserFactory.

The remainder of the document pipeline should remain unchanged.

---

## Retrieval

The retrieval subsystem should integrate between Memory and Provider execution.

Conceptually:

```text
ExecutionPipeline

        ▼

MemoryStep

        ▼

RetrieverStep

        ▼

RAGStep

        ▼

ProviderStep
```

The existing execution pipeline should require minimal modification.

---

# Long-Term Architectural Evolution

The project has been intentionally designed for gradual evolution.

The expected architectural progression is:

```text
Chat Backend

        ▼

AI Engine

        ▼

Conversation Memory

        ▼

Streaming

        ▼

Document Processing

        ▼

Chunking

        ▼

Embeddings

        ▼

Vector Database

        ▼

Retrieval

        ▼

RAG

        ▼

LangGraph

        ▼

Tool Calling

        ▼

Multi-Agent Systems

        ▼

Complete AI Reasoning Platform
```

Each stage builds upon previously established architectural foundations.

Rather than repeatedly restructuring the application, future milestones should extend existing abstractions.

---

# Guiding Philosophy

The ultimate objective of the Modular AI Engine is **not** to maximize the number of implemented features.

Instead, the objective is to build an architecture that remains understandable, maintainable, extensible, and production-ready as the system grows.

Every architectural decision should answer the following questions:

* Does this improve modularity?
* Does this reduce coupling?
* Does this make future development easier?
* Does this preserve clean architectural boundaries?
* Does this encourage reuse rather than duplication?

If the answer to these questions is consistently **yes**, the architecture is moving in the right direction.

The success of the project will ultimately be measured not by the number of features it contains, but by how easily new capabilities can be integrated while preserving the clarity, stability, and elegance of the existing system.
