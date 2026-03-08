# Gym Members Exercise Dataset

Source: [Gym Members Exercise Dataset](https://www.kaggle.com/datasets/valakhorasani/gym-members-exercise-dataset) — Kaggle (Apache 2.0)

## Schema

| Column | Type | Description |
|---|---|---|
| Age | int | Member age in years |
| Gender | string | Male / Female |
| Weight (kg) | float | Body weight in kilograms |
| Height (m) | float | Height in metres |
| Max_BPM | int | Maximum heart rate during workout |
| Avg_BPM | int | Average heart rate during workout |
| Resting_BPM | int | Resting heart rate before workout |
| Session_Duration (hours) | float | Workout session length in hours |
| Calories_Burned | float | Calories burned per session |
| Workout_Type | string | Cardio / Strength / Yoga / HIIT |
| Fat_Percentage | float | Body fat percentage |
| Water_Intake (liters) | float | Daily water intake |
| Workout_Frequency (days/week) | int | Sessions per week |
| Experience_Level | int | 1=Beginner, 2=Intermediate, 3=Expert |
| BMI | float | Body Mass Index |

## Stats

- 973 rows
- Workout_Type distribution: Cardio / Strength / Yoga / HIIT (roughly balanced)
- Experience_Level: 1 (Beginner), 2 (Intermediate), 3 (Expert)

## Used by

`scripts/evaluate_health_trainer.py` — calibration and evaluation of `classify_workout_type()` rules.
