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

## Parallel Worktree Workflow (Hackathon)

Two developers work simultaneously using git worktrees. Each task gets its own branch and worktree.

### Setup
```bash
git worktree add .claude/worktrees/<task-name> feat/<task-name>
```

### Merge Loop
1. **Work** on your feature branch in your worktree
2. **Coordinate verbally** — say "I'm merging" before merging
3. **Rebase and merge** (one person at a time):
   ```bash
   # In your worktree
   git fetch origin
   git rebase origin/main
   # Then from main worktree
   git merge --ff-only feat/<task-name>
   git push origin main
   ```
4. **Other person rebases** their branch immediately:
   ```bash
   git fetch origin && git rebase origin/main
   ```
5. **Continue working**

### Rules
- One merge at a time — coordinate verbally
- Rebase before every merge to keep linear history
- Merge frequently (every 30-60 min) to minimize divergence
- Keep shared files (`models.py`, `config.py`, `__init__.py`) small and coordinate changes verbally
- If conflicts arise, the person merging resolves them on the spot

## Commands

```bash
uv sync                  # Install dependencies
uv run pytest            # Run tests
uv run python scripts/   # Run scripts
```
