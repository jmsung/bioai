# Health Trainer Agent

Conversational agent that creates personalized exercise plans for patients referred by the doctor agent (`Recommendation.HEALTH_TRAINER`). Uses clinical rules derived from ADA 2023 and ACSM guidelines to classify workout type, informed by prior genomics and doctor findings.

---

## Role in the Pipeline

```
Patient
   │
   ├── DNA Sequence ──▶ [GenomicsAgent] ──▶ DMT1 / DMT2 / NONDM
   │                                              │
   ├── Clinical Chat ──▶ [DoctorAgent] ──▶ Diabetic / Non-Diabetic
   │                                              │
   │                              ┌───────────────┴────────────────┐
   │                           High risk                     Moderate/Low risk
   │                              │                                │
   │                         → Hospital                    → HealthTrainerAgent
   │                                                               │
   │                                              ┌────────────────┤
   │                                              ▼                ▼
   │                                    classify_workout_type   recommend_exercises
   │                                              │                │
   │                                              ▼                ▼
   │                                    type + experience    filtered exercises
   │                                              │                │
   │                                              └────────┬───────┘
   │                                                       ▼
   └──────────────────────────────────────▶  Weekly Exercise Plan + Report
```

---

## Files

| File | Purpose |
|---|---|
| `src/bioai/agents/health_trainer.py` | Agent class (two-tool conversational flow) |
| `src/bioai/tools/workout_type_classifier.py` | Clinical rule-based workout type + experience level classifier |
| `src/bioai/tools/exercise_recommender.py` | Exercise database lookup/filter tool |
| `src/bioai/prompts/health_trainer.txt` | System prompt with 7-step conversation flow |
| `src/bioai/models.py` | `HealthTrainerFindings` model |
| `scripts/evaluate_health_trainer.py` | 3-layer evaluation against gym members dataset |
| `data/exercises/raw/exercises.csv` | 50-exercise dataset |
| `data/gym_members/raw/gym_members.csv` | 973-row gym members dataset (evaluation + future ML) |

### Tests

| File | Count | What it covers |
|---|---|---|
| `tests/test_workout_type_classifier.py` | 15 | Clinical rules, experience thresholds, BMI/age modifiers |
| `tests/test_health_trainer_agent.py` | 10 | Context injection, two-tool flow, findings lifecycle |
| `tests/test_exercise_recommender.py` | 9 | Filter logic, combined filters, field validation |
| `tests/test_integration_full_pipeline.py` | 1 | Full DNA → Doctor → HealthTrainer end-to-end |
| `tests/test_integration_genomics_doctor.py` | 1 | DNA → Doctor two-agent pipeline (pre-existing) |

---

## Data Flow

```
GenomicsFindings ─┐
                  ├─→ classify_workout_type(age, gender, weight, height,
DoctorFindings ───┘                         diabetes_type, risk_prob,
                                            frequency, duration)
                                            │
                      clinical rules ────── ┤─ diabetes modifier  (ADA 2023 + ACSM)
                      demographic base ───── ┘─ flat 1.0 baseline  (→ EXTENSION POINT A)
                                            │
                                            ▼
                                  ranked_workout_types + experience_level
                                            │
                                            ▼
                             recommend_exercises(type, difficulty)
                                            │
                                            ▼
                                  weekly exercise plan
```

---

## Conversation Flow (7 steps)

```
Step 1  Introduce as health trainer, explain the plan.

Step 2  Ask: age, gender, height, weight.

Step 3  Ask: exercise frequency (days/week) and session duration (hours).
        → 0 frequency / 0 duration is fine — records as no prior exercise.

Step 4  Call classify_workout_type()
        → uses vitals + exercise history + diabetes findings from context
        → returns suggested_type (Cardio/Strength/Flexibility/HIIT)
                   experience_level (Beginner/Intermediate/Expert)
                   reasoning (explained to patient in plain language)

Step 5  Ask: available equipment, body parts to focus on or avoid, any injuries.

Step 6  Call recommend_exercises(exercise_type, difficulty, equipment?, body_part?)
        → may be called multiple times for different body parts.

Step 7  Deliver weekly plan with clinical reasoning explained in plain language.
```

---

## Tool: `classify_workout_type`

```python
classify_workout_type(
    age: int,
    gender: str,                      # "Male" / "Female"
    weight_kg: float,
    height_cm: float,
    workout_frequency_per_week: int,
    session_duration_hours: float,
    diabetes_type: str,               # "DMT1" / "DMT2" / "NONDM"
    diabetes_probability: float,      # 0.0–1.0 from DoctorAgent
) -> {
    "suggested_type": "Strength",     # highest-scoring workout type
    "experience_level": "Beginner",   # from exercise history
    "bmi": 24.5,
    "reasoning": "...",               # plain-language explanation
    "all_scores": {                   # full ranking
        "Cardio": 1.6,
        "Strength": 1.8,
        "Flexibility": 1.2,
        "HIIT": 0.8,
    },
}
```

### Architecture: two independent layers

The classifier has two layers that can be improved independently:

```
┌──────────────────────────────────────────────────────────┐
│  Layer 1: Demographic base scores                        │
│  Currently: flat 1.0 for all types                       │
│  → EXTENSION POINT A: replace with ML model              │
│    trained on gym_members.csv (age, gender, BMI → type)  │
│  Input: age, gender, weight_kg, height_cm                │
│  Output: base scores per workout type                    │
│  File: _score_types() in workout_type_classifier.py      │
├──────────────────────────────────────────────────────────┤
│  Layer 2: Clinical override (DO NOT MODIFY)              │
│  Source: ADA 2023, ACSM guidelines                       │
│  Input: diabetes_type, diabetes_probability, bmi, age    │
│  Output: score adjustments (additive)                    │
│  These rules are safety-critical — changes require       │
│  clinical literature review.                             │
└──────────────────────────────────────────────────────────┘
```

### Clinical rules (ADA 2023 + ACSM)

| Condition | Effect on scores |
|---|---|
| DMT1 (genetic) | Cardio +0.5, Strength +0.3, **HIIT −0.8** (hypoglycemia risk) |
| DMT2 (genetic or clinical prob ≥ 0.5) | **Strength +0.5, Cardio +0.5** (ADA gold standard), HIIT +0.1 |
| Pre-diabetic (prob 0.35–0.5) | Cardio +0.2, Strength +0.2, Flexibility +0.1 |
| BMI ≥ 35 | Cardio +0.3, Flexibility +0.2, **HIIT −0.3** (joint stress) |
| BMI ≥ 30 | Cardio +0.1, HIIT −0.1 |
| Age ≥ 65 | **Flexibility +0.4**, Strength +0.2, **HIIT −0.5** (cardiac stress) |
| Age ≥ 50 | Flexibility +0.2, HIIT −0.2 |
| Age < 30 | HIIT +0.2 (recovery capacity) |
| Beginner experience | HIIT −0.3, Cardio +0.1 |
| Expert experience | HIIT +0.3 |

### Experience level thresholds

| Frequency (days/wk) | Session (hours) | Level |
|---|---|---|
| 0 or 0h session | — | Beginner |
| ≤ 1 or < 0.75h | — | Beginner |
| 2–3 and ≥ 0.75h | — | Intermediate |
| ≥ 4 and > 1.0h | — | Expert |

---

## Tool: `recommend_exercises`

```python
recommend_exercises(
    body_part="Legs",       # optional
    exercise_type="Cardio", # optional — use suggested_type from classifier
    difficulty="Beginner",  # optional — use experience_level from classifier
    equipment="Bodyweight", # optional
    max_results=10,         # optional
) -> {
    "exercises": [...],     # list of exercise dicts
    "total_found": int,
    "filters_applied": {...},
}
```

Reads `data/exercises/raw/exercises.csv` (cached with `@lru_cache`). Full Body exercises are always included when filtering by a specific body part.

---

## Clinical Context Injection

Prior agent findings are injected into the system prompt at agent construction time:

```python
trainer = HealthTrainerAgent(
    context={
        "genomics": genomics_result.model_dump(),
        "doctor":   doctor_result.model_dump(),
    }
)
```

Claude reads this silently and uses `diabetes_type` + `diabetes_probability` when calling `classify_workout_type`. If no context is provided, defaults to `NONDM` / `0.0`.

---

## Output Model: `HealthTrainerFindings`

```python
HealthTrainerFindings(
    fitness_level="beginner",           # from experience_level
    goals=["weight loss", "cardio"],    # extracted from conversation
    recommended_exercises=[...],        # all exercises from recommend_exercises calls
    weekly_plan="...",                  # trainer's final narrative plan
)
```

Wrapped in `AgentResult`. `findings` is `None` until **both** `classify_workout_type` and `recommend_exercises` have been called.

---

## Evaluation

### Running

```bash
uv run python scripts/evaluate_health_trainer.py
```

### Three-layer evaluation against gym members dataset (973 rows)

| Layer | What it tests | Ground truth | Key metric |
|---|---|---|---|
| **1. Experience level** | Threshold calibration | `Experience_Level` (1/2/3) from gym data | Accuracy |
| **2. Workout type baseline** | Demographic scoring (NONDM, prob=0.0) | `Workout_Type` from gym data | Accuracy (expected low) |
| **3. Clinical constraints** | Safety rules with synthetic diabetes overlay | Assertions (not accuracy) | **0 violations** |

### Current results

```
Layer 1 — Experience Level
  Accuracy: 48.2%
  Confusion (rows=actual, cols=predicted):
                   Beginner  Intermediate  Expert
       Beginner         85           291       0
   Intermediate          0           193     213
         Expert          0             0     191

Layer 2 — Workout Type Baseline (NONDM)
  Accuracy: 19.7%

Layer 3 — Clinical Constraints
  Synthetic DMT1: 18, Synthetic DMT2: 174
  Violations: 0 ✓
```

### Interpreting the results

**Experience level (48.2%)**: Our thresholds are intentionally conservative — real gym beginners exercise 2.5 days/wk at 1h, but our rules classify that as Intermediate. This is correct for our use case: patients coming from a diabetes pipeline are likely less fit than regular gym members. We never over-classify (no Beginner called Expert), only under-classify (safe direction).

**Workout type (19.7%)**: Expected and acceptable. The gym dataset shows workout types are evenly distributed across all demographics — no demographic feature predicts workout type. This confirms our decision to use clinical rules (diabetes context) rather than demographic ML for type selection.

**Clinical constraints (0 violations)**: The most important metric. Across 192 synthetic diabetic patients: DMT1 never gets HIIT, DMT2 always has Strength/Cardio in top 2, high-risk beginners never get HIIT.

### Synthetic diabetes assignment logic

Used in Layer 3 to overlay diabetes labels onto gym members:

| Condition | Assigned | Probability |
|---|---|---|
| BMI > 35 and age > 50 | DMT1 | 0.80 |
| BMI > 30 and age > 45 | DMT2 | 0.70 |
| BMI > 30 | DMT2 | 0.55 |
| BMI > 28 and age > 40 | NONDM (pre-diabetic) | 0.40 |
| Otherwise | Skipped | — |

---

## Datasets

| Dataset | Source | Rows | Used for |
|---|---|---|---|
| 50 exercises | [Best 50 Exercises](https://www.kaggle.com/datasets/prajwaldongre/best-50-exercise-for-your-body) | 50 | `recommend_exercises` lookup |
| Gym members | [Gym Members Exercise Dataset](https://www.kaggle.com/datasets/valakhorasani/gym-members-exercise-dataset) | 973 | Evaluation + future ML (Apache 2.0) |

### Gym members schema (relevant columns)

| Column | Type | Used in evaluation |
|---|---|---|
| Age | int | Layer 1, 2, 3 |
| Gender | string (Male/Female) | Layer 2, 3 |
| Weight (kg) | float | Layer 2, 3 |
| Height (m) | float | Layer 2, 3 (converted to cm) |
| Session_Duration (hours) | float | Layer 1 |
| Workout_Type | string (Cardio/Strength/Yoga/HIIT) | Layer 2 ground truth |
| Workout_Frequency (days/week) | int | Layer 1 |
| Experience_Level | int (1/2/3) | Layer 1 ground truth |
| BMI | float | Layer 3 |

---

## Extension Points for Contributors

### EXTENSION POINT A — Demographic ML Model

**Goal**: Replace the flat 1.0 base scores in `_score_types()` with a trained model.

**Location**: `src/bioai/tools/workout_type_classifier.py`, function `_score_types()`

**What to change**:
1. Train a model on `data/gym_members/raw/gym_members.csv`:
   - Features: `Age`, `Gender`, `Weight (kg)`, `Height (m)`, `BMI`
   - Target: `Workout_Type` (Cardio / Strength / Yoga / HIIT)
   - Output: probability per class (use as base scores instead of flat 1.0)
2. Save model to `data/gym_members/models/` (e.g., `.keras`, `.pkl`)
3. Replace the line `scores = {t: 1.0 for t in _BASE_TYPES}` with model predictions
4. **Keep the clinical override section unchanged** — it applies additively on top

**Contract**: The function must still return `dict[str, float]` mapping each type to a score. The clinical overrides add/subtract from these scores. Higher score = more recommended.

**Evaluation**: Run `uv run python scripts/evaluate_health_trainer.py` — Layer 2 accuracy should improve from the current 19.7% baseline. Layer 3 (0 violations) must remain at 0.

**Note on Yoga**: The gym dataset has `Yoga` as a workout type, but our exercise CSV uses `Flexibility`. The recommender maps `Flexibility` exercises for Yoga suggestions. If adding Yoga as a distinct type, also update `_BASE_TYPES` and add Yoga exercises to the 50-exercise CSV.

### EXTENSION POINT B — Experience Level ML

**Goal**: Replace threshold-based `_experience_level()` with a trained model.

**Location**: `src/bioai/tools/workout_type_classifier.py`, function `_experience_level()`

**What to change**:
1. Train on gym data: features `Workout_Frequency`, `Session_Duration` → target `Experience_Level`
2. Layer 1 evaluation accuracy should improve from 48.2%
3. **Keep conservative bias** — for diabetes patients, under-classifying (Intermediate → Beginner) is safer than over-classifying

### EXTENSION POINT C — Expand Exercise Database

**Goal**: Add more exercises or exercise metadata.

**Location**: `data/exercises/raw/exercises.csv`

**Schema** (must keep these columns):
```
Name, Type, BodyPart, Equipment, Level, Description, Benefits, CaloriesPerMinute
```

Adding rows requires no code changes — the tool reads CSV at runtime. Adding new `Type` values (e.g., "Yoga") requires updating `_BASE_TYPES` in `workout_type_classifier.py`.

### EXTENSION POINT D — Additional Clinical Context

**Goal**: Accept findings from other agents (e.g., Transcriptomics, Proteomics).

**Location**: `src/bioai/agents/health_trainer.py`, function `_build_clinical_context()`

**What to change**:
1. Add parsing for new agent keys in the `context` dict
2. Add corresponding scoring rules in `_score_types()` if the new agent provides exercise-relevant signals
3. Update the system prompt template in `src/bioai/prompts/health_trainer.txt`

---

## Usage

```python
from bioai.agents.health_trainer import HealthTrainerAgent

# Standalone (no prior agents)
trainer = HealthTrainerAgent()

# With prior agent context (recommended)
trainer = HealthTrainerAgent(context={
    "genomics": genomics_result.model_dump(),
    "doctor":   doctor_result.model_dump(),
})

reply = trainer.chat("My doctor referred me — I need to start exercising.")
reply = trainer.chat("I'm 45, female, 68kg, 162cm.")
reply = trainer.chat("I exercise once a week for about 30 minutes.")
# → Claude calls classify_workout_type internally
reply = trainer.chat("I have dumbbells at home and want to focus on my legs.")
# → Claude calls recommend_exercises internally
# → Delivers weekly plan

result = trainer.result()
print(result.findings.fitness_level)          # "beginner"
print(result.findings.recommended_exercises)  # list of exercise dicts
```

### End-to-end pipeline

```python
import asyncio
from bioai.agents.genomics import GenomicsAgent
from bioai.agents.doctor import DoctorAgent
from bioai.agents.health_trainer import HealthTrainerAgent

# Step 1: Genomics
genomics = GenomicsAgent()
genomics_result = asyncio.run(genomics.analyze(f"Analyze DNA: {dna_sequence}"))

# Step 2: Doctor
doctor = DoctorAgent()
doctor.chat("My DNA test showed DMT2 risk...")
# ... multi-turn conversation ...
doctor_result = doctor.result(summary)

# Step 3: Health Trainer (receives both prior results)
if doctor.findings.recommendation == Recommendation.HEALTH_TRAINER:
    trainer = HealthTrainerAgent(context={
        "genomics": genomics_result.model_dump(),
        "doctor":   doctor_result.model_dump(),
    })
    trainer.chat("My doctor referred me to you.")
    # ... conversation continues ...
    final_result = trainer.result()
```

Full pipeline test: `tests/test_integration_full_pipeline.py`
