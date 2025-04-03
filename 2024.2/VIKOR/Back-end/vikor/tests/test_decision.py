# tests/test_decision.py

from __future__ import annotations
import pytest
from typing import List, Tuple
from vikor.models import Alternative, Criterion
from vikor.decision import Vikor
from vikor.exceptions import VikorError

def create_sample_data() -> Tuple[List[Alternative], List[Criterion]]:
    alt1 = Alternative("A1", {"Custo": 100, "Qualidade": 80})
    alt2 = Alternative("A2", {"Custo": 110, "Qualidade": 90})
    alt3 = Alternative("A3", {"Custo": 90, "Qualidade": 70})
    crit1 = Criterion("Custo", 0.4, is_benefit=False)
    crit2 = Criterion("Qualidade", 0.6, is_benefit=True)
    return [alt1, alt2, alt3], [crit1, crit2]

def test_vikor_evaluate_default_v() -> None:
    alternatives, criteria = create_sample_data()
    vikor_obj = Vikor(alternatives, criteria, v=0.5)
    q_scores = vikor_obj.evaluate()
    # Verifica se todas as alternativas foram avaliadas e se os valores são floats.
    assert set(q_scores.keys()) == {alt.name for alt in alternatives}
    for q in q_scores.values():
        assert isinstance(q, float)

def test_vikor_evaluate_v_extremes() -> None:
    alternatives, criteria = create_sample_data()
    # Testa v = 0 (prioriza R)
    q_scores_v0 = Vikor(alternatives, criteria, v=0.0).evaluate()
    for q in q_scores_v0.values():
        assert isinstance(q, float)
    # Testa v = 1 (prioriza S)
    q_scores_v1 = Vikor(alternatives, criteria, v=1.0).evaluate()
    for q in q_scores_v1.values():
        assert isinstance(q, float)

def test_vikor_identical_scores() -> None:
    # Alternativas com scores idênticos devem ter Q iguais
    alt1 = Alternative("A1", {"Custo": 100, "Qualidade": 80})
    alt2 = Alternative("A2", {"Custo": 100, "Qualidade": 80})
    crit1 = Criterion("Custo", 0.5, is_benefit=False)
    crit2 = Criterion("Qualidade", 0.5, is_benefit=True)
    vikor_obj = Vikor([alt1, alt2], [crit1, crit2], v=0.5)
    q_scores = vikor_obj.evaluate()
    assert q_scores["A1"] == q_scores["A2"]

def test_vikor_invalid_v_parameter() -> None:
    alternatives, criteria = create_sample_data()
    with pytest.raises(VikorError):
        Vikor(alternatives, criteria, v=-0.1)
    with pytest.raises(VikorError):
        Vikor(alternatives, criteria, v=1.1)

def test_vikor_empty_alternatives() -> None:
    _, criteria = create_sample_data()
    with pytest.raises(VikorError):
        Vikor([], criteria, v=0.5)

def test_vikor_empty_criteria() -> None:
    alternatives, _ = create_sample_data()
    with pytest.raises(VikorError):
        Vikor(alternatives, [], v=0.5)

def test_vikor_missing_score() -> None:
    alt1 = Alternative("A1", {"Custo": 100})  # Falta "Qualidade"
    crit1 = Criterion("Custo", 0.5, is_benefit=False)
    crit2 = Criterion("Qualidade", 0.5, is_benefit=True)
    with pytest.raises(VikorError):
        Vikor([alt1], [crit1, crit2], v=0.5).evaluate()
