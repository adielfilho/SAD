import numpy as np
import json

class RIM:
    def __init__(self, alternatives, criteria, performance_matrix, criteria_types, weights):
        self.alternatives = alternatives  # Lista das alternativas (A1, A2, ...)
        self.criteria = criteria  # Lista dos critérios (C1, C2, ...)
        self.performance_matrix = performance_matrix
        self.X = np.array([performance_matrix[a] for a in alternatives])  # Matriz de desempenho
        self.weights = np.array([weights[c] for c in criteria])  # Pesos dos critérios
        self.criteria_types = criteria_types  # Tipos dos critérios (max/min)

    def normalize_with_ideal(self): #normalizando os valores na matrix
        Y = np.zeros_like(self.X, dtype=float)  # Matriz de saída de zeros
        for j, crit in enumerate(self.criteria):  # Para cada critério
            col = self.X[:, j]  # Obtém os valores da coluna (critérios)
            t_min, t_max = np.min(col), np.max(col)  # Valores mínimo e máximo da coluna
            s_min, s_max = (t_min, t_max) if self.criteria_types[crit] == "max" else (t_max, t_min)

            for i, x in enumerate(col):  # Para cada alternativa
                if self.criteria_types[crit] == "max":  # Se o critério for "max"
                    if x == s_max:  # Se o valor for igual ao valor máximo da coluna
                        Y[i, j] = 1  # Atribui 1 à matriz normalizada
                    else:
                        d_min = min(abs(x - s_min), abs(x - s_max))  # Distância mínima ao ideal
                        Y[i, j] = 1 - (d_min / (t_max - t_min))  # Cálculo da normalização
                else:  # Se o critério for "min"
                    if x == s_min:  # Se o valor for igual ao valor mínimo da coluna
                        Y[i, j] = 1  # Atribui 1 à matriz normalizada
                    else:
                        d_min = min(abs(x - s_min), abs(x - s_max))  # Distância mínima ao ideal
                        Y[i, j] = 1 - (d_min / (t_max - t_min))  # Cálculo da normalização
        print(Y)
        return Y  # Retorna a matriz normalizada

    def calculate_weighted_normalized_matrix(self):  #pesos bagunçados
        Y = self.normalize_with_ideal()  # Obtém a matriz normalizada
        weighted_matrix = Y * self.weights  # Aplica os pesos na matriz normalizada
        print(weighted_matrix)
        return weighted_matrix



    def calculate_indices(self): #pesos normalizados
        weighted_normalized_matrix = self.calculate_weighted_normalized_matrix()
        I_pos = np.sqrt(np.sum((weighted_normalized_matrix - self.weights) ** 2, axis=1))
        I_neg = np.sqrt(np.sum(weighted_normalized_matrix ** 2, axis=1))
        R = I_neg / (I_pos + I_neg)
        ranking = sorted(zip(self.alternatives, R), key=lambda x: x[1], reverse=True)
        normalized_weights = {alt: round(R[i] / sum(R), 4) for i, alt in enumerate(self.alternatives)}
        print(normalized_weights)
        return {
            "ranking": [alt for alt, _ in ranking],
            "scores": {alt: round(score, 4) for alt, score in ranking},
            "normalized_weights": normalized_weights
        }


    def process_json(self, json_data): #ler o json
        data = json.loads(json_data)
        params = data["parameters"]
        self.__init__(params["alternatives"], params["criteria"], params["performance_matrix"],
                      params["criteria_types"], params["weights"])
        results = self.calculate_indices()
        json_str = json.dumps({"method": "RIM", "results": results}, indent=2)
        json_str = json_str.replace('\n    ],', '],')
        json_str = json_str.replace('\n    },', '},')
        json_str = json_str.replace('\n      ', ' ').replace('\n    }', '}')
        return json_str
    
    solver = RIM([], [], {}, {}, {})
    resultado = solver.process_json(entrada_json)
    print(resultado)