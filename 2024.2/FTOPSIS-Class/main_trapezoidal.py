from ftopsis_class import CriteriaType
from ftopsis_class import FTOPSISClass as ft
import numpy as np
import pandas as pd

def main():
    # Variáveis Linguísticas para avaliação alternativas
    VL = np.array([0.0, 0.0, 0.1, 0.2])  # Muito Ruim
    L = np.array([0.1, 0.2, 0.3, 0.4])   # Ruim
    M = np.array([0.3, 0.4, 0.5, 0.6])   # Medio
    H = np.array([0.5, 0.6, 0.7, 0.8])   # Bom
    VH = np.array([0.7, 0.8, 0.9, 1.0])  # Muito Bom

    # Variáveis Linguísticas dos pesos dos critérios
    U = np.array([0.0, 0.0, 0.1, 0.2])   # Nada Importante
    MI = np.array([0.1, 0.2, 0.3, 0.4])  # Pouco Importante
    I = np.array([0.3, 0.4, 0.5, 0.6])   # Importancia Media
    VI = np.array([0.5, 0.6, 0.7, 0.8])  # Importante
    EI = np.array([0.7, 0.8, 0.9, 1.0])  # Muito Importante

    # Matriz de decisão
    dados_matriz_decisao = {
        "C1": [VL, VL, L, L, M, M, H, H, VH, VH],
        'C2': [VL, VL, VL, VL, VL, VL, H, L, VL, VH],
        'C3': [H, VH, H, VH, VH, VH, VH, VL, VH, L],
        'C4': [VL, VL, L, L, M, M, H, H, VH, VH],
        'C5': [VH, VH, H, H, M, M, L, L, VL, VL],
        'C6': [VL, VL, L, L, M, M, H, H, VH, VH],
        'C7': [M, M, M, M, VH, VH, VH, H, H, VH]
    }
    matriz_decisao = pd.DataFrame(dados_matriz_decisao)

    # Matriz de perfil
    dados_perfil = {
        "C1": [L, L, H, VH],
        'C2': [VL, VL, VL, VL],
        'C3': [VL, L, H, VH],
        'C4': [VL, L, H, VH],
        'C5': [VH, H, L, VL],
        'C6': [VL, L, H, VH],
        'C7': [H, H, L, VL]
    }
    matriz_perfil = pd.DataFrame(dados_perfil)

    mapeamento_perfil = {0: 'Conservative', 1: 'Moderate', 2: 'Bold', 3: 'Agressive'}

    # Pesos dos critérios
    pesos = {
        "C1": [VI], "C2": [VI], "C3": [VI], 
        "C4": [VI], "C5": [VI], "C6": [VI], "C7": [VI]
    }
    pesos = pd.DataFrame(pesos)

    # Tipo de critério
    tipo_criterio = {
        "C1": CriteriaType.Benefit,
        "C2": CriteriaType.Benefit,
        "C3": CriteriaType.Benefit,
        "C4": CriteriaType.Benefit,
        "C5": CriteriaType.Benefit,
        "C6": CriteriaType.Benefit,
        "C7": CriteriaType.Benefit
    }

    # Processamento FTOPSIS
    matriz_normalizada = ft.normalize_matrix(matriz_decisao, tipo_criterio)
    matriz_ponderada = ft.weigh_matrix(matriz_normalizada, pesos)
    matriz_decisao_normalizada_ponderada = ft.round_weighted_normalized_matrix(matriz_ponderada)

    matriz_perfil_normalizada = ft.normalize_matrix(matriz_perfil, tipo_criterio)
    matriz_perfil_ponderada = ft.weigh_matrix(matriz_perfil_normalizada, pesos)
    matriz_perfil_normalizada_ponderada = ft.round_weighted_normalized_matrix(matriz_perfil_ponderada)

    solucao_ideal_positiva, solucao_ideal_negativa = ft.ideal_solution(
        matriz_perfil_normalizada_ponderada, mapeamento_perfil
    )

    distancia_positiva, distancia_neagtiva = ft.distance_calculation(
        matriz_decisao_normalizada_ponderada, solucao_ideal_positiva, solucao_ideal_negativa
    )

    resultado = ft.proximity_coefficient(distancia_positiva, distancia_neagtiva)

    # Nomes dos fornecedores
    fornecedores = [
        "F1", "F2", "F3", "F4",
        "F5", "F6", "F7", "F8", 
        "F9", "F10"
    ]
    resultado.index = fornecedores

    # Exibir resultados
    print("Resultado da avaliação FTOPSIS:")
    print(resultado)

if __name__ == "__main__":
    main()