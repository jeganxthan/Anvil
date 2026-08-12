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

Anvil aims to become the **VS Code of AI** — a single, extensible desktop workspace instead of switching between ChatGPT, Claude, Ollama, NotebookLM, and a dozen other tools.

Anvil isn't built against a fixed feature list. As new open-source AI tools, frameworks, and techniques prove themselves useful, they get folded in behind Anvil's existing interfaces — the app keeps absorbing what's genuinely good in the ecosystem, without turning into an unmaintainable pile of half-finished integrations.

---

## Current Status

Built with **Tauri + React** as the desktop chat application. This is the working foundation everything else builds on.

**Build order, in progress:**

1. ✅ **Tauri + React chat app** — the core desktop shell, chat UI, streaming responses
2. 🔨 **RAG with a document chunk viewer** — users can see exactly which chunks were retrieved and used to ground an answer, not just the final response
3. ⬜ **Crawl4AI** — scrape websites into clean, LLM-ready content that feeds into RAG the same way any other document does
4. ⬜ **CrewAI** — multi-agent workflows on top of the RAG foundation
5. 🔨 **LangChain & LlamaIndex** — currently being wired in as the retrieval/orchestration layer underneath RAG and agents

This order matters: chunk-level transparency in RAG has to work first, since everything after it (scraped content, agents) depends on trusting what's actually being retrieved.

---

## Core Principles

* Open Source, Privacy First, Local First
* Multi-Provider, Extensible, Plugin Based
* Fast, Cross Platform, Developer Friendly
* **Continuously integrated** — any suitable open-source AI project can be added as the ecosystem evolves; Anvil's core (chat, cache, memory) stays stable while what plugs into it grows

---

## Tech Stack (current)

**Desktop app:** Tauri + React + TypeScript
**Backend:** Python (FastAPI)
**RAG:** LangChain, LlamaIndex — being integrated now
**Web ingestion:** Crawl4AI — next up
**Agents:** CrewAI — next up
**Vector storage:** local-first (sqlite-vec / Qdrant, exact choice per deployment)

This list grows as the roadmap above moves forward — see Current Status for what's actually working today versus in progress.

---

## Contributing

We welcome contributors of all experience levels — Rust, Python, React, AI/ML, documentation, testing, UI/UX. See `CONTRIBUTING.md` before opening a pull request.

---

## License

MIT License — see `LICENSE`.

---

## Long-Term Goal

Anvil is not another chatbot. It's meant to become an extensible AI workspace that keeps pace with the open-source AI ecosystem — pulling in whatever proves genuinely useful, cleanly, without losing the simplicity of the core application.