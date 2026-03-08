# BioAI

Multi-agent AI system for DNA-precision diabetes care. Specialized agents analyze patient biological data across multiple omics domains — genomics, transcriptomics, proteomics, metabolomics — and synthesize personalized health assessments with multi-omics validation.

## Architecture

```
Patient
   ├── DNA Sequence ──→ [Genomics Agent] ──→ DMT1 / DMT2 / NONDM
   │                                                │
   ├── Clinical Chat ──→ [Doctor Agent] ──→ Diabetic / Non-Diabetic
   │                                                │
   │                                    ┌───────────┴───────────┐
   │                                 Hospital              Health Trainer
   │                                    │                       │
   │                    [Transcriptomics Agent]        [Health Trainer Agent]
   │                     (confirms / rejects)           (exercise prescription)
   │                            │
   │                    ┌───────┴───────┐
   │                 Confirmed      False Positive
   │                    │               │
   │              Pharmacology     Health Trainer
   │              (drug plan)      (no drugs needed)
   │
   └── Evaluation Engine → Ralph Loop (auto-improve prompts) → Dashboard
```

## Agents

| Agent | Domain | Backend | Status |
|-------|--------|---------|--------|
| **Genomics** | Inherited risk → DMT1/DMT2/NONDM | Pre-trained CNN (3-mer, 84%) | Implemented + evaluated |
| **Doctor** | Conversational intake → Diabetic/Non-Diabetic | Pre-trained MLP (Pima, 75%) | Implemented + evaluated |
| **Health Trainer** | Exercise prescription with clinical rules | ADA 2023 rules + 50-exercise DB | Implemented + evaluated |
| **Transcriptomics** | Pathway activity → subtype, false positive filter | GSE26168 z-score (110 genes) | Implemented |
| **Proteomics** | Functional biomarkers (inflammatory, kidney/CV) | TBD | In progress (YH) |
| **Metabolomics** | Metabolic state (insulin resistance, lipids, BCAAs) | TBD | In progress (YH) |
| Pharmacology | Subtype-informed drug recommendations | TBD | Stub |
| Clinical Guidelines | Medical guidelines | JSON knowledge base | Stub |
| Literature Review | Publications | PubMed, Semantic Scholar | Stub |

## Quick Start

```bash
uv sync
export ANTHROPIC_API_KEY=sk-...
uv run python scripts/run.py --case 1
uv run python scripts/evaluate.py --mock    # eval with pre-recorded outputs
uv run streamlit run app/dashboard.py        # eval dashboard
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
│   ├── agents/          # 9 agents (4 implemented, 2 in progress, 3 stubs)
│   ├── tools/           # Python functions backing agent tools
│   ├── prompts/         # System prompts (.txt, editable by Ralph Loop)
│   ├── eval/            # Metrics, LLM-as-judge, Ralph Loop
│   ├── models.py        # AgentResult, *Findings, HealthAssessment
│   ├── orchestrator.py  # Agent execution
│   └── config.py        # Settings
├── data/                # Datasets (gitignored)
├── scripts/             # CLI entry points
├── app/                 # Streamlit eval dashboard
├── tests/               # 90 tests (17 test files)
└── docs/                # Architecture, vision, data, demo
```
