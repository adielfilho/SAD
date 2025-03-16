import numpy as np

class Topsis:
    def __init__(self, decision_matrix, weights, criteria):
        """
        Classe para executar o algoritmo TOPSIS em Pyodide.

        :param decision_matrix: Matriz de decisão (lista de listas, onde cada linha é uma alternativa)
        :param weights: Pesos dos critérios (lista de valores positivos)
        :param criteria: Lista indicando se o critério é benefício (1) ou custo (0)
        """
        self.decision_matrix = np.array(decision_matrix, dtype=np.float64)
        self.weights = np.array(weights, dtype=np.float64)
        self.criteria = np.array(criteria)
    
    def normalize_matrix(self):
        """Normaliza a matriz de decisão usando a norma Euclidiana."""
        norm = np.linalg.norm(self.decision_matrix, axis=0)
        return self.decision_matrix / norm

    def weighted_normalized_matrix(self):
        """Multiplica a matriz normalizada pelos pesos dos critérios."""
        return self.normalize_matrix() * self.weights

    def ideal_solutions(self):
        """Calcula as soluções ideais positiva e negativa."""
        weighted_matrix = self.weighted_normalized_matrix()
        ideal_positive = np.where(self.criteria == 1, np.max(weighted_matrix, axis=0), np.min(weighted_matrix, axis=0))
        ideal_negative = np.where(self.criteria == 1, np.min(weighted_matrix, axis=0), np.max(weighted_matrix, axis=0))
        return ideal_positive, ideal_negative

    def distance_to_ideal(self, ideal_solution):
        """Calcula a distância Euclidiana para uma solução ideal."""
        return np.linalg.norm(self.weighted_normalized_matrix() - ideal_solution, axis=1)

    def calculate_scores(self):
        """Calcula os scores de similaridade à solução ideal positiva."""
        ideal_positive, ideal_negative = self.ideal_solutions()
        dist_positive = self.distance_to_ideal(ideal_positive)
        dist_negative = self.distance_to_ideal(ideal_negative)
        return dist_negative / (dist_positive + dist_negative)

    def rank_alternatives(self):
        """Retorna o ranking das alternativas baseado nos scores."""
        scores = self.calculate_scores()
        ranking = np.argsort(scores)[::-1]  
        return (ranking + 1).tolist(), scores.tolist()

