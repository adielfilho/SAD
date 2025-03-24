import numpy as np
import json

class Topsis:
    def __init__(self, alternatives, criteria, performance_matrix, criteria_types, weights):
        """
        Classe para executar o algoritmo TOPSIS.

        :param alternatives: Lista de alternativas (ex: ["A1", "A2", "A3"])
        :param criteria: Lista de critérios (ex: ["C1", "C2", "C3"])
        :param performance_matrix: Matriz de desempenho (dicionário onde as chaves são as alternativas)
        :param criteria_types: Tipos de critérios (dicionário com "max" ou "min")
        :param weights: Pesos dos critérios (dicionário com os pesos dos critérios)
        """
        self.alternatives = alternatives
        self.criteria = criteria
        self.performance_matrix = performance_matrix
        self.criteria_types = criteria_types
        self.weights = weights

        # Converte a matriz de desempenho para um formato numpy (alternativas x critérios)
        self.decision_matrix = np.array([performance_matrix[alt] for alt in alternatives], dtype=np.float64)

        # Mapeia os tipos de critérios (max ou min) para 1 ou 0
        self.criteria_flags = np.array([1 if criteria_types[c] == "max" else 0 for c in criteria])

        # Converte os pesos para um formato numpy
        self.weights_array = np.array([weights[c] for c in criteria], dtype=np.float64)
    
    def normalize_matrix(self):
        """Normaliza a matriz de decisão usando a norma Euclidiana."""
        norm = np.linalg.norm(self.decision_matrix, axis=0)
        return self.decision_matrix / norm

    def weighted_normalized_matrix(self):
        """Multiplica a matriz normalizada pelos pesos dos critérios."""
        return self.normalize_matrix() * self.weights_array

    def ideal_solutions(self):
        """Calcula as soluções ideais positiva e negativa."""
        weighted_matrix = self.weighted_normalized_matrix()
        ideal_positive = np.where(self.criteria_flags == 1, np.max(weighted_matrix, axis=0), np.min(weighted_matrix, axis=0))
        ideal_negative = np.where(self.criteria_flags == 1, np.min(weighted_matrix, axis=0), np.max(weighted_matrix, axis=0))
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
        ranking = np.argsort(scores)[::-1]  # Ranking em ordem decrescente
        ranked_alternatives = [self.alternatives[i] for i in ranking]
        return ranked_alternatives, scores.tolist()


# Função para ser chamada pelo React
def run_topsis(input_data):
    try:
        # Carregar e processar o input_data
        data = json.loads(input_data)

        # Extrair parâmetros
        alternatives = data['parameters']['alternatives']
        criteria = data['parameters']['criteria']
        performance_matrix = data['parameters']['performance_matrix']
        criteria_types = data['parameters']['criteria_types']
        weights = data['parameters']['weights']
        
        # Instanciar a classe Topsis com os dados extraídos
        topsis = Topsis(alternatives, criteria, performance_matrix, criteria_types, weights)

        # Calcular as soluções ideais
        ideal_positive, ideal_negative = topsis.ideal_solutions()

        # Calcular as distâncias para as soluções ideais
        dist_positive = topsis.distance_to_ideal(ideal_positive)
        dist_negative = topsis.distance_to_ideal(ideal_negative)

        # Calcular os scores TOPSIS
        topsis_scores = topsis.calculate_scores()

        # Calcular o ranking
        ranked_alternatives, scores = topsis.rank_alternatives()

        # Estruturar o resultado no formato desejado
        result = {
            "method": "TOPSIS",
            "results": {
                "positive_ideal_solution": {criteria[i]: float(ideal_positive[i]) for i in range(len(criteria))},
                "negative_ideal_solution": {criteria[i]: float(ideal_negative[i]) for i in range(len(criteria))},
                "distance_to_pis": {alternatives[i]: float(dist_positive[i]) for i in range(len(alternatives))},
                "distance_to_nis": {alternatives[i]: float(dist_negative[i]) for i in range(len(alternatives))},
                "topsis_score": {alternatives[i]: float(topsis_scores[i]) for i in range(len(alternatives))},
                "ranking": ranked_alternatives
            }
        }

        return result
    
    except Exception as e:
        print(f"Erro ao processar os dados: {e}")
        return {"error": str(e)}

# Função principal chamada pelo React
def get_input_data(input_data):
    return run_topsis(input_data)

