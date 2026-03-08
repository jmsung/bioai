# Demo Plan

## Presentation (2 minutes)

1. **(15s)** Problem: cancer treatment needs genomics + drugs + literature + guidelines — no single clinician has it all
2. **(60s)** Live: METABRIC patient → 6 agents in parallel → show analyses → synthesis report
3. **(30s)** Dashboard: eval scores → Ralph Loop: "3 iterations: relevance 3.2→4.1, hallucination 12%→4%"
4. **(15s)** Architecture slide

**Prep**: Pre-cache API responses. Fallback pre-recorded run.

## Dashboard (Streamlit)

| Tab | Content |
|-----|---------|
| **MDT Meeting** | Select patient → Run Analysis → agent cards (color-coded confidence) → synthesis report |
| **Evaluation** | Test case x Agent score heatmap, aggregate metrics, latency/cost charts |
| **Ralph Loop** | Iteration timeline, before/after scores, prompt viewer |

## Priority Tiers

### P0 — MVP
- [ ] `models.py`, `blackboard.py`, `base.py`, `orchestrator.py`
- [ ] 3 agents: Genomics, Pharmacology, Literature
- [ ] 1 patient test case
- [ ] `scripts/run.py` CLI
- [ ] Streamlit MDT Meeting tab

### P1 — Should Have
- [ ] Remaining 3 agents (Transcriptomics, Proteomics, Clinical)
- [ ] Evaluation framework with LLM-as-judge
- [ ] Ralph Loop (1-2 iterations)
- [ ] Streamlit evaluation tab

### P2 — Nice to Have
- [ ] Streamlit Ralph Loop tab
- [ ] Debate/contradiction resolution
- [ ] More test cases

### Explicitly Skip
- GPU-requiring models (ESM-2, DNABERT-2, AlphaFold)
- FHIR data formatting
- Synthea patient generation
- Database/persistent storage
- Auth/user management

## Verification Commands

```bash
uv run python scripts/run.py --case 1              # full pipeline
uv run python scripts/evaluate.py                   # eval suite
uv run python scripts/evaluate.py --ralph --iter 3  # Ralph Loop
uv run streamlit run app/dashboard.py               # dashboard
```
