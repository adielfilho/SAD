from typing import Dict, List

def invert_matrix(label_1: List[str], label_2: List[str], matrix: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Inverte a matriz.

    Args:
        label_1: Lista de elementos (ex: ["F1", "F2", ..., "F10"]).
        label_2: Lista de critérios (ex: ["C1", "C2", ..., "C7"]).
        matrix: Dicionário onde cada chave é um critério e o valor é uma lista de termos.

    Returns:
        Um dicionário no formato {"F1": ["VL", "VL", ...], "F2": [...], ...}.

    Raises:
        KeyError: Se algum critério não estiver presente na matriz.
        ValueError: Se o tamanho das listas de termos for inconsistente.
    """

    missing_label_2 = [c for c in label_2 if c not in matrix]
    if missing_label_2:
        raise KeyError(f"Critérios faltando na matriz: {missing_label_2}")
    
    expected_length = len(label_1)
    for criterion in label_2:
        actual_length = len(matrix[criterion])
        if actual_length != expected_length:
            raise ValueError(f"Critério '{criterion}' tem {actual_length} termos, mas deveria ter {expected_length}.")
    
    fuzzy_decision_matrix = {}
    for i, tag in enumerate(label_1):
        fuzzy_decision_matrix[tag] = [
            matrix[criterion][i]
            for criterion in label_2
        ]
    
    return fuzzy_decision_matrix