import json
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any
from utils.format_output import format_to_json
from utils.invert_matrix import invert_matrix

class FTOPSISProcessor:
    
    @staticmethod
    def load_json_data(file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file {file_path} not found")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in {file_path}")

    @staticmethod
    def print_results(result: pd.DataFrame, title: str = "Results") -> None:
        print(f"\n{title}:")
        print(result.to_string(index=True, float_format="%.5f"))


def trapezoidal_ftopsis_class(input_path: str = 'data/json/trapezoidal_input.json') -> None:
    from ftopsis_class.trapezoidal_core import FuzzyNumber, FTOPSISClass, CriteriaType

    data = FTOPSISProcessor.load_json_data(input_path)
    #print(data)
    criteria_type = {k: CriteriaType[v] for k, v in data['criteria_type'].items()}
    
    ftopsis = FTOPSISClass(
        linguistic_variables_alternatives=data['linguistic_variables_alternatives'],
        linguistic_variables_weights=data['linguistic_variables_weights'],
        weights=data['weights'],
        criteria_type=criteria_type,
        alternatives=data['alternatives'],
        criteria=data['weights'].keys(),
        profile_matrix=data['profile_matrix'],
        decision_matrix=data['decision_matrix'],
        profile_mapping=data['profile_mapping']
    )
    
    closeness, classification = ftopsis.run()
    
    print("\nRunning FTOPSIS-Class (Dynamic Output)...")
    
    # Obter perfis dinamicamente
    profiles = list(data['profile_matrix'].keys())
    if not profiles:
        raise ValueError("Nenhum perfil definido na matriz de referência")

    # Calcular largura das colunas
    max_profile_length = max(len(profile) for profile in profiles)
    col_width = max(max_profile_length + 2, 12)  # Mínimo de 12 caracteres

    # Header dinâmico
    header = f"{'Element':<10}"
    header += "".join([f"{profile:<{col_width}}" for profile in profiles])
    header += f"{'Classification':<20}"
    print(header)
    print("-" * (10 + (col_width * len(profiles)) + 20))

    # Linhas dinâmicas
    for element in data['alternatives']:
        cc = closeness[element]
        best_profile, best_cc = classification[element]
        
        # Valores de proximidade para cada perfil
        row = f"{element:<10}"
        for profile in profiles:
            row += f"{cc.get(profile, 0.0):<{col_width}.5f}"
        
        # Classificação final
        row += f"{best_profile} ({best_cc:.5f})"
        print(row)


def triangular_ftopsis_class(input_path: str = "data/json/triangular_input.json") -> Tuple[pd.DataFrame, Dict]:
    from ftopsis_class.triangular_core import CriteriaType, FTOPSISClass as TriFTOPSIS

    config = FTOPSISProcessor.load_json_data(input_path)

    linguistic_vars_alt = {k: np.array(v) for k, v in config['linguistic_variables_alternatives'].items()}
    linguistic_vars_weight = {k: np.array(v) for k, v in config['linguistic_variables_weights'].items()}

    decision_matrix = pd.DataFrame({
        k: [linguistic_vars_alt[val] for val in v]
        for k, v in config['decision_matrix'].items()
    })
    
    profile_matrix = pd.DataFrame({
        k: [linguistic_vars_alt[val] for val in v]
        for k, v in config['profile_matrix'].items()
    })

    weights = pd.DataFrame({k: [linguistic_vars_weight[v[0]]] for k, v in config['weights'].items()})
    criteria_type = {k: CriteriaType[v] for k, v in config['criteria_type'].items()}
    profile_mapping = {int(k): v for k, v in config['profile_mapping'].items()}

    norm_matrix = TriFTOPSIS.normalize_matrix(decision_matrix, criteria_type)
    weighted_matrix = TriFTOPSIS.weigh_matrix(norm_matrix, weights)
    final_matrix = TriFTOPSIS.round_weighted_normalized_matrix(weighted_matrix)

    norm_profile = TriFTOPSIS.normalize_matrix(profile_matrix, criteria_type)
    weighted_profile = TriFTOPSIS.weigh_matrix(norm_profile, weights)
    final_profile = TriFTOPSIS.round_weighted_normalized_matrix(weighted_profile)

    pos_sol, neg_sol = TriFTOPSIS.ideal_solution(final_profile, profile_mapping)
    pos_dist, neg_dist = TriFTOPSIS.distance_calculation(final_matrix, pos_sol, neg_sol)
    result = TriFTOPSIS.proximity_coefficient(pos_dist, neg_dist)

    result.index = config['alternatives']
    result['Classificação'] = result.idxmax(axis=1)
    json_output = format_to_json(result)

    FTOPSISProcessor.print_results(result)
    return result, json_output


def main() -> None:
    print("FTOPSIS Classification System")
    print("------------------------------")
    
    while True:
        choice = input("Escolha o tamanho do número fuzzy:\n[3] Triangular\n[4] Trapezoidal\n> ")
        
        if choice == "3":
            triangular_ftopsis_class()
            break
        elif choice == "4":
            trapezoidal_ftopsis_class()
            break
        print("Entrada inválida, por favor insira 3 ou 4.\n")


if __name__ == "__main__":
    main()
    """
    try:
        main()
    except Exception as e:
        print(f"\nErro: {str(e)}")
        exit(1)
    """