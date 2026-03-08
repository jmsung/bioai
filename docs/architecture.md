# Architecture

## Core Pipeline: DNA-Precision Diabetes Decision

The primary use case is a two-stage sequential pipeline: DNA assessment first, then clinical assessment. The genomics result informs and can override the clinical result.

```
Patient
   │
   ├─── DNA Sequence ──▶ [Genomics Agent] ──▶ DMT1 / DMT2 / NONDM
   │                                                  │
   │                                    ┌─────────────┴──────────────┐
   │                                 High risk                   No risk (NONDM)
   │                                    │                            │
   ├─── Clinical Chat ──▶ [Doctor Agent] ──▶ Diabetic / Non-Diabetic  │
   │         (8 features gathered                   │               │
   │          through conversation)                 │               │
   │                                    ┌───────────┴───────────┐   │
   │                                 Diabetic             Non-Diabetic
   │                                 + High DNA risk       + No DNA risk
   │                                    │                       │
   │                              → Hospital              → Reconsider
   │                                    │                  (may not need drugs)
   │                         ┌──────────┴──────────┐
   │                       DMT1                   DMT2
   │                         │                      │
   │                    Insulin therapy        Metformin / GLP-1
   │                    (Type 1 drugs)         (Type 2 drugs)
   │
   ├─── (HEALTH_TRAINER) ──▶ [Health Trainer Agent]
   │                              │
   │                    classify_workout_type (ADA 2023 rules)
   │                    + diabetes context from Genomics & Doctor
   │                              │
   │                    recommend_exercises (50-exercise DB)
   │                              │
   │                    → Personalised weekly plan
   │
   └─── (Background) ──▶ [Transcriptomics, Proteomics, Pharma, Clinical, Literature]
                                          │
                                    Synthesis (Claude Opus)
                                          │
                                    Unified Health Report
```

## Full Multi-Agent Pipeline

```
Patient Case → Orchestrator → [6 Agents in Parallel] → Blackboard → Synthesis → Report
                                                                          ↓
                                                              Evaluation Engine
                                                                          ↓
                                                              Ralph Loop (improve prompts)
                                                                          ↓
                                                              Dashboard (Streamlit)
```

## Specialized Agents

| Agent | Tools | Backend | Role in Diabetes Pipeline |
|-------|-------|---------|--------------------------|
| **Genomics** | `classify_dna` | Pre-trained 2-layer CNN (3-mer tokenization) | Genetic predisposition: DMT1/DMT2/NONDM |
| **Doctor** | `classify_diabetes` | Pre-trained MLP (8 clinical features) | Conversational intake → hospital/health trainer routing |
| **Health Trainer** | `classify_workout_type`, `recommend_exercises` | ADA 2023 clinical rules + 50-exercise DB | Exercise prescription for HEALTH_TRAINER referrals |
| **Transcriptomics** | `run_gsea`, `classify_subtype` | GSEApy | Gene expression signals for progression |
| **Proteomics** | `lookup_protein`, `get_protein_interactions` | UniProt REST, STRING DB | Biomarker inference |
| **Pharmacology** | `search_drug_gene_interactions`, `search_adverse_effects` | DGIpy, OpenFDA | DNA-matched drug recommendations |
| **Clinical** | `lookup_guidelines`, `check_screening_criteria` | JSON knowledge base | Evidence-based guideline interpretation |
| **Literature** | `search_pubmed`, `search_semantic_scholar` | Biopython Entrez, semanticscholar | Latest research on DNA-matched treatment |

### Doctor Agent: Conversational Clinical Intake

Unlike the other agents which receive structured input, the Doctor Agent gathers data through natural conversation:

```
Patient speaks freely:
  "I'm 42, female, my glucose was 160 last week, 85kg at 165cm,
   pregnant twice, my mom has diabetes, I don't know my insulin."

Doctor Agent extracts:
  pregnancies=2, glucose=160, blood_pressure=80, skin_thickness=28,
  insulin=0, bmi=31.2, diabetes_pedigree_function=0.5, age=42

Calls: classify_diabetes(**extracted_values)
Returns: DoctorFindings(prediction, probability, risk_level, recommendation)
```

Recommendation logic (combined with genomics):

| Genomics | Clinical | Decision |
|---|---|---|
| DMT1 or DMT2 | Diabetic | → Hospital (confirmed) |
| DMT1 or DMT2 | Non-Diabetic | → Hospital (genetic override — early intervention) |
| NONDM | Diabetic | → Reconsider (may not need drugs) |
| NONDM | Non-Diabetic | → Health trainer (prevention) |

All tools: **on-device or free API calls** — no GPU, no paid APIs beyond Claude.

## Base Agent (agentic tool-use loop)

1. Build messages from blackboard context + query
2. Call Claude API with agent-specific tools
3. If `tool_use` blocks → execute Python tool function → append result → call again
4. Loop until `end_turn` → return structured `AgentResult`

## Orchestrator + Blackboard

### Blackboard
- `patient: Patient` — input data
- `query: str` — clinical question
- `agent_results: dict[str, AgentResult]` — accumulated findings
- `get_context_for_agent(name)` → patient + prior findings

### Orchestrator (2-phase)
- **Phase 1**: 6 agents run in parallel (`asyncio.gather`). Each reads patient data only.
- **Phase 2**: Synthesis (Claude Opus) reads ALL agent results → unified health assessment.
- **(Optional)**: Re-query agents if synthesis finds contradictions.

## Evaluation Pipeline

Three agents are evaluated: Genomics, Doctor, and Health Trainer (case-4 only). Four test cases with ground truth cover all branches of the decision matrix.

### Test Cases

| Case | DNA Input | Clinical Input | HT Vitals | Expected Decision |
|------|-----------|----------------|-----------|-------------------|
| case-1 | DMT2 (800bp) | diabetic (glucose=189, bmi=30.1, age=59) | — | hospital |
| case-2 | DMT2 (same) | non_diabetic (glucose=89, bmi=28.1, age=21) | — | hospital |
| case-3 | NONDM (1500bp) | diabetic (same as case-1) | — | reconsider |
| case-4 | NONDM (same) | non_diabetic (same as case-2) | age=21, Male, 170cm, 81.2kg, freq=0, dur=0 | health_trainer |

DNA sequences are real from the DNA classification dataset. Clinical features are real Pima Indians Diabetes rows. Health trainer vitals are derived from case-4 demographics. All stored in `src/bioai/eval/data/case_inputs.json`.

### Evaluation Layers

**Layer 1 — Tool Accuracy (deterministic, no LLM)**
Checks whether the underlying ML/rule tool returned the correct prediction:
- Genomics: `classify_dna(sequence)` → `predicted_class == expected_dna_class`?
- Doctor: `classify_diabetes(features)` → `prediction == expected_clinical_prediction`?
- Health Trainer: `classify_workout_type(vitals)` → `fitness_level == expected_fitness_level`?

Binary: 1.0 (correct) or 0.0 (wrong).

**Layer 2 — Agent Quality (LLM-as-judge)**
Claude Sonnet scores each agent's output on a 1-5 scale. The judge sees the agent's `AgentResult` (findings JSON + summary) alongside the case ground truth:

| Dimension | Question |
|-----------|----------|
| Relevance (1-5) | Does the output address the clinical question? |
| Completeness (1-5) | Are all relevant findings covered? |
| Accuracy (1-5) | Is the interpretation clinically correct given ground truth? |
| Safety (1-5) | Any harmful or misleading recommendations? (5 = safe) |

**Layer 3 — Decision Correctness (deterministic)**
Combines genomics + doctor outputs through the decision matrix:

| Genomics | Doctor | Expected Decision |
|---|---|---|
| DMT1/DMT2 | Diabetic | Hospital (confirmed) |
| DMT1/DMT2 | Non-Diabetic | Hospital (DNA override) |
| NONDM | Diabetic | Reconsider (lifestyle first) |
| NONDM | Non-Diabetic | Health Trainer (prevention) |

### Current Results (13/13 deterministic pass)

| Case | Genomics Tool | Doctor Tool | HT Tool | Decision | Judge (genomics) | Judge (doctor) | Judge (HT) |
|------|--------------|-------------|---------|----------|-----------------|----------------|------------|
| case-1 | PASS | PASS | — | PASS | 5/4/5/5 | 5/4/5/5 | — |
| case-2 | PASS | PASS | — | PASS | 5/4/5/4 | 2/1/1/1* | — |
| case-3 | PASS | PASS | — | PASS | 4/3/5/3 | 2/1/2/2* | — |
| case-4 | PASS | PASS | PASS | PASS | 5/5/5/5 | 5/4/5/5 | 5/4/5/5 |

*Doctor case-2/3 judge scores are low by design — the doctor agent doesn't see DNA results. The decision matrix (Layer 3) handles the cross-agent logic correctly.

### Execution Modes

```bash
uv run python scripts/evaluate.py              # real mode (all agents + judge via Claude API)
uv run python scripts/evaluate.py --mock       # mock mode (pre-recorded outputs, scoring only)
uv run python scripts/evaluate.py --save       # real mode + save outputs for future mock runs
uv run python scripts/evaluate.py --ralph --iter 3  # Ralph Loop (3 prompt optimization iterations)
```

- **Real mode**: ~$0.15/run, ~30s. Runs agents + judge via Claude API.
- **Mock mode**: Free, instant. Uses saved JSON from `src/bioai/eval/data/mock_outputs/`.
- **Workflow**: real `--save` → iterate on eval logic in mock → Ralph Loop → real again.

## Ralph Loop (Iterative Prompt Optimization)

Automated prompt improvement: evaluate → find weakest agent/metric → rewrite prompt → re-evaluate.

### Data Flow

```
evaluate_case() × 4 cases
    → Layer 1: tool accuracy (deterministic)
    → Layer 2: judge scores (Claude Sonnet, 4 dimensions × 1-5)
    → Layer 3: decision correctness (deterministic)
           ↓
collect_judge_averages()
    → Per-agent averages: {genomics: {rel: 5.0, comp: 4.0, ...}, doctor: {...}, health_trainer: {...}}
           ↓
_find_weakest()
    → Scan all (agent, metric) pairs → pick the single lowest score
    → e.g. ("health_trainer", "completeness", 1.0)
           ↓
ralph_iterate()
    → Read src/bioai/prompts/{agent}.txt
    → Send to Claude Opus:
        System: "You are an expert prompt engineer for biomedical AI agents.
                 Rewrite to improve the weakest metric. Keep tool-calling instructions intact."
        User:   "Agent: health_trainer, Weakest: completeness (1.0),
                 All scores: {rel: 2.0, comp: 1.0, acc: 3.0, safe: 4.0}
                 Current prompt: [full text]"
    → Opus returns rewritten prompt
    → Save to disk (overwrites the .txt file)
           ↓
Re-run full evaluation (all 4 cases × all agents × all 3 layers)
    → New judge averages → next iteration
```

### Results (3 iterations)

| Iter | Target | Score | Prompt Rewritten | Effect |
|------|--------|-------|------------------|--------|
| 1 | health_trainer/completeness | 1.0 | health_trainer.txt | rel 2→4, comp 1→3, acc 3→4, safe 4→5 |
| 2 | doctor/completeness | 2.5 | doctor.txt | Added verification step, systematic checklist |
| 3 | doctor/completeness | 2.8 | doctor.txt | Further persistence + response structure |

Prompts are `.txt` files on disk — Ralph Loop reads, rewrites, saves. No code changes per iteration.

## Model Strategy

| Component | Model | Why |
|-----------|-------|-----|
| Agent analysis | `claude-sonnet-4-20250514` | Fast + cheap for tool use |
| Synthesis | `claude-opus-4-20250514` | Best quality for final report |
| LLM-as-judge | `claude-sonnet-4-20250514` | Cost-efficient scoring |
| Ralph Loop | `claude-opus-4-20250514` | Needs strong reasoning |

Cost: ~$0.15/run. Budget: ~$5-10 for hackathon.

## Project Structure

```
src/bioai/
├── config.py                  Pydantic settings (models, API keys, paths)
├── models.py                  AgentResult, GenomicsFindings, DoctorFindings, HealthTrainerFindings
├── blackboard.py              Shared state for agent communication
├── orchestrator.py            2-phase: parallel agents → synthesis
├── agents/
│   ├── base.py                BaseAgent ABC
│   ├── genomics.py            DNA classification → DMT1/DMT2/NONDM
│   ├── doctor.py              Conversational intake → Diabetic/Non-Diabetic
│   ├── health_trainer.py      Exercise prescription with clinical context
│   ├── transcriptomics.py     GSEApy pathway enrichment (stub)
│   ├── proteomics.py          UniProt REST API (stub)
│   ├── pharmacology.py        DGIpy, OpenFDA (stub)
│   ├── clinical.py            Guidelines knowledge base (stub)
│   └── literature.py          PubMed, Semantic Scholar (stub)
├── tools/
│   ├── dna_classifier.py      Pre-trained CNN (3-mer, 84% accuracy)
│   ├── diabetes_classifier.py Pre-trained MLP (Pima, 75% accuracy)
│   ├── workout_type_classifier.py  ADA 2023 clinical rules
│   └── exercise_recommender.py     50-exercise CSV lookup
├── prompts/                   System prompts as .txt (Ralph Loop edits these)
│   ├── genomics.txt
│   ├── doctor.txt
│   └── health_trainer.txt
└── eval/
    ├── cases.py               4 test cases with ground truth
    ├── metrics.py             Layer 1 (tool accuracy) + Layer 3 (decision correctness)
    ├── judge.py               Layer 2 (LLM-as-judge, 4 dimensions × 1-5)
    ├── ralph.py               Ralph Loop prompt optimizer
    └── data/
        ├── case_inputs.json   DNA sequences + clinical features + HT vitals
        └── mock_outputs/      Pre-recorded AgentResult JSON per case per agent
```

## Tech Stack

- Python 3.12 + uv
- Anthropic Claude API (agent reasoning)
- asyncio (concurrency)
- Streamlit (dashboard)
