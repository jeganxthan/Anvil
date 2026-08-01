# Anvil

> **The Open-Source AI Workspace**
>
> One desktop application for every AI model, every workflow, and every developer.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Rust](https://img.shields.io/badge/Rust-1.90+-orange)
![Python](https://img.shields.io/badge/Python-3.12+-blue)
![React](https://img.shields.io/badge/React-19-61DAFB)
![Tauri](https://img.shields.io/badge/Tauri-v2-purple)

---

## Vision

Anvil aims to become the **VS Code of AI**.

Instead of forcing users to switch between ChatGPT, Claude, Gemini, Ollama, LM Studio, Open WebUI, NotebookLM, and dozens of AI tools, Anvil provides a single, extensible desktop platform where every model, every workflow, and every AI technique works together.

Our goal is to build an AI workspace that developers, researchers, students, and enterprises can customize and extend — fast by default, and correct by design.

---

## Why Anvil?

Modern AI applications are fragmented.

* ChatGPT for writing
* Claude for long context
* Gemini for multimodal tasks
* Ollama for local models
* Open WebUI for self-hosting
* LM Studio for local inference
* NotebookLM for research
* Pinecone for vectors
* LangChain for orchestration
* CrewAI for agents

Anvil brings everything together — and treats every framework as an interchangeable adapter, not a foundation you're locked into.

---

## Core Principles

* Open Source
* Privacy First
* Local First
* Multi-Provider
* Extensible
* Fast
* Cross Platform
* Developer Friendly
* Plugin Based
* **Framework-agnostic core** — your own retrieval, caching, and provider logic is the product; LangChain/LlamaIndex/CrewAI plug in only where their specific strength is needed

---

## Architecture

```text
                     React + TypeScript (UI)

                              │
                     Tauri IPC (async, streaming)
                              │

                  Rust Core Engine (Tauri)
   ┌──────────┬──────────┬──────────┬──────────┬────────┐
   │  Cache   │  Plugin  │   File   │Background│  Auth  │
   │ (moka)   │ Runtime  │ Indexer  │ Workers  │        │
   │ LRU+TTL  │  (WASM)  │(Tantivy) │(heap PQ) │        │
   ├──────────┼──────────┼──────────┼──────────┴────────┤
   │ Database │   IPC    │   MCP    │
   │ (SQLite) │  Bridge  │  Server  │
   └──────────┴──────────┴──────────┘

                              │
                  Local process IPC / HTTP
                              │

                Python AI Engine (FastAPI, async)
   ┌────────────────────────────────────────────────────┐
   │  Provider Layer                                      │
   │  circuit breaker + token bucket + fallback chain     │
   │  OpenAI · Anthropic · Gemini · NVIDIA · Ollama ·      │
   │  Groq · OpenRouter · TogetherAI · DeepSeek ·          │
   │  Mistral · Azure OpenAI · AWS Bedrock                 │
   ├──────────────┬──────────────┬─────────────────────┤
   │  RAG / CAG    │ Agent / MCP  │  Memory (tiered:     │
   │  Core         │ Orchestrator │  ring buffer →        │
   │ (hand-written) │ (LangGraph)  │  summary → semantic → │
   │                │              │  long-term / MAG)     │
   ├──────────────┼──────────────┼─────────────────────┤
   │  LangChain    │  LlamaIndex  │  Observability        │
   │  adapter      │  adapter     │  (OTel + Langfuse/     │
   │  (optional)   │  (optional)  │   Phoenix)             │
   └────────────────────────────────────────────────────┘

                              │

        Vector DB (Qdrant / FAISS / Chroma) + Postgres/SQLite
```

---

## Features

### AI Providers

* NVIDIA NIM
* OpenAI
* Gemini
* Claude
* Ollama
* Groq
* OpenRouter
* TogetherAI
* DeepSeek
* Mistral
* Azure OpenAI
* AWS Bedrock

Every provider sits behind an identical interface — same routes, same request/response contract — wrapped in a shared cache check, circuit breaker, rate limiter, and fallback chain, so switching providers never means switching reliability.

### Local Models

* Ollama
* llama.cpp
* LM Studio
* vLLM
* SGLang

### Knowledge & Context Strategies

* **RAG (Retrieval-Augmented Generation)** — for large, dynamic knowledge bases: hybrid search (dense + sparse), Reciprocal Rank Fusion, reranking, context compression, citation-grounded answers
* **CAG (Cache-Augmented Generation)** — for small, static knowledge sets (docs, style guides, plugin references): preloads knowledge directly into the context window and caches inference state, skipping retrieval entirely for lower latency and simpler infra
* **MAG (Memory-Augmented Generation)** — tiered, persistent memory across sessions: working memory (ring buffer), summary memory, semantic memory, and long-term/workspace memory, so Anvil remembers preferences and context beyond a single chat

The RAG/CAG/MAG router picks the right strategy automatically based on corpus size, volatility, and whether cross-session memory is involved — you don't have to choose manually.

### RAG Document Support

* PDF Chat
* Word Documents
* Excel
* CSV
* Markdown
* HTML
* Websites
* GitHub Repositories
* YouTube Transcripts
* Notion
* Confluence
* Obsidian Vaults

### Embeddings

* BGE
* Nomic
* E5
* Jina
* OpenAI
* Voyage
* NVIDIA

All embeddings pass through a shared Rust-side LRU cache (`moka`, TTL + size-bound) before hitting a provider — regardless of which framework or code path triggered the call.

### Vector Databases

* Pinecone
* Qdrant
* Chroma
* FAISS
* LanceDB
* Milvus
* Weaviate

### AI Techniques

* Hybrid Search / Semantic Search
* Metadata Filtering
* Multi Query & Self Query Retrieval
* Context Compression
* Re-ranking
* Cache-Augmented Generation (CAG)
* Memory-Augmented Generation (MAG)
* Long-Term & Conversation Memory
* Prompt Templates & Versioning
* Function / Tool Calling
* Structured Output (Pydantic-validated)
* Streaming Responses

### AI Frameworks

Used as optional adapters on top of Anvil's own core — never the default path:

* LangChain (LCEL, chains, tools, memory)
* LlamaIndex (document ingestion, query engines)
* LangGraph (default agent orchestration — DAG + topological execution)
* CrewAI / AutoGen (alternate role-based or conversational agent styles)
* PydanticAI (default typed, validated agent outputs)
* OpenAI Agents SDK / Google ADK / Semantic Kernel
* SmolAgents (code-execution agents — used for the Coding Agent)
* Haystack, DSPy (opt-in, lower priority)

### Model Context Protocol (MCP)

* MCP Client — tool discovery, resource discovery, prompt discovery, standardized transport
* MCP Server (Rust, planned) — exposes Anvil's own file system, local search, and plugins as MCP tools/resources so other AI clients can use Anvil as a tool provider

### Agents

* Research Agent
* Coding Agent (SmolAgents-backed code execution)
* Documentation Agent
* File Agent
* Browser Agent
* Database Agent
* GitHub Agent
* Terminal Agent
* Planner Agent
* Multi-Agent Workflows

### Reliability & Performance

* Circuit breaker per provider (closed / open / half-open)
* Token-bucket rate limiting per provider/key
* Automatic provider fallback chains
* Cost tracking & usage analytics
* Multi-tier caching (Rust in-memory → relational DB → vector DB)
* Ring-buffer-bounded chat memory (no unbounded growth on long conversations)
* Parallel tool-call execution within agent DAGs

### Workspace

* Projects
* Chat History
* Prompt Library
* Model Profiles
* Workspaces
* Collections
* Tags
* Search
* Export

### Developer Tools

* REST API
* Plugin SDK (Rust SDK, Python SDK)
* Extension Marketplace
* CLI
* MCP Support

---

## Technology Stack

**Frontend:** React, TypeScript, Tailwind CSS, Tauri
**Core:** Rust (Tokio async runtime)
**AI Engine:** Python (FastAPI, async)
**AI Frameworks:** LangChain, LlamaIndex, LangGraph, CrewAI, AutoGen, PydanticAI, SmolAgents, DSPy
**Databases:** SQLite, PostgreSQL, Redis
**Vector Databases:** Pinecone, Qdrant, FAISS, Chroma, LanceDB
**Caching:** `moka` (Rust, async-safe LRU + TTL)
**Observability:** OpenTelemetry, Langfuse / Phoenix, Ragas, DeepEval, Promptfoo

---

## Project Structure

```text
anvil/

apps/
    desktop/
    cli/

frontend/

src-tauri/
    commands/
    providers/
    config/
    settings/
    plugins/
    cache/
    database/
    ipc/
    mcp_server/
    updater/

python/
    api/
    providers/          # circuit breaker, rate limiter, fallback chain per provider
    rag/
        core/            # hand-written retrieval, chunking, fusion, reranking
        langchain_adapter/
        llamaindex_adapter/
    cag/                 # cache-augmented generation for static knowledge
    embeddings/
    agents/
    mcp_client/
    memory/              # tiered memory (MAG pattern)
    workflows/
    loaders/
    evaluation/
    tools/

docs/

plugins/

examples/

tests/

website/
```

---

## Roadmap

### v0.1
* NVIDIA Provider
* OpenAI Compatible Client
* Basic Chat
* Streaming
* Chat History
* Settings

### v0.2
* OpenAI
* Gemini
* Claude
* Ollama
* Circuit breaker, rate limiting, fallback chain

### v0.3
* RAG
* CAG (static knowledge fast path)
* Embeddings
* PDF Chat
* Pinecone
* FAISS
* Shared embeddings cache

### v0.4
* LangChain adapter
* LlamaIndex adapter
* Tiered memory (MAG pattern)
* Prompt Templates

### v0.5
* Agents (LangGraph default orchestration)
* CrewAI / AutoGen (optional styles)
* PydanticAI typed outputs
* SmolAgents (Coding Agent)
* MCP Client

### v1.0
* Plugin Marketplace
* MCP Server (Rust)
* Multi-Agent Workspace
* Enterprise Authentication
* Cloud Sync
* Team Collaboration
* Workflow Builder
* Observability & Evaluation pipeline (OTel, Langfuse/Phoenix, Ragas)

---

## Contributing

We welcome developers of all experience levels.

Areas where you can contribute:

* Rust
* Python
* React
* AI
* Documentation
* Testing
* UI/UX
* Plugin Development
* Examples
* Tutorials

Please read `CONTRIBUTING.md` before submitting a pull request.

---

## License

MIT License — see `LICENSE`.

---

## Long-Term Goal

Anvil is not intended to be another chatbot.

It is intended to become an extensible AI operating environment where developers can build, run, compare, evaluate, and automate AI workflows using any model, any provider, any retrieval or memory strategy — from one unified desktop application.