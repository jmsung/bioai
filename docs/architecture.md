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

### Evaluation Layers

The eval framework is designed around the 2-agent demo (Genomics + Doctor) first, but is scalable — each layer applies to any agent that gets added.

**Layer 1 — Tool Accuracy (deterministic, no LLM)**
Checks whether the underlying ML model returns the correct prediction.
- `classify_dna(sequence)` → expected class (DMT1/DMT2/NONDM)
- `classify_diabetes(features)` → expected prediction (Diabetic/Non-Diabetic)

**Layer 2 — Agent Quality (LLM-as-judge)**
Scores each agent's output on a 1-5 scale across four dimensions.
- Relevance: Does the output address the clinical question?
- Completeness: Are all relevant findings covered?
- Accuracy: Is the interpretation clinically correct?
- Safety: Are there any harmful or misleading recommendations?

**Layer 3 — Decision Quality (deterministic + LLM)**
Checks whether the combined agent outputs produce the correct final decision per the decision matrix:

| Genomics | Doctor | Expected Decision |
|---|---|---|
| DMT1/DMT2 | Diabetic | Hospital (confirmed) |
| DMT1/DMT2 | Non-Diabetic | Hospital (DNA override) |
| NONDM | Diabetic | Reconsider (lifestyle first) |
| NONDM | Non-Diabetic | Health Trainer (prevention) |

### Metrics Summary

| Category | Metric | Method | Target |
|----------|--------|--------|--------|
| Tool | DNA classification accuracy | vs ground truth label | >80% |
| Tool | Clinical prediction accuracy | vs ground truth label | >75% |
| Quality | Relevance (1-5) | LLM-as-judge | >3.5 |
| Quality | Completeness (1-5) | LLM-as-judge | >3.5 |
| Quality | Accuracy (1-5) | LLM-as-judge | >3.5 |
| Safety | Harmful recommendation | LLM-as-judge | 0 |
| Safety | Clinical constraint violations | Synthetic diabetes overlay on gym data | 0 |
| Decision | Combined decision correctness | vs decision matrix | 100% |
| Health Trainer | Experience level accuracy | vs gym members ground truth | Track (48.2%) |
| Health Trainer | Workout type baseline | vs gym members (NONDM) | Track (19.7%) |
| System | Latency per agent | time.time() | <30s |
| System | Cost per run | API usage field | Track |

### Execution Modes

**Real mode** (`scripts/evaluate.py`): Runs each agent end-to-end via Claude API. Produces actual agent outputs, then scores them. Use this to measure real quality and after prompt changes.
- Cost: ~$0.15/run, ~30s

**Mock mode** (`scripts/evaluate.py --mock`): Skips Claude API calls. Uses pre-recorded agent outputs (saved from a previous real run or hand-crafted). Only the scoring logic runs. Use this to:
- Iterate on eval/scoring logic without burning API credits
- Test the eval framework itself in CI
- Get fast feedback during metric development

**Workflow**: Run real mode → save outputs as baseline → iterate on eval logic in mock mode → change prompts via Ralph Loop → run real mode again to measure improvement.

### LLM-as-Judge
Claude Sonnet scores each agent on relevance, completeness, accuracy, safety. Returns `{score, explanation}`.

## Ralph Loop (Iterative Improvement)

Simple v1: evaluate → find weakest agent → update prompt → re-evaluate. Iteration process can be improved later.

```
while not all_criteria_met (max 5 iterations):
    1. Run all test cases through full pipeline (real mode)
    2. Score every agent on every metric
    3. Find worst-performing agent + metric
    4. Use Claude Opus to rewrite that agent's system prompt
       (input: current prompt + eval results + failure examples)
    5. Re-run evaluation with new prompt
    6. If improved → keep new prompt, log change
       If degraded → revert, try different approach
    7. Log learnings to guardrails file
```

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
├── models.py                  Patient, AgentResult, TestCase Pydantic models
├── blackboard.py              Shared state for agent communication
├── orchestrator.py            2-phase: parallel agents → synthesis
├── synthesis.py               Claude-powered final report generation
├── agents/
│   ├── base.py                BaseAgent with agentic tool-use loop
│   ├── genomics.py            myvariant.info, ClinVar
│   ├── transcriptomics.py     GSEApy pathway enrichment
│   ├── proteomics.py          UniProt REST API
│   ├── pharmacology.py        DGIpy, OpenFDA
│   ├── clinical.py            Guidelines knowledge base
│   └── literature.py          PubMed (Entrez), Semantic Scholar
├── tools/                     Plain Python functions backing agent tools
│   ├── genomics_tools.py
│   ├── transcriptomics_tools.py
│   ├── proteomics_tools.py
│   ├── pharma_tools.py
│   ├── clinical_tools.py
│   └── literature_tools.py
├── prompts/                   System prompts as .txt (Ralph Loop edits these)
│   ├── genomics.txt
│   ├── transcriptomics.txt
│   ├── proteomics.txt
│   ├── pharmacology.txt
│   ├── clinical.txt
│   ├── literature.txt
│   └── synthesis.txt
└── eval/
    ├── metrics.py             Automated + LLM-as-judge scoring
    ├── cases.py               Test cases with ground truth
    ├── judge.py               Claude-as-evaluator
    └── ralph.py               Ralph Loop prompt optimizer
```

## Tech Stack

- Python 3.12 + uv
- Anthropic Claude API (agent reasoning)
- asyncio (concurrency)
- Streamlit (dashboard)
