import numpy as np
from coefficient import approximation_coefficient
from profiles import dominant_profiles_distances

def topsis_b_sort_profile_classification(decision_matrix, domain_matrix, dominant_profiles, weights):
    Cl = approximation_coefficient(decision_matrix, domain_matrix, weights)
    Cl_profiles = dominant_profiles_distances(decision_matrix, domain_matrix, dominant_profiles, weights)
    
    C = np.zeros((decision_matrix.shape[0], 2))
    for i in range(decision_matrix.shape[0]):
        if Cl[i] >= Cl_profiles[0]:
            C[i, 0] = 1
        else:
            for k in range(1, dominant_profiles.shape[0]):
                if Cl_profiles[k-1] > Cl[i] >= Cl_profiles[k]:
                    C[i, 0] = k + 1
                    break
        C[i, 1] = Cl[i]

    best_solution_index = np.argmax(C[:, 1])  # Index of the row with the highest approximation coefficient
    best_solution = decision_matrix[best_solution_index]  # Best solution
    best_profile = int(C[best_solution_index, 0])  # Dominant profile of the best solution
    
    return C, best_solution, best_profile
