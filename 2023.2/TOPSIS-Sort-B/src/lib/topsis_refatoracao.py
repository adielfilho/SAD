import numpy as np

# Normalização da matriz de decisão
def normalizao_ponderacao(X,D,w):

    R = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            R[i, j] = X[i, j] / D[0, j]
    V = np.zeros_like(R)
    for i in range(V.shape[0]):
        for j in range(V.shape[1]):
            V[i, j] = w[j] * R[i, j]
    return V

def coeficiente_de_aproximacao(X, D, w):
    V = normalizao_ponderacao(X,D,w)
    # Cálculo das soluções ideal e anti-ideal
    V_ideal = np.max(V, axis=0)
    V_anti_ideal = np.min(V, axis=0)

    # Cálculo das distâncias euclidianas
    d_plus = np.zeros(X.shape[0])
    d_minus = np.zeros(X.shape[0])

    for i in range(X.shape[0]):
        d_plus[i] = np.sqrt(np.sum((V[i, :] - V_ideal)**2))
        d_minus[i] = np.sqrt(np.sum((V[i, :] - V_anti_ideal)**2))

    # Corrigindo divisão por zero
    d_plus[d_plus == 0] = np.finfo(float).eps
    d_minus[d_minus == 0] = np.finfo(float).eps

    # Cálculo do coeficiente de aproximação
    Cl = d_minus / (d_plus + d_minus)
    return Cl

def distancia_dos_perfis_dominantes(X, D, P, w):
    P_normalized = np.zeros_like(P)
    for i in range(P.shape[0]):
        for j in range(P.shape[1]):
            P_normalized[i,j] = P[i, j]/D[0, j]
    V_perfis = np.zeros_like(P_normalized)

    for i in range(V_perfis.shape[0]):
        for j in range(V_perfis.shape[1]):
            V_perfis[i, j] = w[j] * P_normalized[i, j]

    V_ideal_perfis = np.max(V_perfis, axis=0)
    V_anti_ideal_perfis = np.min(V_perfis, axis=0)

    d_plus_p = np.zeros(P.shape[0])
    d_minus_p = np.zeros(P.shape[0])
    for k in range(P.shape[0]):
        d_plus_p[k] = np.sqrt(np.sum((V_perfis[k, :] - V_ideal_perfis)**2))
        d_minus_p[k] = np.sqrt(np.sum((V_perfis[k, :] - V_anti_ideal_perfis)**2))

    # Corrigindo divisão por zero
    d_plus_p[d_plus_p == 0] = np.finfo(float).eps
    d_minus_p[d_minus_p == 0] = np.finfo(float).eps

    # Cálculo do coeficiente de aproximação dos perfis dominantes
    Cl_p = d_minus_p / (d_plus_p + d_minus_p)
    return Cl_p
def topsis_sort_b_classificao_dos_perfis(X, D, P, w):

    Cl = coeficiente_de_aproximacao(X,D, w)
    Cl_p = distancia_dos_perfis_dominantes(X,D,P,w)
    C = np.zeros((X.shape[0], 2))
    for i in range(X.shape[0]):
        if Cl[i] >= Cl_p[0]:
            C[i, 0] = 1
        else:
            for k in range(1, P.shape[0]):
                if Cl_p[k-1] > Cl[i] >= Cl_p[k]:
                    C[i, 0] = k + 1
                    break
        C[i, 1] = Cl[i]

    return C

X = np.array([[3, 8, 5],[9, 4, 1],[5, 2, 10], [10, 5, 2]])
P = np.array([[3, 7, 5]])
D = np.array([[1, 1, 1], [100, 100, 100]])
w = np.array([0.2, 0.2, 0.6])
print(topsis_sort_b_classificao_dos_perfis(X, D, P, w))