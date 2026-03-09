# Demo Plan — 3-Minute Hackathon Presentation

## The Story

> *"Your doctor says you have diabetes. Should you trust that? What if your DNA says otherwise?"*

We show patients with identical clinical readings but different genetic realities — getting different, correct recommendations. Then we show how the system improves itself automatically.

---

## Presentation Flow (3 minutes)

### Act 1: The Problem (20s)

Doctors diagnose diabetes from blood tests alone. But two patients with identical glucose and BMI can have completely different futures. DNA + molecular evidence changes everything.

### Act 2: Live E2E Pipeline (90s)

Run `scripts/run.py --case 1` live. Show a patient flowing through 3 validation layers:

**Patient A — Confirmed Diabetic (case-1)**
```
DNA (Genomics) → DMT2 detected (85% confidence)
Clinical (Doctor) → Diabetic (glucose=189, BMI=30.1)
Molecular (Transcriptomics) → 5/5 pathways active, confirmed
→ Decision: HOSPITAL → Pharmacology → metformin + GLP-1
```

**Patient B — DNA Override (case-2)**
```
DNA (Genomics) → DMT2 detected
Clinical (Doctor) → Non-Diabetic (clean labs)
Molecular (Transcriptomics) → Early pathway activation, confirmed
→ Decision: HOSPITAL → catch it early, before symptoms
```

**Patient C — No Genetic Risk (case-3)**
```
DNA (Genomics) → NONDM (no genetic risk)
Clinical (Doctor) → Diabetic (looks diabetic on paper)
→ Decision: RECONSIDER → avoid unnecessary drugs, lifestyle first
```

Key message: Same clinical numbers, different DNA → different treatment. The 3rd layer (transcriptomics) catches false positives.

### Act 3: Self-Improving System — Ralph Loop (30s)

> "What if an agent gives a bad answer? We don't rewrite code — we run Ralph Loop."

Show before/after:
- Ralph identifies weakest agent + metric from eval scores
- Automatically rewrites the agent's prompt
- Re-evaluates — scores improve
- If scores regress, it rolls back automatically

```bash
uv run python scripts/evaluate.py --mock       # 15/15 metrics pass
uv run python scripts/evaluate.py --ralph --iter 3  # auto-improve
```

### Act 4: Architecture (20s)

Show the 3-layer validation diagram:
```
Layer 1: DNA (Genomics CNN) ──────────────────┐
Layer 2: Clinical (Doctor + Pima classifier) ──┼── Decision Matrix
Layer 3: Molecular (Transcriptomics 5-pathway)─┘
    ├── Hospital → Pharmacology (ADA drug matching)
    └── Healthy → Health Trainer (exercise plan)
```

8 specialized agents, Claude as reasoning backbone, deterministic tools for accuracy.

---

## Demo Cases

### Case 1 — Confirmed Diabetic
- Clinical: glucose=189, BMI=30.1, age=59
- DNA: DMT2 (high confidence)
- Transcriptomics: 5/5 pathways active (inflammation, insulin resistance dominant)
- → **Hospital** → Pharmacology → metformin

### Case 2 — DNA Override: Early Intervention
- Clinical: glucose=89, BMI=28.1, age=21 (looks healthy)
- DNA: DMT2 (high confidence)
- Transcriptomics: mild pathway activation (early molecular signs)
- → **Hospital** (genetic risk overrides clean labs)

### Case 3 — Clinical Override: Avoid Unnecessary Treatment
- Clinical: glucose=189 (looks diabetic)
- DNA: NONDM (no genetic predisposition)
- → **Reconsider** (lifestyle first, avoid drugs)

### Case 4 — Healthy Prevention
- Clinical: glucose=89 (normal), DNA: NONDM
- → **Health Trainer** (exercise plan)

### Case 5 — Hospital 4-Layer Validation (stretch)
- Genomics + Doctor → **Hospital**
- Hospital Agent: explains blood tests, patient consents
- Transcriptomics + Metabolomics both confirm → **Pharmacology**

### Case 6 — Hospital False Positive Filter (stretch)
- Genomics + Doctor → **Hospital**
- Transcriptomics: no pathway activation, Metabolomics: normal
- Combined: neither confirms → **Health Trainer** (avoid unnecessary drugs)

---

## Priority Tiers

### P0 — Demo Critical
- [x] 5 working agents: Genomics, Doctor, Transcriptomics, Pharmacology, Health Trainer
- [x] Eval pipeline: 15/15 mock metrics, 165 tests
- [x] Ralph Loop v2: failure context, rollback, history
- [x] Transcriptomics as 3rd validation layer in eval
- [ ] `scripts/run.py --case N` — E2E pipeline CLI (the demo entry point)

### P1 — Nice to Have
- [ ] Streamlit dashboard: visual pipeline flow for presentation
- [x] Metabolomics Agent — metabolic state (YH landed)
- [x] Hospital Agent — coordinates molecular tests (YH landed)
- [ ] Proteomics Agent — protein biomarkers (YH in progress)

### Explicitly Skip
- GPU models (ESM-2, DNABERT-2, AlphaFold)
- FHIR, Synthea, database, auth
- Latency/cost tracking

---

## Verification Commands

```bash
uv run python scripts/run.py --case 1              # E2E pipeline (demo entry point)
uv run python scripts/evaluate.py --mock            # mock eval (15/15 pass)
uv run python scripts/evaluate.py --ralph --iter 3  # Ralph Loop auto-improvement
uv run pytest --tb=short -q                         # full test suite (165 pass)
```
