from ftopsis_class import CriteriaType, FTOPSISClass as ft
import numpy as np
import pandas as pd
import json
from utils.format_output import format_to_json

# Carrega o Json
def load_config(file_path: str) -> dict:
    with open(file_path) as f:
        return json.load(f)

# Prepara todas os dados necessários
def prepare_data(config: dict) -> tuple:
    # Variáveis linguísticas
    vl_alternativas = {k: np.array(v) for k, v in config['linguistic_variables_alternatives'].items()}
    vl_pesos = {k: np.array(v) for k, v in config['linguistic_variables_weights'].items()}
    
    # Matrizes
    matriz_decisao = pd.DataFrame({
        k: [vl_alternativas[val] for val in v] 
        for k, v in config['decision_matrix'].items()
    })
    matriz_perfil = pd.DataFrame({
        k: [vl_alternativas[val] for val in v] 
        for k, v in config['profile_matrix'].items()
    })
    
    # Pesos e critérios
    pesos = pd.DataFrame({k: [vl_pesos[v[0]]] for k, v in config['weights'].items()})
    tipo_criterio = {k: CriteriaType[v] for k, v in config['criteria_type'].items()}
    mapeamento_perfil = {int(k): v for k, v in config['profile_mapping'].items()}
    
    return matriz_decisao, matriz_perfil, pesos, tipo_criterio, mapeamento_perfil

# Executa o FTOPSIS-CLASS
def run_ftopsis(matriz_decisao, matriz_perfil, pesos, tipo_criterio, mapeamento_perfil) -> pd.DataFrame:
    # Normalização e ponderação
    matriz_norm = ft.normalize_matrix(matriz_decisao, tipo_criterio)
    matriz_pond = ft.weigh_matrix(matriz_norm, pesos)
    matriz_final = ft.round_weighted_normalized_matrix(matriz_pond)

    # Processamento do perfil
    matriz_perfil_norm = ft.normalize_matrix(matriz_perfil, tipo_criterio)
    matriz_perfil_pond = ft.weigh_matrix(matriz_perfil_norm, pesos)
    matriz_perfil_final = ft.round_weighted_normalized_matrix(matriz_perfil_pond)

    # Cálculo das soluções ideais
    sol_pos, sol_neg = ft.ideal_solution(matriz_perfil_final, mapeamento_perfil)
    dist_pos, dist_neg = ft.distance_calculation(matriz_final, sol_pos, sol_neg)
    return ft.proximity_coefficient(dist_pos, dist_neg)

def main(input_file: str = "triangular.json"):
    # Carrega configuração
    config = load_config(input_file)
    
    # Prepara dados
    matriz_decisao, matriz_perfil, pesos, tipo_criterio, mapeamento_perfil = prepare_data(config)
    
    # Executa FTOPSIS
    resultado = run_ftopsis(matriz_decisao, matriz_perfil, pesos, tipo_criterio, mapeamento_perfil)
    resultado.index = config['suppliers']
    resultado['Classificação'] = resultado.idxmax(axis=1)
    
    # Formata saída
    output_json = format_to_json(resultado)
    
    # Exibe resultados
    print("Resultado Final:")
    print(resultado)
    print("\nSaída em JSON:")
    print(json.dumps(output_json, indent=4, ensure_ascii=False))
    
    return resultado, output_json

if __name__ == "__main__":
    main()