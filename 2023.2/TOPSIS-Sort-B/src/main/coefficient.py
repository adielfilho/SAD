import numpy as np
from normalization import decision_matrix_normalization

def approximation_coefficient(decision_matrix, domain_matrix, weights):
    V = decision_matrix_normalization(decision_matrix, domain_matrix, weights)
    # Ideal and Anti-Ideal Solutions Calculation
    V_ideal = np.max(V, axis=0)
    V_anti_ideal = np.min(V, axis=0)

    # Euclidean Distances Calculation
    d_plus = np.zeros(decision_matrix.shape[0])
    d_minus = np.zeros(decision_matrix.shape[0])

    for i in range(decision_matrix.shape[0]):
        d_plus[i] = np.sqrt(np.sum((V[i, :] - V_ideal)**2))
        d_minus[i] = np.sqrt(np.sum((V[i, :] - V_anti_ideal)**2))

    # Avoiding division by zero
    d_plus[d_plus == 0] = np.finfo(float).eps
    d_minus[d_minus == 0] = np.finfo(float).eps

    # Approximation Coefficient Calculation
    Cl = d_minus / (d_plus + d_minus)
    return Cl