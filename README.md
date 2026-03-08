# BioAI

Multi-agent AI system for personalized healthcare intelligence. Specialized agents analyze patient biological data across six domains and synthesize integrated health assessments with evidence-grounded reasoning.

## Architecture

```
Patient Case → Orchestrator → [6 Agents in Parallel] → Blackboard → Synthesis → Report
                                        ↓                                ↓
                                   Tool Calls                    Evaluation Engine
                              (APIs, databases)                  Ralph Loop (auto-improve)
```

## Agents

| Agent | Domain | Backend | Status |
|-------|--------|---------|--------|
| **Genomics** | DNA → DMT1/DMT2/NONDM | Pre-trained CNN (3-mer, 84%) | Implemented + evaluated |
| **Doctor** | Conversational intake → Diabetic/Non-Diabetic | Pre-trained MLP (Pima, 75%) | Implemented + evaluated |
| **Health Trainer** | Exercise prescription with clinical rules | ADA 2023 rules + 50-exercise DB | Implemented + evaluated |
| Pharmacology | Drug interactions | DGIpy, OpenFDA | Stub |
| Transcriptomics | Gene expression | GSEApy, PAM50 | Stub |
| Proteomics | Biomarker inference | UniProt, STRING DB | Stub |
| Clinical Guidelines | Medical guidelines | JSON knowledge base | Stub |
| Literature Review | Publications | PubMed, Semantic Scholar | Stub |

## Quick Start

```bash
uv sync
export ANTHROPIC_API_KEY=sk-...
uv run python scripts/run.py --case 1
```

## Tech Stack

- **Python 3.12** + uv
- **Claude API** (Anthropic) — agent reasoning, synthesis, evaluation
- **asyncio** — parallel agent execution
- **Streamlit** — interactive dashboard

## Project Structure

```
bioai/
├── src/bioai/
│   ├── agents/          # 6 domain-specific agents
│   ├── tools/           # Python functions backing agent tools
│   ├── prompts/         # System prompts (.txt, editable by Ralph Loop)
│   ├── eval/            # Metrics, LLM-as-judge, Ralph Loop
│   ├── models.py        # Patient, AgentResult, TestCase
│   ├── blackboard.py    # Shared state for agent communication
│   ├── orchestrator.py  # 2-phase: parallel agents → synthesis
│   └── config.py        # Settings
├── data/                # Datasets (gitignored)
├── scripts/             # CLI entry points
├── app/                 # Streamlit dashboard
├── tests/               # Tests
└── docs/                # Architecture, vision, data, demo
```
