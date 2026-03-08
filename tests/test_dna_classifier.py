"""Tests for the DNA classifier tool."""

from bioai.tools.dna_classifier import _load_model, _load_tokenizer


def test_load_model():
    model = _load_model()
    assert model is not None
    # Expect 3-class output (DMT1, DMT2, NONDM)
    assert model.output_shape == (None, 3)
