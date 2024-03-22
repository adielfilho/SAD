import numpy as np

def dominant_profiles_distances(decision_matrix, domain_matrix, dominant_profiles, weights):
    dominant_profiles_normalized = np.zeros_like(dominant_profiles)
    
    for i in range(dominant_profiles.shape[0]):
        for j in range(dominant_profiles.shape[1]):
            # Evitar divisão por zero
            if domain_matrix[0, j] != 0:
                dominant_profiles_normalized[i, j] = dominant_profiles[i, j] / domain_matrix[0, j]
            else:
                dominant_profiles_normalized[i, j] = 0  # Ou escolha um valor adequado se domain_matrix[0, j] for zero
    
    V_profiles = np.zeros_like(dominant_profiles_normalized)
    
    for i in range(V_profiles.shape[0]):
        for j in range(V_profiles.shape[1]):
            V_profiles[i, j] = weights[j] * dominant_profiles_normalized[i, j]

    # Dominant Profiles Distances Calculation
    V_ideal_profiles = np.max(V_profiles, axis=0)
    V_anti_ideal_profiles = np.min(V_profiles, axis=0)

    d_plus_profiles = np.zeros(dominant_profiles.shape[0])
    d_minus_profiles = np.zeros(dominant_profiles.shape[0])
    
    for k in range(dominant_profiles.shape[0]):
        d_plus_profiles[k] = np.sqrt(np.sum((V_profiles[k, :] - V_ideal_profiles)**2))
        d_minus_profiles[k] = np.sqrt(np.sum((V_profiles[k, :] - V_anti_ideal_profiles)**2))

    # Avoiding division by zero
    d_plus_profiles[d_plus_profiles == 0] = np.finfo(float).eps
    d_minus_profiles[d_minus_profiles == 0] = np.finfo(float).eps

    # Dominant Profiles Approximation Coefficient Calculation
    Cl_profiles = d_minus_profiles / (d_plus_profiles + d_minus_profiles)
    
    return Cl_profiles
