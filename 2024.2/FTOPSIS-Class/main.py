from ftopsis_class import CriteriaType
from ftopsis_class import FTOPSISClass as ft
import numpy as np
import pandas as pd

# Variáveis Linguísticas para avaliação das alternativas
MR = np.array([0.0, 0.0, 2.5])  # Muito Ruim
R = np.array([0.0, 2.5, 5.0])   # Ruim
M = np.array([2.5, 5.0, 7.5])   # Médio
B = np.array([5.0, 7.5, 10.0])  # Bom
MB = np.array([7.5, 10.0, 10.0]) # Muito Bom

# Variáveis Linguísticas dos pesos dos critérios
NI = np.array([0.2, 0.2, 0.4])  # Nada Importante
PI = np.array([0.2, 0.4, 0.6])  # Pouco Importante
IM = np.array([0.4, 0.6, 0.8])  # Importância Média
I = np.array([0.6, 0.8, 1.0])   # Importante
MI = np.array([0.8, 0.8, 1.0])  # Muito Importante

# Matriz de Decisão
dados_matriz_decisao = {
    "C1": [MB, B, M, R, MR, MB, MB, R, B],
    'C2': [MB, B, M, R, MR, R, MR, B, MR],
    'C3': [MB, B, M, R, MR, B, B, B, R],
    'C4': [MB, B, M, R, MR, MB, MB, B, MB]
}
matriz_decisao = pd.DataFrame(dados_matriz_decisao)

# Matriz de Perfil
dados_perfil = {
    "C1": [MB, B, R],
    'C2': [B, M, R],
    'C3': [B, M, MR],
    'C4': [MB, B, M]
}
matriz_perfil = pd.DataFrame(dados_perfil)

mapeamento_perfil = {0: 'Preferível', 1: 'Aceitável', 2: 'Inaceitável'}

# Pesos dos Critérios
pesos = {"C1": [I], "C2": [IM], "C3": [IM], "C4": [I]}
pesos = pd.DataFrame(pesos)

# Tipo dos Critérios (Benefício ou Custo)
tipo_criterio = {
    "C1": CriteriaType.Benefit,
    "C2": CriteriaType.Benefit,
    "C3": CriteriaType.Benefit,
    "C4": CriteriaType.Benefit,
}

# Normalização e Ponderação
matriz_normalizada = ft.normalize_matrix(matriz_decisao, tipo_criterio)
matriz_ponderada = ft.weigh_matrix(matriz_normalizada, pesos)
matriz_decisao_normalizada_ponderada = ft.round_weighted_normalized_matrix(matriz_ponderada)

matriz_perfil_normalizada = ft.normalize_matrix(matriz_perfil, tipo_criterio)
matriz_perfil_ponderada = ft.weigh_matrix(matriz_perfil_normalizada, pesos)
matriz_perfil_normalizada_ponderada = ft.round_weighted_normalized_matrix(matriz_perfil_ponderada)

# Soluções Ideais e Distâncias
solucao_ideal_positiva, solucao_ideal_negativa = ft.ideal_solution(matriz_perfil_normalizada_ponderada, mapeamento_perfil)
distancia_positiva, distancia_neagtiva = ft.distance_calculation(matriz_decisao_normalizada_ponderada, solucao_ideal_positiva, solucao_ideal_negativa)

# Cálculo do Coeficiente de Proximidade
resultado = ft.proximity_coefficient(distancia_positiva, distancia_neagtiva)

# Nomes dos Fornecedores
fornecedores = [
    "Fornecedor 1", "Fornecedor 2", "Fornecedor 3", 
    "Fornecedor 4", "Fornecedor 5", "Fornecedor 6", 
    "Fornecedor 7", "Fornecedor 8", "Fornecedor 9"
]
resultado.index = fornecedores

# Exibir Resultados
print("Resultado Final:")
print(resultado)