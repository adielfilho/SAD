# tests/test_utils.py

from __future__ import annotations
import pytest

from ..src.vikor_cin import Alternative, Criterion
from ..src.vikor_cin import normalize_value, validate_alternatives_scores
from ..src.vikor_cin import VikorMissingScoreError

def test_normalize_value_standard() -> None:
    # Exemplo: f_star = 100, f_minus = 50, f = 75 → (100 - 75)/(100-50)=25/50 = 0.5
    result = normalize_value(100, 50, 75)
    assert result == 0.5

def test_normalize_value_zero_denominator() -> None:
    # Se f_star == f_minus, denom é 1e-10
    result = normalize_value(100, 100, 90)
    expected = (100 - 90) / 1e-10
    assert result == expected

def test_normalize_value_negative_result() -> None:
    # Se f for maior que f_star para critério de benefício, o resultado será negativo.
    result = normalize_value(80, 50, 90)
    expected = (80 - 90) / (80 - 50)
    assert pytest.approx(result, rel=1e-6) == expected

def test_validate_alternatives_scores_success() -> None:
    alt1 = Alternative("A1", {"Custo": 100, "Qualidade": 80})
    alt2 = Alternative("A2", {"Custo": 110, "Qualidade": 70})
    crit1 = Criterion("Custo", 0.5, is_benefit=False)
    crit2 = Criterion("Qualidade", 0.5, is_benefit=True)
    # Deve passar sem lançar exceção
    validate_alternatives_scores([alt1, alt2], [crit1, crit2])

def test_validate_alternatives_scores_failure() -> None:
    alt1 = Alternative("A1", {"Custo": 100})
    crit1 = Criterion("Custo", 0.5, is_benefit=False)
    crit2 = Criterion("Qualidade", 0.5, is_benefit=True)
    with pytest.raises(VikorMissingScoreError):
        validate_alternatives_scores([alt1], [crit1, crit2])
