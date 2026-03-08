# Progress — JS (Top-Down: Infra, Orchestration, Architecture)

## Active

### Phase 3: Evaluation Framework
- [x] `eval/cases.py` — 4 test cases with ground truth (EvalCase, ExpectedOutput)
- [x] `eval/metrics.py` — deterministic scoring (tool accuracy + decision matrix)
- [x] `eval/judge.py` — LLM-as-judge (relevance, completeness, accuracy, safety)
- [x] `eval/ralph.py` — Ralph Loop v1 (find weakest → rewrite prompt)
- [x] `scripts/evaluate.py` — CLI runner (--mock, --save, --ralph --iter N)
- [x] `data/eval/case_inputs.json` — real DNA sequences + Pima clinical features
- [x] Baseline eval run — 12/12 deterministic pass, judge scores saved
- [x] `prompts/genomics.txt` — extracted from hardcoded agent (Ralph Loop ready)
- [x] `app/dashboard.py` — Streamlit eval dashboard (Overview, Case Details, LLM-as-Judge tabs)

### Waiting on YH
- [ ] Re-run full eval after YH merges agent updates (genomics, doctor, health trainer)
- [ ] Run Ralph Loop to improve prompts based on judge feedback

## Hold

### Phase 4: Integration & Polish
- [ ] End-to-end test: `scripts/run.py --case 1`
- [ ] Wire all 6 agents into orchestrator
- [ ] Bug fixes, error handling, polish

## Todo

## Completed

### Phase 2: Core Framework — **Reassigned to YH**
- YH owns: BaseAgent rewrite, orchestrator, synthesis, models, blackboard
- YH landed: genomics agent+tool, doctor agent+tool, diabetes classifier

### phase1-setup-models — Config rewrite
- [x] `config.py` → Pydantic BaseModel with multi-model fields, `from_env()`, paths
- [x] Test coverage for config (`tests/test_config.py`)

### main — Project scaffolding
- [x] Initialize repo with uv + Python 3.12
- [x] BaseAgent ABC and six agent stubs
- [x] Orchestrator skeleton
- [x] Config, tests, entry point
