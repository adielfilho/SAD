# tests/test_vikor.py

from __future__ import annotations
import pytest
from typing import Any, Dict
from vikor_main import run_vikor_decision 

# Exemplo de entrada válida para o método VIKOR
VALID_INPUT: Dict[str, Any] = {
    "method": "VIKOR",
    "parameters": {
        "alternatives": ["A1", "A2", "A3"],
        "criteria": ["C1", "C2", "C3"],
        "performance_matrix": {
            "A1": [0.7, 0.5, 0.8],
            "A2": [0.6, 0.7, 0.6],
            "A3": [0.8, 0.6, 0.7]
        },
        "criteria_types": {
            "C1": "max",
            "C2": "min",
            "C3": "max"
        },
        "weights": {
            "C1": 0.4,
            "C2": 0.3,
            "C3": 0.3
        },
        "v": 0.5
    }
}

def test_run_vikor_decision_success() -> None:
    """
    Testa a execução bem-sucedida do método VIKOR com entrada válida.
    
    Verifica se o dicionário de resultados contém as chaves esperadas:
      - "method"
      - "results" com subchaves: "scores", "ranking", "compromise_solution",
        "weight_stability" e "distance_to_ideal"
    """
    results = run_vikor_decision(VALID_INPUT)
    assert results.get("method") == "VIKOR"
    results_dict = results.get("results")
    assert isinstance(results_dict, dict)
    for key in ["scores", "ranking", "compromise_solution", "weight_stability", "distance_to_ideal"]:
        assert key in results_dict

    # Verifica que o ranking contenha todas as alternativas
    ranking = results_dict.get("ranking")
    assert isinstance(ranking, list)
    assert set(ranking) == set(VALID_INPUT["parameters"]["alternatives"])

def test_run_vikor_missing_parameters() -> None:
    """
    Testa que uma entrada com parâmetros incompletos lança ValueError.
    """
    incomplete_input = {
        "method": "VIKOR",
        "parameters": {
            # "alternatives" faltando
            "criteria": ["C1", "C2"],
            "performance_matrix": {"A1": [0.7, 0.5]},
            "criteria_types": {"C1": "max", "C2": "min"},
            "weights": {"C1": 0.6, "C2": 0.4},
            "v": 0.5
        }
    }
    with pytest.raises(ValueError):
        run_vikor_decision(incomplete_input)

def test_run_vikor_incorrect_performance_matrix() -> None:
    """
    Testa que, se o número de valores na performance_matrix para uma alternativa não corresponder
    ao número de critérios, um ValueError é lançado.
    """
    bad_perf_input = {
        "method": "VIKOR",
        "parameters": {
            "alternatives": ["A1", "A2"],
            "criteria": ["C1", "C2", "C3"],
            "performance_matrix": {
                # A1 possui apenas 2 valores, mas deveriam ser 3
                "A1": [0.7, 0.5],
                "A2": [0.6, 0.7, 0.6]
            },
            "criteria_types": {"C1": "max", "C2": "min", "C3": "max"},
            "weights": {"C1": 0.4, "C2": 0.3, "C3": 0.3},
            "v": 0.5
        }
    }
    with pytest.raises(ValueError):
        run_vikor_decision(bad_perf_input)

def test_run_vikor_invalid_criteria_type() -> None:
    """
    Testa que, se algum critério tiver um tipo inválido (diferente de "max" ou "min"),
    um ValueError é lançado.
    """
    bad_type_input = {
        "method": "VIKOR",
        "parameters": {
            "alternatives": ["A1", "A2", "A3"],
            "criteria": ["C1", "C2", "C3"],
            "performance_matrix": {
                "A1": [0.7, 0.5, 0.8],
                "A2": [0.6, 0.7, 0.6],
                "A3": [0.8, 0.6, 0.7]
            },
            "criteria_types": {"C1": "max", "C2": "invalid", "C3": "max"},
            "weights": {"C1": 0.4, "C2": 0.3, "C3": 0.3},
            "v": 0.5
        }
    }
    with pytest.raises(ValueError):
        run_vikor_decision(bad_type_input)
