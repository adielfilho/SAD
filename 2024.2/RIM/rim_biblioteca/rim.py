import numpy as np

class RIM:
    def __init__(self, decision_matrix, weights, criteria_types):
        """
        :param decision_matrix: Matriz de decisão (alternativas x critérios)
        :param weights: Lista de pesos dos critérios
        :param criteria_types: Lista indicando se cada critério é "max" ou "min"
        """
        self.decision_matrix = np.array(decision_matrix, dtype=float)
        self.weights = np.array(weights, dtype=float)
        self.criteria_types = criteria_types

    def normalize(self):
        """ Normaliza a matriz de decisão """
        norm_matrix = np.zeros_like(self.decision_matrix)
        for j in range(self.decision_matrix.shape[1]):
            col = self.decision_matrix[:, j]
            if self.criteria_types[j] == "max":
                norm_matrix[:, j] = col / col.max()
            else:  # Minimização
                norm_matrix[:, j] = col.min() / col
        return norm_matrix

    def calculate_ideal_reference(self):
        """ Calcula a referência ideal ponderada """
        norm_matrix = self.normalize()
        return np.dot(norm_matrix, self.weights)

    def rank_alternatives(self):
        """ Calcula as distâncias das alternativas à referência ideal e ordena """
        ref = self.calculate_ideal_reference()
        distances = np.linalg.norm(self.decision_matrix - ref, axis=1)
        ranking = np.argsort(distances)  # Índices das melhores alternativas
        return ranking, distances

