from typing import Dict, List

def invert_matrix(elements: List[str], criteria: List[str], decision_matrix_by_criteria: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Inverte a matriz de decisão por critério para uma matriz fuzzy (por elemento), validando os dados.

    Args:
        elements: Lista de elementos (ex: ["F1", "F2", ..., "F10"]).
        criteria: Lista de critérios (ex: ["C1", "C2", ..., "C7"]).
        decision_matrix_by_criteria: Dicionário onde cada chave é um critério e o valor é uma lista de termos.

    Returns:
        Um dicionário no formato {"F1": ["VL", "VL", ...], "F2": [...], ...}.

    Raises:
        KeyError: Se algum critério não estiver presente na matriz.
        ValueError: Se o tamanho das listas de termos for inconsistente.
    """
    # Verificar se todos os critérios existem
    missing_criteria = [c for c in criteria if c not in decision_matrix_by_criteria]
    if missing_criteria:
        raise KeyError(f"Critérios faltando na matriz: {missing_criteria}")
    
    # Verificar o tamanho das listas de termos
    expected_length = len(elements)
    for criterion in criteria:
        actual_length = len(decision_matrix_by_criteria[criterion])
        if actual_length != expected_length:
            raise ValueError(f"Critério '{criterion}' tem {actual_length} termos, mas deveria ter {expected_length}.")
    
    # Inverter a matriz
    fuzzy_decision_matrix = {}
    for i, element in enumerate(elements):
        fuzzy_decision_matrix[element] = [
            decision_matrix_by_criteria[criterion][i]
            for criterion in criteria
        ]
    
    return fuzzy_decision_matrix