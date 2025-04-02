import numpy as np 
import json

class RIM:
    def __init__(self, alternatives, criteria, performance_matrix, weights, intervals, reference_ideals):
        self.alternatives = alternatives
        self.criteria = criteria
        self.performance_matrix = performance_matrix
        self.X = np.array([performance_matrix[a] for a in alternatives])  # Matriz de desempenho
        self.weights = np.array([weights[c] for c in criteria])  # Pesos
        self.criteria_types = {c: "max" for c in criteria}  # Assumindo que todos os critérios são max
        self.intervals = intervals  # Intervalos de normalização
        self.reference_ideals = reference_ideals  # Ideais de referência

    def normalize_with_ideal(self):
        """Normalização baseada na distância para o ideal (min e max), agora diferenciada."""
        Y = np.zeros_like(self.X, dtype=float)
        for j, crit in enumerate(self.criteria):
            col = self.X[:, j]
            t_min, t_max = self.intervals[crit]  # Intervalos do critério
            s_min, s_max = self.reference_ideals[crit]  # Valores ideais de referência
            
            for i, x in enumerate(col):
                if s_min <= x <= s_max:
                    Y[i, j] = 1
                elif x < s_min:
                    denom = s_min - t_min
                    Y[i, j] = 1 - ((s_min - x) / denom) if denom != 0 else 1
                elif x > s_max:
                    denom = t_max - s_max
                    Y[i, j] = 1 - ((x - s_max) / denom) if denom != 0 else 1
        return Y

    def calculate_weighted_normalized_matrix(self):
        """Calcula a matriz ponderada normalizada."""
        Y = self.normalize_with_ideal()
        return Y * self.weights

    def calculate_indices(self):
        """Calcula os índices I_pos, I_neg e R para as alternativas."""
        weighted_normalized_matrix = self.calculate_weighted_normalized_matrix()
        I_pos = np.sqrt(np.sum((weighted_normalized_matrix - self.weights) ** 2, axis=1))
        I_neg = np.sqrt(np.sum(weighted_normalized_matrix ** 2, axis=1))
        R = I_neg / (I_pos + I_neg)
        ranking = sorted(zip(self.alternatives, R), key=lambda x: x[1], reverse=True)
        scores = {alt: round(R[i], 5) for i, alt in enumerate(self.alternatives)}
        normalized_weights = {c: round(float(self.weights[i]), 5) for i, c in enumerate(self.criteria)}
        weighted_matrix_dict = {self.alternatives[i]: [round(x, 5) for x in weighted_normalized_matrix[i]] for i in range(len(self.alternatives))}
        return {
            "ranking": [alt for alt, _ in ranking],
            "scores": scores,
            "weights": normalized_weights,
            "weighted_normalized_matrix": weighted_matrix_dict
        }

    def process_json(self, json_data):
        """Processa o JSON de entrada e retorna os resultados em formato JSON."""
        data = json.loads(json_data)
        params = data["parameters"]
        self.__init__(
            params["alternatives"], params["criteria"], params["performance_matrix"],
            params["weights"], params["intervals"], params["reference_ideals"]
        )
        results = self.calculate_indices()
        return json.dumps({"method": "RIM", "results": results}, indent=2, ensure_ascii=False)
    
    solver = RIM([], [], {}, {}, {}, {})
    resultado = solver.process_json(entrada_json)
    print(resultado)