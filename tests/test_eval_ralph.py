"""Tests for Ralph Loop prompt optimizer."""

import asyncio
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from bioai.eval.ralph import RalphResult, ralph_iterate


def _mock_rewrite_response(new_prompt: str) -> MagicMock:
    block = MagicMock()
    block.type = "text"
    block.text = new_prompt

    response = MagicMock()
    response.content = [block]
    return response


def _mock_judge_response(scores: dict) -> MagicMock:
    block = MagicMock()
    block.type = "text"
    block.text = json.dumps(scores)

    response = MagicMock()
    response.content = [block]
    return response


@patch("bioai.eval.ralph.anthropic.Anthropic")
def test_ralph_iterate_rewrites_prompt(mock_anthropic_cls, tmp_path):
    """Ralph should rewrite the weakest agent's prompt file."""
    # Set up a prompt file
    prompt_file = tmp_path / "doctor.txt"
    prompt_file.write_text("You are a doctor. Ask questions.")

    mock_client = mock_anthropic_cls.return_value
    mock_client.messages.create.return_value = _mock_rewrite_response(
        "You are an expert clinical doctor. Gather all 8 features carefully."
    )

    # Simulate eval results: doctor scored worst on completeness
    eval_scores = {
        "doctor": {"relevance": 4, "completeness": 2, "accuracy": 4, "safety": 5},
        "genomics": {"relevance": 4, "completeness": 4, "accuracy": 5, "safety": 5},
    }

    result = asyncio.run(
        ralph_iterate(
            eval_scores=eval_scores,
            prompt_dir=tmp_path,
        )
    )

    assert isinstance(result, RalphResult)
    assert result.agent == "doctor"
    assert result.metric == "completeness"
    assert result.prompt_changed
    # Prompt file should be updated
    assert "expert clinical doctor" in prompt_file.read_text()


@patch("bioai.eval.ralph.anthropic.Anthropic")
def test_ralph_iterate_skips_missing_prompt(mock_anthropic_cls, tmp_path):
    """If the worst agent has no prompt file, ralph should report no change."""
    eval_scores = {
        "doctor": {"relevance": 5, "completeness": 5, "accuracy": 5, "safety": 5},
        "genomics": {"relevance": 2, "completeness": 2, "accuracy": 2, "safety": 5},
    }

    result = asyncio.run(
        ralph_iterate(
            eval_scores=eval_scores,
            prompt_dir=tmp_path,
        )
    )

    assert not result.prompt_changed
    assert "no prompt file" in result.diff.lower()
