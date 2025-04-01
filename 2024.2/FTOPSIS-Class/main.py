from ftopsis_class import CriteriaType, FTOPSISClass as ft
import numpy as np
import pandas as pd
import json

# Recebe a entrada (tipo json)
ARQUIVO_JSON = "triangular.json"

# Carrega Entrada .Json
with open(ARQUIVO_JSON) as f:
    config = json.load(f)

# Variáveis linguísticas
vl_alternativas = {k: np.array(v) for k, v in config['linguistic_variables_alternatives'].items()}
vl_pesos = {k: np.array(v) for k, v in config['linguistic_variables_weights'].items()}

# Matrizes
matriz_decisao = pd.DataFrame({k: [vl_alternativas[val] for val in v] 
                             for k, v in config['decision_matrix'].items()})
matriz_perfil = pd.DataFrame({k: [vl_alternativas[val] for val in v] 
                           for k, v in config['profile_matrix'].items()})

# Pesos e critérios
pesos = pd.DataFrame({k: [vl_pesos[v[0]]] for k, v in config['weights'].items()})
tipo_criterio = {k: CriteriaType[v] for k, v in config['criteria_type'].items()}
mapeamento_perfil = {int(k): v for k, v in config['profile_mapping'].items()}

# Executa o FTOPSIS-CLASS
matriz_norm = ft.normalize_matrix(matriz_decisao, tipo_criterio)
matriz_pond = ft.weigh_matrix(matriz_norm, pesos)
matriz_final = ft.round_weighted_normalized_matrix(matriz_pond)

matriz_perfil_norm = ft.normalize_matrix(matriz_perfil, tipo_criterio)
matriz_perfil_pond = ft.weigh_matrix(matriz_perfil_norm, pesos)
matriz_perfil_final = ft.round_weighted_normalized_matrix(matriz_perfil_pond)

sol_pos, sol_neg = ft.ideal_solution(matriz_perfil_final, mapeamento_perfil)
dist_pos, dist_neg = ft.distance_calculation(matriz_final, sol_pos, sol_neg)
resultado = ft.proximity_coefficient(dist_pos, dist_neg)

# Prepara a Saída
resultado.index = config['suppliers']
print("\nResultado Final:")
print(resultado)