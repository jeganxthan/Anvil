# Contributing to Anvil

First off, thank you for considering contributing to Anvil. This project only exists because of contributors like you, and we welcome developers of all experience levels — whether you're fixing a typo in the docs or building out a new agent framework integration.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Branching & Commit Guidelines](#branching--commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Plugin Development](#plugin-development)
- [Documentation](#documentation)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Community](#community)

---

## Code of Conduct

This project follows a standard Code of Conduct. By participating, you agree to:

- Be respectful and considerate in all interactions
- Welcome newcomers and differing viewpoints
- Give and accept constructive feedback gracefully
- Focus on what is best for the community and the project

Unacceptable behavior can be reported to the maintainers via GitHub Issues or the project's designated contact channel.

---

## Ways to Contribute

You don't need to write code to contribute. Areas where we need help include:

| Area | Examples |
|---|---|
| **Rust** | Core engine, Tauri commands, IPC, plugin runtime, performance |
| **Python** | Providers, RAG pipelines, agents, embeddings, evaluation |
| **React / TypeScript** | UI components, workspace views, settings screens |
| **AI / ML** | New provider integrations, retrieval techniques, agent workflows |
| **Documentation** | Guides, API reference, architecture docs, tutorials |
| **Testing** | Unit tests, integration tests, manual QA |
| **UI/UX** | Design feedback, accessibility, Figma mockups |
| **Plugins** | Building and publishing plugins to the marketplace |
| **Examples** | Sample workflows, starter templates |
| **Triage** | Reproducing bugs, labeling issues, answering questions |

If you're not sure where to start, look for issues labeled `good first issue` or `help wanted`.

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
    updater/

python/
    api/
    providers/
    rag/
    embeddings/
    agents/
    workflows/
    loaders/
    memory/
    evaluation/
    tools/

docs/

plugins/

examples/

tests/

website/
```

A quick orientation:

- **`frontend/`** — React + TypeScript UI, rendered inside the Tauri shell
- **`src-tauri/`** — Rust core engine: filesystem, database, plugin runtime, IPC bridge, caching, auth
- **`python/`** — AI engine: providers, RAG, embeddings, agents, workflows, evaluation
- **`plugins/`** — First-party and example plugins
- **`docs/`** — User and developer documentation
- **`examples/`** — Sample projects and workflows
- **`tests/`** — Cross-cutting integration tests

---

## Getting Started

1. **Fork** the repository and clone your fork:
   ```bash
   git clone https://github.com/<your-username>/anvil.git
   cd anvil
   ```
2. **Add the upstream remote:**
   ```bash
   git remote add upstream https://github.com/anvil-ai/anvil.git
   ```
3. Follow the [Development Setup](#development-setup) below to get everything running locally.
4. Pick an issue, comment on it to let others know you're working on it, and create a branch.

---

## Development Setup

### Prerequisites

- **Rust** 1.90+ (`rustup` recommended)
- **Node.js** 20+ and **pnpm**
- **Python** 3.12+
- **Tauri CLI v2** (`cargo install tauri-cli`)

### Install dependencies

```bash
# Frontend
cd frontend
pnpm install

# Python AI engine
cd ../python
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Rust core
cd ../src-tauri
cargo build
```

### Run in development mode

```bash
# From project root
pnpm tauri dev
```

This starts the Tauri shell, the React dev server, and the Python AI engine together with hot-reload enabled.

### Environment variables

Copy `.env.example` to `.env` in the project root and fill in API keys for the providers you want to test against (OpenAI, Anthropic, Gemini, etc.). Never commit your `.env` file.

---

## Branching & Commit Guidelines

- Branch off `main` using a descriptive name:
  - `feat/qdrant-hybrid-search`
  - `fix/streaming-response-cutoff`
  - `docs/plugin-sdk-guide`
- Use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages:
  ```
  feat(rag): add hybrid search support for Qdrant
  fix(core): resolve race condition in plugin cache
  docs(readme): update roadmap for v0.3
  ```
- Keep commits focused. Prefer several small, reviewable commits over one large commit.

---

## Pull Request Process

1. Ensure your branch is up to date with `upstream/main` before opening a PR.
2. Fill out the PR template completely, including:
   - What the change does and why
   - Related issue number(s)
   - Screenshots/GIFs for UI changes
   - Any breaking changes
3. Make sure all tests pass and linting is clean (see [Testing](#testing)).
4. Request review from a maintainer. Address feedback with additional commits rather than force-pushing over review history until the PR is approved.
5. A maintainer will merge once the PR has the required approvals and passing CI.

PRs that only reformat code, rename variables, or otherwise churn large diffs without functional change should be discussed in an issue first.

---

## Coding Standards

### Rust
- Format with `cargo fmt`
- Lint with `cargo clippy -- -D warnings`
- Prefer explicit error types (`thiserror`/`anyhow`) over `unwrap()` in non-test code

### Python
- Format with `black`, lint with `ruff`
- Type hints required for public functions
- Follow existing patterns in `python/providers/` when adding a new provider

### React / TypeScript
- Format with `prettier`, lint with `eslint`
- Functional components with hooks; avoid class components
- Co-locate component styles using Tailwind utility classes
- Keep components small and composable

### General
- No secrets, API keys, or credentials in code or commits
- Public functions and modules should have docstrings/comments explaining intent, not just mechanics

---

## Testing

- **Rust:** `cargo test`
- **Python:** `pytest` from the `python/` directory
- **Frontend:** `pnpm test`
- **Integration:** tests under `tests/` exercise cross-language flows (e.g., a chat request through Rust → Python → provider → back)

New features should include tests. Bug fixes should include a regression test where practical.

---

## Plugin Development

Anvil is plugin-based by design. If you're building a plugin:

1. Start from the template in `examples/plugin-template/`
2. Use the Rust SDK or Python SDK depending on what your plugin needs to touch
3. Document your plugin's configuration and permissions clearly
4. Submit to the Extension Marketplace via a PR to `plugins/` once it's stable

See `docs/plugin-sdk.md` for the full API reference.

---

## Documentation

Docs live in `docs/` and are just as valuable as code contributions. When adding a feature, please also:

- Update relevant pages in `docs/`
- Add or update examples in `examples/` if applicable
- Keep the root `README.md` roadmap section accurate if your change completes a roadmap item

---

## Reporting Bugs

Before opening a new issue, search existing issues to avoid duplicates. A good bug report includes:

- Anvil version and OS/platform
- Steps to reproduce
- Expected vs. actual behavior
- Logs or screenshots if relevant
- Which provider(s)/model(s) were involved, if applicable

## Suggesting Features

Feature requests are welcome. Please describe:

- The problem you're trying to solve (not just the solution)
- Any alternatives you've considered
- Whether you'd be interested in implementing it yourself

---

## Community

- **Issues & Discussions:** GitHub Issues and Discussions tabs
- **Roadmap:** see the root `README.md` for current milestones (v0.1 → v1.0)

Thank you again for contributing to Anvil — let's build the open, extensible AI workspace this ecosystem needs.
