import numpy as np
from typing import Dict, List, Tuple
from enum import Enum
from .utils.invert_matrix import invert_matrix

class CriteriaType(Enum):
    Benefit = 1
    Cost = 0

class FuzzyNumber:
    def __init__(self, a1: float, a2: float, a3: float, a4: float):
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
    
    def __repr__(self):
        return f"FuzzyNumber({self.a1}, {self.a2}, {self.a3}, {self.a4})"
    
    def distance(self, other: 'FuzzyNumber') -> float:
        return np.sqrt(0.25 * (
            (self.a1 - other.a1)**2 + 
            (self.a2 - other.a2)**2 + 
            (self.a3 - other.a3)**2 + 
            (self.a4 - other.a4)**2
        ))

class FTOPSISClass:
    
    def __init__(self, linguistic_variables_alternatives: Dict, linguistic_variables_weights: Dict, weights: Dict, criteria_type: Dict,
                 alternatives: List[str], criteria: List[str], profile_matrix: Dict, decision_matrix: Dict, profile_mapping: Dict):
        self.linguistic_variables_alternatives = {k: FuzzyNumber(*v) if not isinstance(v, FuzzyNumber) else v 
                                for k, v in linguistic_variables_alternatives.items()}
        self.linguistic_variables_weights = {k: FuzzyNumber(*v) if not isinstance(v, FuzzyNumber) else v 
                                for k, v in linguistic_variables_weights.items()}
        self.weights = weights
        self.criteria_type = criteria_type
        self.alternatives = alternatives
        self.criteria = criteria
        self.profile_matrix = profile_matrix
        self.decision_matrix = decision_matrix
        self.profile_mapping = profile_mapping

    def _normalize_criteria(self, values: List[FuzzyNumber], criterion: str) -> List[FuzzyNumber]:
        if self.criteria_type[criterion] == CriteriaType.Benefit:
            max_val = max([v.a4 for v in values])  # Usamos o maior valor do suporte
            return [FuzzyNumber(v.a1/max_val, v.a2/max_val, v.a3/max_val, v.a4/max_val) for v in values]
        else:
            min_val = min([v.a1 for v in values])  # Usamos o menor valor do suporte
            return [FuzzyNumber(min_val/v.a4, min_val/v.a3, min_val/v.a2, min_val/v.a1) for v in values]

    def normalize_matrix(self) -> Dict:
        inverted_matrix = invert_matrix(self.alternatives, self.criteria, self.decision_matrix)
        fuzzy_matrix = {
            fund: [self.linguistic_variables_alternatives[term] for term in terms]
            for fund, terms in inverted_matrix.items()
        }

        normalized = {fund: [] for fund in self.alternatives}
        for i, criterion in enumerate(self.criteria):
            values = [fuzzy_matrix[fund][i] for fund in self.alternatives]
            normalized_values = self._normalize_criteria(values, criterion)

            weight = self.linguistic_variables_weights[self.weights[criterion][0]]
            for j, fund in enumerate(self.alternatives):
                nv = normalized_values[j]
                weighted = FuzzyNumber(
                    nv.a1 * weight.a1,
                    nv.a2 * weight.a2,
                    nv.a3 * weight.a3,
                    nv.a4 * weight.a4
                )
                normalized[fund].append(weighted)
        
        return normalized

    def calculate_closeness(self) -> Dict:
        normalized = self.normalize_matrix()

        inverted_profile_matrix = invert_matrix(list(self.profile_mapping.values()), list(self.criteria), self.profile_matrix)

        profiles = list(inverted_profile_matrix.keys())
        results = {fund: {} for fund in self.alternatives}
        
        for profile in profiles:
            A_p_pos = []
            for i, criterion in enumerate(self.criteria):
                term = inverted_profile_matrix[profile][i]
                weight_term = self.weights[criterion]
                
                fuzzy_num = self.linguistic_variables_alternatives[term]
                weight = self.linguistic_variables_weights[weight_term[0]]
                
                weighted = FuzzyNumber(
                    fuzzy_num.a1 * weight.a1,
                    fuzzy_num.a2 * weight.a2,
                    fuzzy_num.a3 * weight.a3,
                    fuzzy_num.a4 * weight.a4
                )
                A_p_pos.append(weighted)
            
            profile_distances = {}
            for other_profile in profiles:
                if other_profile == profile:
                    continue
                
                distance = 0
                for i in range(len(self.criteria)):
                    term_p = inverted_profile_matrix[profile][i]
                    term_op = inverted_profile_matrix[other_profile][i]
                    
                    distance += self.linguistic_variables_alternatives[term_p].distance(
                        self.linguistic_variables_alternatives[term_op]
                    )
                profile_distances[other_profile] = distance
            
            farthest_profile = max(profile_distances, key=profile_distances.get)
            
            A_p_neg = []
            for i, criterion in enumerate(self.criteria):
                term = inverted_profile_matrix[farthest_profile][i]
                weight_term = self.weights[criterion]
                
                fuzzy_num = self.linguistic_variables_alternatives[term]
                weight = self.linguistic_variables_weights[weight_term[0]]
                
                weighted = FuzzyNumber(
                    fuzzy_num.a1 * weight.a1,
                    fuzzy_num.a2 * weight.a2,
                    fuzzy_num.a3 * weight.a3,
                    fuzzy_num.a4 * weight.a4
                )
                A_p_neg.append(weighted)
            
            for fund in self.alternatives:
                d_plus = sum(
                    normalized[fund][i].distance(A_p_pos[i]) 
                    for i in range(len(self.criteria))
                )
                
                d_minus = sum(
                    normalized[fund][i].distance(A_p_neg[i]) 
                    for i in range(len(self.criteria))
                )
                
                cc = d_minus / (d_plus + d_minus) if (d_plus + d_minus) != 0 else 0
                results[fund][profile] = cc
        
        return results

    def classify_funds(self) -> Dict:
        closeness = self.calculate_closeness()
        classification = {}
        
        for fund in self.alternatives:
            max_cc = -1
            best_profile = None
            
            for profile, cc in closeness[fund].items():
                if cc > max_cc:
                    max_cc = cc
                    best_profile = profile
            
            classification[fund] = (best_profile, max_cc)
        
        return classification

    def run(self) -> Tuple[Dict, Dict]:
        closeness = self.calculate_closeness()
        classification = self.classify_funds()
        return closeness, classification