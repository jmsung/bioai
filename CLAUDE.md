# BioAI — Multi-Agent Healthcare Intelligence System

## Overview

A multi-agent AI system that integrates diverse biomedical knowledge domains to support **personalized health guidance** and **early intervention**. Given a patient's biological data and health profile, specialized agents collaborate to detect early risk signals, recommend preventive strategies, and provide evidence-grounded reasoning.

## Architecture

### Specialized Agents

| Agent | Domain | Responsibility |
|-------|--------|----------------|
| Genomics | Variant interpretation | Analyze genetic variants for disease risk |
| Transcriptomics | Gene expression | Interpret expression patterns and signals |
| Proteomics | Biomarker inference | Identify protein biomarkers and pathways |
| Pharmacology | Drug interactions | Reason about medications, interactions, contraindications |
| Clinical Guidelines | Medical guidelines | Interpret and apply clinical practice guidelines |
| Literature Review | Publications | Search and synthesize recent medical literature |

### System Flow

1. Patient data ingestion (biological data + health profile)
2. Agents independently analyze their domain
3. Orchestrator aggregates findings
4. Generate integrated health assessment with citations

## Project Structure

```
bioai/
├── src/bioai/          # Shared package (importable modules)
│   ├── agents/         # Agent implementations (one per domain)
│   ├── orchestrator/   # Multi-agent coordination
│   ├── models/         # Data models and schemas
│   └── utils/          # Shared utilities
├── scripts/            # Entry points and CLI tools
├── tests/              # Tests (mirror src/ structure)
├── docs/               # Documentation
└── CLAUDE.md           # This file
```

## Development Rules

- **Python 3.11+** as primary language.
- Use `uv` for dependency management.
- Reusable logic goes in `src/bioai/`. Scripts only orchestrate.
- Never duplicate functions across files — extract to the shared package.
- Type hints on all function signatures.
- Docstrings on public functions and classes.

## Coding Standards

- Clean, readable code. Simplicity over cleverness.
- Minimal diffs — every changed line should trace to a task.
- Follow existing patterns. Keep changes localized.
- If 200 lines could be 50, rewrite it.

## Agent Implementation

- Each agent is a self-contained module in `src/bioai/agents/`.
- Agents expose a consistent interface (input schema → output schema).
- Use Claude API (`anthropic` SDK) for LLM calls.
- Keep prompts in separate files or constants, not inline.
- Each agent should declare its tools/capabilities explicitly.

## Version Control

- Conventional commits: `type(scope): description`
  - Types: `feat`, `fix`, `test`, `refactor`, `docs`, `chore`
- Branch naming: `type/description` (kebab-case)
- Never force push to main.

## Commands

```bash
uv sync                  # Install dependencies
uv run pytest            # Run tests
uv run python scripts/   # Run scripts
```
