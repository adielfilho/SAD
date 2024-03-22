import numpy as np
# Decision Matrix Normalization
def decision_matrix_normalization(decision_matrix, domain_matrix, weights):
    R = np.zeros_like(decision_matrix)
    for i in range(decision_matrix.shape[0]):
        for j in range(decision_matrix.shape[1]):
            R[i, j] = decision_matrix[i, j] / domain_matrix[0, j]
    V = np.zeros_like(R)
    for i in range(V.shape[0]):
        for j in range(V.shape[1]):
            V[i, j] = weights[j] * R[i, j]
    return V
