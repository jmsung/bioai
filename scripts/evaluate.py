"""Evaluation CLI — score agents and optionally run Ralph Loop.

Usage:
    uv run python scripts/evaluate.py              # real mode
    uv run python scripts/evaluate.py --mock       # mock mode (pre-recorded outputs)
    uv run python scripts/evaluate.py --save       # real mode + save outputs for mock
    uv run python scripts/evaluate.py --ralph --iter 3  # Ralph Loop, 3 iterations
"""

import argparse
import asyncio
import json
from pathlib import Path

from bioai.config import Settings
from bioai.eval.cases import EvalCase, load_cases
from bioai.eval.judge import JudgeScore, judge_agent
from bioai.eval.metrics import MetricResult, score_decision, score_tool_accuracy
from bioai.eval.ralph import ralph_iterate
from bioai.models import AgentResult

MOCK_DIR = Path("src/bioai/eval/data/mock_outputs")


# -- Agent runners (real mode) ------------------------------------------------


async def run_genomics(case: EvalCase, settings: Settings) -> AgentResult:
    """Run Genomics agent on a test case."""
    from bioai.agents.genomics import GenomicsAgent

    agent = GenomicsAgent()
    return await agent.analyze(case.dna_sequence or "")


async def run_doctor(case: EvalCase, settings: Settings) -> AgentResult:
    """Run Doctor agent on a test case."""
    from bioai.agents.doctor import DoctorAgent

    agent = DoctorAgent()
    if case.clinical_features:
        # Direct feature input — single turn
        feature_str = ", ".join(f"{k}={v}" for k, v in case.clinical_features.items())
        agent.chat(f"My clinical values: {feature_str}")
    elif case.patient_description:
        agent.chat(case.patient_description)
    return agent.result(summary="Evaluation run")


# -- Mock I/O ----------------------------------------------------------------


def save_outputs(
    case: EvalCase, results: dict[str, AgentResult], mock_dir: Path
) -> None:
    """Save agent outputs for mock mode."""
    case_dir = mock_dir / case.id
    case_dir.mkdir(parents=True, exist_ok=True)
    for agent_name, result in results.items():
        (case_dir / f"{agent_name}.json").write_text(result.model_dump_json(indent=2))


def load_outputs(case: EvalCase, mock_dir: Path) -> dict[str, AgentResult]:
    """Load pre-recorded agent outputs."""
    case_dir = mock_dir / case.id
    results = {}
    for path in case_dir.glob("*.json"):
        data = json.loads(path.read_text())
        results[path.stem] = AgentResult.model_validate(data)
    return results


# -- Eval runner --------------------------------------------------------------


async def evaluate_case(
    case: EvalCase,
    settings: Settings,
    mock: bool = False,
    save: bool = False,
) -> dict:
    """Evaluate a single test case. Returns dict of metric results."""
    # Get agent outputs
    if mock:
        outputs = load_outputs(case, MOCK_DIR)
        genomics_result = outputs.get("genomics")
        doctor_result = outputs.get("doctor")
    else:
        genomics_result = await run_genomics(case, settings)
        doctor_result = await run_doctor(case, settings)

    if save and not mock:
        results_dict = {}
        if genomics_result:
            results_dict["genomics"] = genomics_result
        if doctor_result:
            results_dict["doctor"] = doctor_result
        save_outputs(case, results_dict, MOCK_DIR)

    # Layer 1: Tool accuracy
    metrics: list[MetricResult] = []
    if genomics_result:
        metrics.append(score_tool_accuracy(genomics_result, case))
    if doctor_result:
        metrics.append(score_tool_accuracy(doctor_result, case))

    # Layer 3: Decision correctness
    if genomics_result and doctor_result:
        metrics.append(score_decision(genomics_result, doctor_result, case))

    # Layer 2: LLM-as-judge (skip in mock unless judge is also mocked)
    judge_scores: dict[str, JudgeScore] = {}
    if not mock:
        for agent_result in [genomics_result, doctor_result]:
            if agent_result:
                judge_scores[agent_result.agent] = await judge_agent(
                    agent_result, case, settings
                )

    return {
        "case": case.id,
        "metrics": metrics,
        "judge_scores": judge_scores,
    }


def print_report(results: list[dict]) -> None:
    """Print a summary report to stdout."""
    print("\n" + "=" * 60)
    print("EVALUATION REPORT")
    print("=" * 60)

    for result in results:
        print(f"\n--- {result['case']} ---")
        for m in result["metrics"]:
            status = "PASS" if m.passed else "FAIL"
            print(f"  [{status}] {m.agent}/{m.metric}: {m.score:.1f} — {m.detail}")
        for agent, js in result.get("judge_scores", {}).items():
            print(
                f"  [JUDGE] {agent}: "
                f"rel={js.relevance} comp={js.completeness} "
                f"acc={js.accuracy} safe={js.safety}"
            )
            print(f"          {js.explanation}")

    # Summary
    all_metrics = [m for r in results for m in r["metrics"]]
    passed = sum(1 for m in all_metrics if m.passed)
    total = len(all_metrics)
    print(f"\n{'=' * 60}")
    print(f"TOTAL: {passed}/{total} metrics passed")
    print("=" * 60)


def collect_judge_averages(results: list[dict]) -> dict[str, dict[str, float]]:
    """Aggregate judge scores per agent for Ralph Loop input."""
    agent_scores: dict[str, dict[str, list[float]]] = {}
    for result in results:
        for agent, js in result.get("judge_scores", {}).items():
            if agent not in agent_scores:
                agent_scores[agent] = {
                    "relevance": [],
                    "completeness": [],
                    "accuracy": [],
                    "safety": [],
                }
            agent_scores[agent]["relevance"].append(js.relevance)
            agent_scores[agent]["completeness"].append(js.completeness)
            agent_scores[agent]["accuracy"].append(js.accuracy)
            agent_scores[agent]["safety"].append(js.safety)

    return {
        agent: {m: sum(v) / len(v) for m, v in scores.items()}
        for agent, scores in agent_scores.items()
    }


async def main():
    parser = argparse.ArgumentParser(description="BioAI Evaluation")
    parser.add_argument("--mock", action="store_true", help="Use pre-recorded outputs")
    parser.add_argument(
        "--save", action="store_true", help="Save agent outputs for mock mode"
    )
    parser.add_argument("--ralph", action="store_true", help="Run Ralph Loop")
    parser.add_argument(
        "--iter", type=int, default=3, help="Ralph Loop iterations (default: 3)"
    )
    args = parser.parse_args()

    settings = Settings.from_env()
    cases = load_cases()

    # Run evaluation
    results = []
    for case in cases:
        result = await evaluate_case(case, settings, mock=args.mock, save=args.save)
        results.append(result)

    print_report(results)

    # Ralph Loop
    if args.ralph:
        avg_scores = collect_judge_averages(results)
        if not avg_scores:
            print("\nNo judge scores available for Ralph Loop. Run without --mock.")
            return

        print(f"\nStarting Ralph Loop ({args.iter} iterations)...")
        for i in range(args.iter):
            print(f"\n--- Ralph iteration {i + 1} ---")
            ralph_result = await ralph_iterate(avg_scores, settings=settings)
            print(
                f"  Target: {ralph_result.agent}/{ralph_result.metric} "
                f"(score: {ralph_result.old_score:.1f})"
            )
            print(f"  Changed: {ralph_result.prompt_changed}")
            print(f"  Detail: {ralph_result.diff}")

            if ralph_result.prompt_changed:
                # Re-run eval to get new scores
                results = []
                for case in cases:
                    result = await evaluate_case(case, settings)
                    results.append(result)
                print_report(results)
                avg_scores = collect_judge_averages(results)


if __name__ == "__main__":
    asyncio.run(main())
