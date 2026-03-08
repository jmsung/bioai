"""Ralph Loop — iterative prompt optimizer (v1)."""

from pathlib import Path

import anthropic
from pydantic import BaseModel

from bioai.config import Settings

_REWRITE_SYSTEM = """\
You are an expert prompt engineer for biomedical AI agents.

Given an agent's current system prompt and its evaluation scores, rewrite the prompt
to improve the weakest metric. Keep the prompt's core purpose and tool-calling
instructions intact. Only change phrasing, emphasis, or add guidance that addresses
the specific weakness.

Return ONLY the rewritten prompt text — no explanation, no markdown fences.
"""


class RalphResult(BaseModel):
    """Result of a single Ralph Loop iteration."""

    agent: str
    metric: str
    old_score: float
    new_score: float = 0.0  # filled after re-eval
    prompt_changed: bool
    diff: str  # description of what changed


def _find_weakest(
    eval_scores: dict[str, dict[str, float]],
) -> tuple[str, str, float]:
    """Find the agent + metric with the lowest score.

    Returns (agent_name, metric_name, score).
    """
    worst_agent, worst_metric, worst_score = "", "", float("inf")
    for agent, scores in eval_scores.items():
        for metric, score in scores.items():
            if score < worst_score:
                worst_agent, worst_metric, worst_score = agent, metric, score
    return worst_agent, worst_metric, worst_score


async def ralph_iterate(
    eval_scores: dict[str, dict[str, float]],
    prompt_dir: Path | None = None,
    settings: Settings | None = None,
) -> RalphResult:
    """Run one Ralph Loop iteration: find weakest → rewrite prompt."""
    settings = settings or Settings.from_env()
    prompt_dir = prompt_dir or settings.prompts_dir

    agent_name, metric_name, score = _find_weakest(eval_scores)
    prompt_file = prompt_dir / f"{agent_name}.txt"

    if not prompt_file.exists():
        return RalphResult(
            agent=agent_name,
            metric=metric_name,
            old_score=score,
            prompt_changed=False,
            diff=f"No prompt file found at {prompt_file}",
        )

    current_prompt = prompt_file.read_text()

    try:
        client = anthropic.Anthropic(api_key=settings.api_key)
        response = client.messages.create(
            model=settings.ralph_model,
            max_tokens=2048,
            system=_REWRITE_SYSTEM,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"## Agent: {agent_name}\n"
                        f"## Weakest metric: {metric_name} (score: {score})\n"
                        f"## All scores: {eval_scores[agent_name]}\n\n"
                        f"## Current prompt:\n{current_prompt}"
                    ),
                }
            ],
        )
        new_prompt = response.content[0].text.strip()
        prompt_file.write_text(new_prompt + "\n")

        return RalphResult(
            agent=agent_name,
            metric=metric_name,
            old_score=score,
            prompt_changed=True,
            diff=f"Rewrote {prompt_file.name} to improve {metric_name}",
        )
    except Exception as e:
        return RalphResult(
            agent=agent_name,
            metric=metric_name,
            old_score=score,
            prompt_changed=False,
            diff=f"Rewrite failed: {e}",
        )
