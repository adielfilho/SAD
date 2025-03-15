# tests/test_models.py

from __future__ import annotations
import pytest
from vikor.models import Alternative, Criterion

def test_alternative_creation_valid() -> None:
    alt = Alternative("A1", {"Custo": 100, "Qualidade": 80})
    assert alt.name == "A1"
    assert alt.scores == {"Custo": 100, "Qualidade": 80}

def test_alternative_defensive_copy() -> None:
    original = {"Custo": 100, "Qualidade": 80}
    alt = Alternative("A1", original)
    original["Custo"] = 200  # Modifica o dicionário original
    # A alteração não deve afetar a instância
    assert alt.scores["Custo"] == 100

def test_alternative_repr() -> None:
    alt = Alternative("A1", {"Custo": 100})
    rep = repr(alt)
    assert "Alternative(" in rep

def test_alternative_equality_and_hash() -> None:
    alt1 = Alternative("A1", {"Custo": 100})
    alt2 = Alternative("A1", {"Custo": 100})
    alt3 = Alternative("A1", {"Custo": 200})
    assert alt1 == alt2
    assert alt1 != alt3
    assert hash(alt1) == hash(alt2)
    assert hash(alt1) != hash(alt3)

def test_alternative_invalid_name() -> None:
    with pytest.raises(TypeError):
        Alternative(123, {"Custo": 100})

def test_alternative_invalid_scores_type() -> None:
    with pytest.raises(TypeError):
        Alternative("A1", "não é um dicionário")

def test_alternative_invalid_score_key() -> None:
    with pytest.raises(TypeError):
        Alternative("A1", {1: 100})

def test_alternative_invalid_score_value() -> None:
    with pytest.raises(TypeError):
        Alternative("A1", {"Custo": "100"})

def test_criterion_creation_valid() -> None:
    crit = Criterion("Custo", 0.5, is_benefit=False)
    assert crit.name == "Custo"
    assert crit.weight == 0.5
    assert crit.is_benefit is False

def test_criterion_repr() -> None:
    crit = Criterion("Custo", 0.5, is_benefit=False)
    rep = repr(crit)
    assert "Criterion(" in rep

def test_criterion_equality_and_hash() -> None:
    crit1 = Criterion("Custo", 0.5, is_benefit=False)
    crit2 = Criterion("Custo", 0.5, is_benefit=False)
    crit3 = Criterion("Custo", 1.0, is_benefit=False)
    assert crit1 == crit2
    assert crit1 != crit3
    assert hash(crit1) == hash(crit2)
    assert hash(crit1) != hash(crit3)

def test_criterion_invalid_name() -> None:
    with pytest.raises(TypeError):
        Criterion(123, 0.5)

def test_criterion_invalid_weight_type() -> None:
    with pytest.raises(TypeError):
        Criterion("Custo", "0.5")

def test_criterion_negative_weight() -> None:
    with pytest.raises(ValueError):
        Criterion("Custo", -0.5)

def test_criterion_invalid_is_benefit() -> None:
    with pytest.raises(TypeError):
        Criterion("Custo", 0.5, is_benefit="False")
