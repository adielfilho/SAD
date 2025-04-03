from rim.rim import RIM

# Exemplo de matriz de decisão
decision_matrix = [
    [7, 9, 8],
    [6, 8, 7],
    [8, 6, 9]
]

weights = [0.5, 0.3, 0.2]  # Pesos dos critérios
criteria_types = ["max", "max", "max"]  # Todos critérios de maximização

rim = RIM(decision_matrix, weights, criteria_types)
ranking, distances = rim.rank_alternatives()

print("Ranking das alternativas:", ranking)
print("Distâncias:", distances)