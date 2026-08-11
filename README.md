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

Anvil is designed to keep absorbing new AI technology as it matures — new providers, new retrieval strategies, new agent frameworks — without ever requiring a rewrite of its core.

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
* **Framework-agnostic core** — your own caching, memory, and orchestration logic is the product; LangChain, LlamaIndex, LiteLLM, and every other framework plug in as adapters, never as the foundation
* **Always current** — the architecture is built so new frameworks, providers, and techniques can be added as they emerge, not just the ones listed today

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
   │  LiteLLM Gateway                                      │
   │  single unified endpoint for every provider,          │
   │  routing, fallback, spend/usage tracking, caching     │
   │  OpenAI · Anthropic · Gemini · NVIDIA · Ollama ·      │
   │  Groq · OpenRouter · TogetherAI · DeepSeek ·          │
   │  Mistral · Azure OpenAI · AWS Bedrock · 100+ more      │
   ├────────────────────────────────────────────────────┤
   │  RAG Framework Selector (user-facing, per session)    │
   │  ┌───────────────┐        ┌────────────────────┐    │
   │  │  LlamaIndex    │        │   LangChain          │    │
   │  │  document Q&A, │        │   agentic workflows, │    │
   │  │  hierarchical  │        │   memory, tool-using │    │
   │  │  indexing      │        │   reasoning chains    │    │
   │  └───────────────┘        └────────────────────┘    │
   ├────────────────────────────────────────────────────┤
   │  Ingestion — Crawl4AI                                  │
   │  scrapes websites into clean, LLM-ready Markdown/       │
   │  structured data, feeds directly into either RAG path  │
   ├──────────────┬──────────────┬─────────────────────┤
   │  CAG          │  MAG          │  Agents / MCP        │
   │ (static docs, │  (tiered      │  (LangGraph DAG,      │
   │  prompt/      │  memory:      │  MCP client/server,   │
   │  provider      │  working →    │  parallel tool calls) │
   │  caching)      │  summary →    │                       │
   │                │  semantic →   │                       │
   │                │  long-term)   │                       │
   ├──────────────┴──────────────┴─────────────────────┤
   │  Observability & Prompt Registry                      │
   │  OpenTelemetry + Langfuse/Phoenix (traces, eval)       │
   │  Langfuse prompt management (versioned, no-redeploy)   │
   └────────────────────────────────────────────────────┘

                              │

        Vector DB (SQLite)
```

---

## Features

### AI Providers — via LiteLLM Gateway

Anvil no longer hand-writes a separate router per provider. Every provider — OpenAI, Anthropic, Gemini, NVIDIA, Ollama, Groq, OpenRouter, TogetherAI, DeepSeek, Mistral, Azure OpenAI, AWS Bedrock, and 100+ others LiteLLM supports — is reached through **one unified gateway endpoint**. Switching providers is a configuration change, not a new file. LiteLLM handles routing, fallback, and spend tracking; Anvil's own layer adds the shared embeddings/response cache on top.

### Local Models

* Ollama
* llama.cpp
* LM Studio
* vLLM (supports prefix caching — the backbone of Anvil's local CAG path)
* SGLang

### RAG Framework — user-selectable per session

From the frontend, the user picks the RAG engine that fits what they're doing:

* **LlamaIndex** *(default)* — best for deep document Q&A: strongest PDF/table parsing, hierarchical and multi-document indexing, purpose-built query engines with citation support. Pick this for "chat with my docs/codebase."
* **LangChain** — best for agentic workflows: LCEL chains, richer memory primitives, and native LangGraph integration for multi-step, tool-using reasoning. Pick this when building an agent that needs to retrieve, reason, and act across multiple tools.

Both sit on top of the same vector store and embeddings cache — switching frameworks never means re-ingesting or re-embedding data.

### Web Ingestion — Crawl4AI

Websites are scraped with **Crawl4AI**, which converts pages into clean, LLM-ready Markdown/structured output (stripping nav/ads/boilerplate) before chunking. Scraped content feeds into the same ingestion pipeline as any other document source, and is retrievable through either RAG framework the user selects.

### Knowledge & Context Strategies

* **RAG** — for large or changing knowledge bases (documents, scraped sites, codebases): hybrid search (dense + sparse), Reciprocal Rank Fusion, reranking, context compression, citation-grounded answers
* **CAG (Cache-Augmented Generation)** — for small, static knowledge (plugin docs, style guides): preloaded into context, using provider prompt caching or vLLM prefix caching — no dedicated library, a pattern built on infrastructure Anvil already has
* **MAG (Memory-Augmented Generation)** — tiered, persistent memory across sessions (working → summary → semantic → long-term), so Anvil remembers user preferences and project context between sessions

The router picks the right strategy automatically based on corpus size, volatility, and whether cross-session memory is involved.

### Document Support (feeds RAG via LlamaIndex or LangChain)

* PDF, Word, Excel, CSV, Markdown, HTML
* Websites (via Crawl4AI)
* GitHub Repositories
* YouTube Transcripts
* Notion, Confluence, Obsidian Vaults

### Embeddings

BGE · Nomic · E5 · Jina · OpenAI · Voyage · NVIDIA — all routed through the same shared Rust-side LRU cache (`moka`, TTL + size-bound) before any provider call, regardless of which RAG framework triggered it.

### Vector Databases

* **sqlite-vec** *(local-first default)* — embedded, zero-deploy, fits Anvil's "Local First" principle exactly
* **Qdrant** — self-hosted / power-user tier for large personal corpora
* Pinecone, Chroma, FAISS, LanceDB, Milvus, Weaviate — supported for users who want them

### AI Techniques

* Hybrid Search, Metadata Filtering, Multi/Self Query Retrieval
* Context Compression, Re-ranking, Citation RAG
* Cache-Augmented Generation (CAG)
* Memory-Augmented Generation (MAG)
* Prompt Templates via LangChain/LlamaIndex primitives — never hand-rolled
* Prompt versioning via Langfuse prompt registry — editable without redeploying
* Structured Output (Pydantic-validated)
* Streaming Responses

### AI Frameworks

* **LiteLLM** — unified provider gateway (replaces per-provider routers)
* **LlamaIndex** / **LangChain** — user-selectable RAG engines (see comparison above)
* **LangGraph** — default agent orchestration (DAG + topological execution)
* **PydanticAI** — default typed, validated agent outputs
* **SmolAgents** — code-execution agent, powers the Coding Agent
* CrewAI, AutoGen, OpenAI Agents SDK, Google ADK, Semantic Kernel — optional alternate agent styles
* **Crawl4AI** — website-to-Markdown scraping for RAG ingestion

### Model Context Protocol (MCP)

* MCP Client — tool/resource/prompt discovery, standardized transport
* MCP Server (Rust, planned) — exposes Anvil's own file system, local search, and plugins as MCP tools for other AI clients

### Agents

Research Agent · Coding Agent (SmolAgents) · Documentation Agent · File Agent · Browser Agent · Database Agent · GitHub Agent · Terminal Agent · Planner Agent · Multi-Agent Workflows

### Reliability & Performance

* LiteLLM-level routing + fallback across providers
* Circuit breaker and rate limiting on Anvil's own call layer
* Multi-tier caching (Rust in-memory → relational DB → vector DB)
* Ring-buffer-bounded chat memory
* Parallel tool-call execution within agent DAGs
* Cost tracking & usage analytics

### Workspace

Projects · Chat History · Prompt Library · Model Profiles · Workspaces · Collections · Tags · Search · Export

### Developer Tools

REST API · Plugin SDK (Rust + Python) · Extension Marketplace · CLI · MCP Support

---

## Technology Stack

**Frontend:** React, TypeScript, Tailwind CSS, Tauri
**Core:** Rust (Tokio async runtime)
**AI Engine:** Python (FastAPI, async)
**Provider Gateway:** LiteLLM
**RAG Frameworks:** LlamaIndex, LangChain (user-selectable)
**Agent Orchestration:** LangGraph, PydanticAI, SmolAgents
**Web Ingestion:** Crawl4AI
**Databases:** SQLite, PostgreSQL, Redis
**Vector Databases:** sqlite-vec (local default), Qdrant, Pinecone, FAISS, Chroma, LanceDB
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
    cache/
    plugins/
    database/
    ipc/
    mcp_server/
    config/
    settings/
    updater/

python/
    api/
        gateway.py         # LiteLLM-backed unified chat/embeddings endpoint
    rag/
        selector.py         # user-facing framework choice: llamaindex | langchain
        llamaindex_adapter/
        langchain_adapter/
    ingestion/
        crawl4ai/            # website scraping → clean Markdown → chunking
        loaders/              # pdf, docx, xlsx, notion, confluence, obsidian
    cag/
    memory/                  # tiered memory (MAG pattern)
    agents/
    mcp_client/
    embeddings/
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
* LiteLLM gateway wired in (replaces per-provider routers)
* Basic Chat, Streaming, Chat History, Settings

### v0.2
* Circuit breaker + shared cache on top of LiteLLM
* sqlite-vec local vector store

### v0.3
* RAG framework selector (LlamaIndex + LangChain adapters)
* Crawl4AI web ingestion
* CAG fast path for static knowledge
* Shared embeddings cache

### v0.4
* Tiered memory (MAG pattern)
* Langfuse prompt registry (no hardcoded prompts)

### v0.5
* LangGraph agent orchestration
* PydanticAI typed outputs, SmolAgents coding agent
* MCP Client

### v1.0
* Plugin Marketplace, MCP Server (Rust)
* Multi-Agent Workspace, Team Collaboration, Cloud Sync
* Full observability & evaluation pipeline

### Ongoing
* New providers, RAG/agent frameworks, and ingestion sources get added as adapters behind existing interfaces — the core (cache, memory, orchestration) doesn't change when the ecosystem does

---

## Contributing

We welcome developers of all experience levels — Rust, Python, React, AI, documentation, testing, UI/UX, plugin development. Please read `CONTRIBUTING.md` before submitting a pull request.

---

## License

MIT License — see `LICENSE`.

---

## Long-Term Goal

Anvil is not intended to be another chatbot.

It is an extensible AI operating environment where developers can build, run, compare, evaluate, and automate AI workflows using any model, any provider, any retrieval or memory strategy — and pull in whatever the AI ecosystem builds next, without rewriting the core.