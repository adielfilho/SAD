import json
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any
from utils.format_output import format_to_json

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
    
    criteria_type = {k: CriteriaType[v] for k, v in data['criteria_type'].items()}
    
    ftopsis = FTOPSISClass(
        linguistic_terms=data['linguistic_terms'],
        weights=data['weights'],
        criteria_type=criteria_type,
        elements=data['elements'],
        criteria=data['criteria'],
        fuzzy_decision_matrix=data['fuzzy_decision_matrix'],
        reference_matrix=data['reference_matrix']
    )
    
    closeness, classification = ftopsis.run()
    
    print("\nRunning FTOPSIS-Class (corrected final version)...")
    header = f"{'Element':<10}{'Conservative':<12}{'Moderate':<10}{'Bold':<10}{'Aggressive':<12}{'Classification':<15}"
    print(header)
    
    for element in data['elements']:
        cc = closeness[element]
        best_profile, best_cc = classification[element]
        print(
            f"{element:<10}"
            f"{cc['Conservative']:10.5f}\t"
            f"{cc['Moderate']:10.5f}\t"
            f"{cc['Bold']:10.5f}\t"
            f"{cc['Aggressive']:10.5f}\t"
            f"{best_profile} ({best_cc:.5f})"
        )


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

    result.index = config['suppliers']
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
    try:
        main()
    except Exception as e:
        print(f"\nErro: {str(e)}")
        exit(1)