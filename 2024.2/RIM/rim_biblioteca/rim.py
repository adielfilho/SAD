import numpy as np 
import json

#essa ta mais certa
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
        """Normalização baseada na distância para o ideal (min e max)."""
        Y = np.zeros_like(self.X, dtype=float)
        for j, crit in enumerate(self.criteria):
            col = self.X[:, j]
            t_min, t_max = self.intervals[crit]  # Intervalos do critério
            s_min, s_max = self.reference_ideals[crit]  # Valores ideais de referência
            for i, x in enumerate(col):
                # Distância para o valor ideal mais próximo (mínimo ou máximo)
                d_min = min(abs(x - s_min), abs(x - s_max))
                # Normalização com base no intervalo
                Y[i, j] = 1 - (d_min / (t_max - t_min)) if (t_max - t_min) != 0 else 1
        return Y

    def calculate_weighted_normalized_matrix(self):
        """Calcula a matriz ponderada normalizada."""
        Y = self.normalize_with_ideal()  # Normalização
        return Y * self.weights  # Multiplica a normalização pelos pesos dos critérios

    def calculate_indices(self):
        """Calcula os índices I_pos, I_neg e R para as alternativas."""
        weighted_normalized_matrix = self.calculate_weighted_normalized_matrix()  # Matriz normalizada ponderada
        I_pos = np.sqrt(np.sum((weighted_normalized_matrix - self.weights) ** 2, axis=1))  # Distância positiva
        I_neg = np.sqrt(np.sum(weighted_normalized_matrix ** 2, axis=1))  # Distância negativa
        R = I_neg / (I_pos + I_neg)  # Índice de similaridade com os valores ideais
        ranking = sorted(zip(self.alternatives, R), key=lambda x: x[1], reverse=True)  # Classificação das alternativas
        scores = {alt: round(R[i], 5) for i, alt in enumerate(self.alternatives)}  # Pontuação das alternativas
        normalized_weights = {c: round(float(self.weights[i]), 5) for i, c in enumerate(self.criteria)}
        weighted_matrix_dict = {self.alternatives[i]: [round(x, 5) for x in weighted_normalized_matrix[i]] for i in range(len(self.alternatives))}
        return {
            "classificacao": [alt for alt, _ in ranking],  # Classificação das alternativas
            "pontuacoes": scores,  # Pontuação de cada alternativa
            "pesos": normalized_weights,  # Pesos normalizados
            "matriz_normalizada_ponderada": weighted_matrix_dict  # Matriz normalizada ponderada
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
        return json.dumps({"metodo": "RIM", "resultados": results}, indent=2, ensure_ascii=False)
    
    solver = RIM([], [], {}, {}, {}, {})
    resultado = solver.process_json(entrada_json)
    print(resultado)