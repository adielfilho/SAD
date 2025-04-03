from __future__ import annotations
import json
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any, Union
from .utils.format_output import format_to_json
from .classes.trapezoidal_core import FuzzyNumber, FTOPSISClass, CriteriaType
from .utils.invert_matrix import invert_matrix

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

    @staticmethod
    def print_trapezoidal_results(alternatives: list, closeness: dict, 
                                classification: dict, profile_mapping: dict) -> None:
        profiles = list(profile_mapping.values())
        
        elem_width = 10
        profile_width = 15
        
        # Cabeçalho
        header = f"{'alternative':<{elem_width}}"
        for profile in profiles:
            header += f"{profile:<{profile_width}}"
        header += "Classification"
        print(header)
        
        # Linhas de dados
        for alternative in alternatives:
            cc = closeness[alternative]
            best_profile, best_cc = classification[alternative]
            
            row = f"{alternative:<{elem_width}}"
            for profile in profiles:
                row += f"{cc[profile]:<{profile_width}.5f}"
            row += f"{best_profile} ({best_cc:.5f})"
            
            print(row)

    @staticmethod
    def detect_fuzzy_type(data: Dict[str, Any]) -> str:
        if 'linguistic_variables_alternatives' in data:
            first_term = next(iter(data['linguistic_variables_alternatives'].values()))
            if len(first_term) == 4:
                return 'trapezoidal'
        
        if 'linguistic_variables_alternatives' in data:
            first_term = next(iter(data['linguistic_variables_alternatives'].values()))
            if len(first_term) == 3:
                return 'triangular'
        
        raise ValueError("Could not determine fuzzy number type from JSON structure")

def trapezoidal_ftopsis_class(data: Dict[str, Any]) -> Tuple[pd.DataFrame, Dict]:
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
    
    profiles = list(data['profile_mapping'].values())
    result_data = {
        alternative: {
            **{profile: closeness[alternative][profile] for profile in profiles},
            'Classification': classification[alternative][0]
        }
        for alternative in data['alternatives']
    }
    
    result = pd.DataFrame.from_dict(result_data, orient='index')
    
    json_output = {
        alternative: {
            'scores': {profile: float(closeness[alternative][profile]) for profile in profiles},
            'classification': classification[alternative][0],
        }
        for alternative in data['alternatives']
    }

    return json_output

def triangular_ftopsis_class(data: Dict[str, Any]) -> Tuple[pd.DataFrame, Dict]:
    from .classes.triangular_core import CriteriaType, FTOPSISClass as TriFTOPSIS

    linguistic_vars_alt = {k: np.array(v) for k, v in data['linguistic_variables_alternatives'].items()}
    linguistic_vars_weight = {k: np.array(v) for k, v in data['linguistic_variables_weights'].items()}

    decision_matrix = pd.DataFrame({
        k: [linguistic_vars_alt[val] for val in v]
        for k, v in data['decision_matrix'].items()
    })
    
    profile_matrix = pd.DataFrame({
        k: [linguistic_vars_alt[val] for val in v]
        for k, v in data['profile_matrix'].items()
    })

    weights = pd.DataFrame({k: [linguistic_vars_weight[v[0]]] for k, v in data['weights'].items()})
    criteria_type = {k: CriteriaType[v] for k, v in data['criteria_type'].items()}
    profile_mapping = {int(k): v for k, v in data['profile_mapping'].items()}

    norm_matrix = TriFTOPSIS.normalize_matrix(decision_matrix, criteria_type)
    weighted_matrix = TriFTOPSIS.weigh_matrix(norm_matrix, weights)
    final_matrix = TriFTOPSIS.round_weighted_normalized_matrix(weighted_matrix)

    norm_profile = TriFTOPSIS.normalize_matrix(profile_matrix, criteria_type)
    weighted_profile = TriFTOPSIS.weigh_matrix(norm_profile, weights)
    final_profile = TriFTOPSIS.round_weighted_normalized_matrix(weighted_profile)

    pos_sol, neg_sol = TriFTOPSIS.ideal_solution(final_profile, profile_mapping)
    pos_dist, neg_dist = TriFTOPSIS.distance_calculation(final_matrix, pos_sol, neg_sol)
    result = TriFTOPSIS.proximity_coefficient(pos_dist, neg_dist)

    result.index = data['alternatives']
    result['Classificação'] = result.idxmax(axis=1)
    json_output = format_to_json(result)

    return json_output


def main() -> None:
    while True:
        file_path = 'data/json/trapezoidal_input.json'
        
        #try:
        data = FTOPSISProcessor.load_json_data(file_path)
        fuzzy_type = FTOPSISProcessor.detect_fuzzy_type(data)
        
        if fuzzy_type == 'triangular':
            triangular_ftopsis_class(data)
        else:
            trapezoidal_ftopsis_class(data)
        break

        """    
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {file_path}. Por favor, tente novamente.")
        except ValueError as e:
            print(f"Erro no arquivo: {str(e)}. Por favor, verifique o formato e tente novamente.")
        except Exception as e:
            print(f"Erro inesperado: {str(e)}")
            exit(1)
        """

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nErro: {str(e)}")
        exit(1)