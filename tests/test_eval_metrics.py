"""Tests for deterministic evaluation metrics."""

from bioai.eval.cases import EvalCase, ExpectedOutput
from bioai.eval.metrics import MetricResult, score_decision, score_tool_accuracy
from bioai.models import (
    AgentResult,
    AgentStatus,
    DoctorFindings,
    GenomicsFindings,
    Recommendation,
    RiskLevel,
)


def _genomics_result(predicted_class: str = "DMT2") -> AgentResult:
    return AgentResult(
        agent="genomics",
        status=AgentStatus.SUCCESS,
        findings=GenomicsFindings(
            predicted_class=predicted_class,
            confidence=0.85,
            probabilities={"DMT1": 0.05, "DMT2": 0.85, "NONDM": 0.10},
            risk_level=RiskLevel.HIGH,
            interpretation="High risk for Type 2.",
        ),
        summary="DMT2 detected.",
    )


def _doctor_result(prediction: str = "Diabetic") -> AgentResult:
    return AgentResult(
        agent="doctor",
        status=AgentStatus.SUCCESS,
        findings=DoctorFindings(
            prediction=prediction,
            probability=0.74,
            risk_level=RiskLevel.HIGH if prediction == "Diabetic" else RiskLevel.LOW,
            recommendation=(
                Recommendation.HOSPITAL
                if prediction == "Diabetic"
                else Recommendation.HEALTH_TRAINER
            ),
            reasoning="Based on clinical features.",
        ),
        summary=f"Patient is {prediction}.",
    )


def _case(
    dna_class: str = "DMT2",
    clinical_prediction: str = "Diabetic",
    decision: str = "hospital",
) -> EvalCase:
    return EvalCase(
        id="test",
        name="test",
        description="test",
        expected=ExpectedOutput(
            dna_class=dna_class,
            clinical_prediction=clinical_prediction,
            decision=decision,
        ),
    )


# -- Layer 1: Tool accuracy --------------------------------------------------


class TestToolAccuracy:
    def test_genomics_correct(self):
        result = score_tool_accuracy(_genomics_result("DMT2"), _case(dna_class="DMT2"))
        assert result.score == 1.0
        assert result.passed

    def test_genomics_wrong(self):
        result = score_tool_accuracy(
            _genomics_result("NONDM"), _case(dna_class="DMT2")
        )
        assert result.score == 0.0
        assert not result.passed

    def test_doctor_correct(self):
        result = score_tool_accuracy(
            _doctor_result("Diabetic"), _case(clinical_prediction="Diabetic")
        )
        assert result.score == 1.0
        assert result.passed

    def test_doctor_wrong(self):
        result = score_tool_accuracy(
            _doctor_result("Non-Diabetic"), _case(clinical_prediction="Diabetic")
        )
        assert result.score == 0.0
        assert not result.passed

    def test_error_agent(self):
        error_result = AgentResult(
            agent="genomics",
            status=AgentStatus.ERROR,
            summary="",
            error="Model not found",
        )
        result = score_tool_accuracy(error_result, _case())
        assert result.score == 0.0
        assert not result.passed


# -- Layer 3: Decision correctness -------------------------------------------


class TestDecisionCorrectness:
    def test_hospital_confirmed(self):
        """DMT2 + Diabetic → hospital."""
        result = score_decision(
            _genomics_result("DMT2"),
            _doctor_result("Diabetic"),
            _case(dna_class="DMT2", clinical_prediction="Diabetic", decision="hospital"),
        )
        assert result.score == 1.0
        assert result.passed

    def test_hospital_dna_override(self):
        """DMT2 + Non-Diabetic → hospital (DNA override)."""
        result = score_decision(
            _genomics_result("DMT2"),
            _doctor_result("Non-Diabetic"),
            _case(decision="hospital"),
        )
        assert result.score == 1.0

    def test_reconsider(self):
        """NONDM + Diabetic → reconsider."""
        result = score_decision(
            _genomics_result("NONDM"),
            _doctor_result("Diabetic"),
            _case(decision="reconsider"),
        )
        assert result.score == 1.0

    def test_health_trainer(self):
        """NONDM + Non-Diabetic → health_trainer."""
        result = score_decision(
            _genomics_result("NONDM"),
            _doctor_result("Non-Diabetic"),
            _case(decision="health_trainer"),
        )
        assert result.score == 1.0

    def test_wrong_decision(self):
        """DMT2 + Diabetic should be hospital, not health_trainer."""
        result = score_decision(
            _genomics_result("DMT2"),
            _doctor_result("Diabetic"),
            _case(decision="health_trainer"),
        )
        assert result.score == 0.0
        assert not result.passed
