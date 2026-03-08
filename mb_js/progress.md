# Progress — JS (Top-Down: Infra, Orchestration, Architecture)

## Active

### Phase 4: Integration & Polish — Eval Pipeline Improvements

#### Ralph v2 → evaluate.py wiring (P0)
- [x] `eval/ralph.py` — failure context, rollback/backup, metric filtering, history (8/8 tests)
- [ ] Wire into `scripts/evaluate.py`: collect failure examples from judge, pass history, rollback on regression

#### Transcriptomics in eval pipeline (P0)
- [ ] `eval/cases.py` — add `gene_expression` input field to EvalCase
- [ ] `eval/metrics.py` — add TranscriptomicsFindings to `score_tool_accuracy`
- [ ] `scripts/evaluate.py` — add `run_transcriptomics()` runner
- [ ] Update decision matrix for 3-layer validation (hospital → transcriptomics confirms/rejects)
- [ ] Add test case for false positive filter (hospital decision overridden by transcriptomics)
- [ ] Mock outputs for transcriptomics

#### Latency & cost tracking (P1)
- [ ] Track wall-clock time per agent in `evaluate_case()`
- [ ] Track API token usage (from Claude response metadata)
- [ ] Include in eval report + dashboard

#### Agent-aware judge context (P2)
- [ ] Tell judge what each agent can/can't see (doctor doesn't see DNA results)
- [ ] Fixes misleading low scores on doctor case-2/3

## Hold

- [ ] End-to-end: `scripts/run.py --case 1` (wire agents into orchestrator)
- [ ] Wire all agents into orchestrator
- [ ] Dashboard polish for demo

## Completed

### Phase 4: Ralph Loop v2
- [x] P0: Include failure examples + judge explanations in rewrite prompt
- [x] P0: Add rollback on regression (save before, compare after, revert if worse)
- [x] P1: Filter to prompt-improvable metrics only (skip tool_accuracy)
- [x] P2: Iteration memory / history log (prevent oscillation)
- [x] Tests for all new Ralph Loop behavior (8/8 pass)

### Phase 3: Evaluation Framework
- [x] `eval/cases.py` — 4 test cases with ground truth (EvalCase, ExpectedOutput)
- [x] `eval/metrics.py` — Layer 1 tool accuracy + Layer 3 decision correctness
- [x] `eval/judge.py` — Layer 2 LLM-as-judge (relevance, completeness, accuracy, safety, 1-5)
- [x] `eval/ralph.py` — Ralph Loop v1 (find weakest agent/metric → Claude Opus rewrites prompt)
- [x] `scripts/evaluate.py` — CLI runner (--mock, --save, --ralph --iter N)
- [x] `data/eval/case_inputs.json` — real DNA sequences + Pima clinical features + HT vitals
- [x] `app/dashboard.py` — Streamlit eval dashboard (Overview, Case Details, LLM-as-Judge tabs)
- [x] Health trainer integrated into eval (cases, metrics, evaluate.py, mock I/O)
- [x] Full eval: 13/13 deterministic pass (genomics, doctor, health_trainer, decision)
- [x] Ralph Loop 3 iterations — rewrote health_trainer.txt and doctor.txt
  - health_trainer: rel 2→5, comp 1→4, acc 3→5, safe 4→5
  - doctor: added verification step, systematic collection, comprehensive response
  - Note: doctor case-2/3 low judge scores expected (by design — no DNA context)
- [x] Docs updated: architecture.md, demo.md, README.md
- [x] 23/23 tests pass (metrics, cases, judge, ralph)

### Phase 2: Core Framework — **Reassigned to YH**
- YH owns: BaseAgent rewrite, orchestrator, synthesis, models, blackboard
- YH landed: genomics agent+tool, doctor agent+tool, diabetes classifier, health trainer agent+tools

### phase1-setup-models — Config rewrite
- [x] `config.py` → Pydantic BaseModel with multi-model fields, `from_env()`, paths
- [x] Test coverage for config (`tests/test_config.py`)

### main — Project scaffolding
- [x] Initialize repo with uv + Python 3.12
- [x] BaseAgent ABC and six agent stubs
- [x] Orchestrator skeleton
- [x] Config, tests, entry point
