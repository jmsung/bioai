# Clinical Validation — Case Studies

## Motivation

> *"Your doctor says you have diabetes. Should you trust that? What if your DNA says otherwise?"*

Standard diabetes diagnosis relies on blood tests alone. But two patients with identical glucose and BMI can have fundamentally different biological realities. Multi-omics validation changes clinical outcomes.

---

## Validation Cases

### Case 1 — Confirmed Diabetic
- Clinical: glucose=189, BMI=30.1, age=59
- DNA: DMT2 (high confidence)
- Transcriptomics: 5/5 pathways active (inflammation, insulin resistance dominant)
- **Decision: Hospital → Pharmacology → metformin + GLP-1**

### Case 2 — DNA Override: Early Intervention
- Clinical: glucose=89, BMI=28.1, age=21 (looks healthy)
- DNA: DMT2 (high confidence)
- Transcriptomics: mild pathway activation (early molecular signs)
- **Decision: Hospital (genetic risk overrides clean labs, catch it early)**

### Case 3 — Clinical Override: Avoid Unnecessary Treatment
- Clinical: glucose=189 (looks diabetic)
- DNA: NONDM (no genetic predisposition)
- **Decision: Reconsider (lifestyle first, avoid unnecessary drugs)**

### Case 4 — Healthy Prevention
- Clinical: glucose=89 (normal), DNA: NONDM
- **Decision: Health Trainer (exercise plan)**

### Case 5 — Hospital 4-Layer Validation
- Genomics + Doctor → Hospital
- Hospital Agent: explains blood tests, patient consents
- Transcriptomics + Metabolomics both confirm → Pharmacology

### Case 6 — Hospital False Positive Filter
- Genomics + Doctor → Hospital
- Transcriptomics: no pathway activation, Metabolomics: normal
- Combined: neither confirms → Health Trainer (avoid unnecessary drugs)

---

## 3-Layer Validation Architecture

```
Layer 1: DNA (Genomics CNN) ──────────────────┐
Layer 2: Clinical (Doctor + Pima classifier) ──┼── Decision Matrix
Layer 3: Molecular (Transcriptomics 5-pathway)─┘
    ├── Hospital → Pharmacology (ADA drug matching)
    └── Healthy → Health Trainer (exercise plan)
```

Key insight: Same clinical numbers, different DNA → different treatment. The 3rd layer (transcriptomics) catches false positives before unnecessary medication.

---

## Self-Improving Evaluation — Ralph Loop

Agents improve automatically without code changes:
1. Ralph identifies weakest agent + metric from eval scores
2. Automatically rewrites the agent's prompt
3. Re-evaluates — scores improve
4. If scores regress, rolls back automatically

---

## Running Validation

```bash
uv run python scripts/run.py --case 1              # E2E pipeline (single case)
uv run python scripts/run.py --all --mock           # All cases (pre-recorded)
uv run python scripts/evaluate.py --mock            # Mock eval (15/15 pass)
uv run python scripts/evaluate.py --ralph --iter 3  # Ralph Loop auto-improvement
uv run pytest --tb=short -q                         # Full test suite (200 pass)
```
