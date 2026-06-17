import json
from typing import Dict, Tuple


class TriangularFuzzyNumber:
    def __init__(self, l: float, m: float, r: float):
        self.l = l  # left value
        self.m = m  # middle value
        self.r = r  # right value

    def __repr__(self):
        return f"TFN({self.l}, {self.m}, {self.r})"

    def is_in_range(
        self, other_low: "TriangularFuzzyNumber", other_high: "TriangularFuzzyNumber"
    ) -> bool:
        return self.l >= other_low.l and self.r <= other_high.r


class WFRIM:
    def __init__(self, input_file: str = None):
        self.alternatives = []
        self.criteria = []
        self.decision_matrix = {}
        self.weights = {}
        self.ranges = {}
        self.ideal_ranges = {}
        self.lambdas = {}

        if input_file:
            self.load_from_json(input_file)

    def load_from_json(self, input_file: str):
        data = json.loads(input_file)

        params = data["parameters"]
        self.criteria = params["criteria"]

        # Set weights, ranges, ideal ranges, and preferences
        for crit in self.criteria:
            self.weights[crit] = TriangularFuzzyNumber(*params["weights"][crit])
            self.ranges[crit] = (
                TriangularFuzzyNumber(*params["range"][crit][0]),
                TriangularFuzzyNumber(*params["range"][crit][1]),
            )
            self.ideal_ranges[crit] = (
                TriangularFuzzyNumber(*params["reference_ideal"][crit][0]),
                TriangularFuzzyNumber(*params["reference_ideal"][crit][1]),
            )
            self.lambdas[crit] = params["preferences"][crit]

        # Set alternatives and performance matrix
        for alt_data in params["performance_matrix"]:
            alt_name = alt_data["name"]
            self.alternatives.append(alt_name)
            self.decision_matrix[alt_name] = {
                crit: TriangularFuzzyNumber(*alt_data["values"][crit])
                for crit in self.criteria
            }

    def calculate_weighted_reference_ideal(
        self, criterion: str
    ) -> TriangularFuzzyNumber:
        C_j = self.ideal_ranges[criterion][0]
        D_j = self.ideal_ranges[criterion][1]
        lambda_j = self.lambdas[criterion]

        delta_1j = C_j.l
        delta_2j = (1 - lambda_j) * C_j.m + lambda_j * D_j.m
        delta_3j = D_j.r

        return TriangularFuzzyNumber(delta_1j, delta_2j, delta_3j)

    def absolute_distance(
        self, a: TriangularFuzzyNumber, b: TriangularFuzzyNumber
    ) -> float:
        return (abs(a.l - b.l) + abs(a.m - b.m) + abs(a.r - b.r)) / 3

    def distance_within_ideal_range(
        self, x: TriangularFuzzyNumber, criterion: str, delta: TriangularFuzzyNumber
    ) -> float:
        C_j = self.ideal_ranges[criterion][0]
        D_j = self.ideal_ranges[criterion][1]
        denominator = 1 + abs(C_j.l - D_j.r)
        return (
            abs(x.l - delta.l) / denominator
            + abs(x.m - delta.m)
            + abs(x.r - delta.r) / denominator
        ) / 3

    def distance_outside_ideal_range(
        self, x: TriangularFuzzyNumber, criterion: str, delta: TriangularFuzzyNumber
    ) -> float:
        A_j = self.ranges[criterion][0]
        B_j = self.ranges[criterion][1]
        return (
            self.absolute_distance(x, delta)
            + max(
                self.absolute_distance(A_j, delta), self.absolute_distance(delta, B_j)
            )
        ) / 2

    def normalize_performance(self, x: TriangularFuzzyNumber, criterion: str) -> float:
        A_j, B_j = self.ranges[criterion]
        C_j, D_j = self.ideal_ranges[criterion]
        delta_j = self.calculate_weighted_reference_ideal(criterion)

        if x.l == delta_j.l and x.m == delta_j.m and x.r == delta_j.r:
            return 1.0

        if x.is_in_range(C_j, D_j):
            dist = self.distance_within_ideal_range(x, criterion, delta_j)
            denom = self.absolute_distance(A_j, delta_j) + self.absolute_distance(
                delta_j, B_j
            )
            return 1 - (dist / denom) if denom != 0 else 1.0
        else:
            dist = self.distance_outside_ideal_range(x, criterion, delta_j)
            denom = max(
                self.absolute_distance(A_j, delta_j),
                self.absolute_distance(delta_j, B_j),
            )
            return 1 - (dist / denom) if denom != 0 else 0.0

    def calculate_normalized_matrix(self) -> Dict[str, Dict[str, float]]:
        return {
            alt: {
                crit: self.normalize_performance(self.decision_matrix[alt][crit], crit)
                for crit in self.criteria
            }
            for alt in self.alternatives
        }

    def calculate_weighted_normalized_matrix(
        self, normalized_matrix: Dict[str, Dict[str, float]]
    ) -> Dict[str, Dict[str, TriangularFuzzyNumber]]:
        return {
            alt: {
                crit: TriangularFuzzyNumber(
                    normalized_matrix[alt][crit] * self.weights[crit].l,
                    normalized_matrix[alt][crit] * self.weights[crit].m,
                    normalized_matrix[alt][crit] * self.weights[crit].r,
                )
                for crit in self.criteria
            }
            for alt in self.alternatives
        }

    def calculate_ideal_distances(
        self, weighted_matrix: Dict[str, Dict[str, TriangularFuzzyNumber]]
    ) -> Dict[str, Tuple[float, float]]:
        c_star = {}
        d_star = {}
        for crit in self.criteria:
            C_j = self.ideal_ranges[crit][0]
            D_j = self.ideal_ranges[crit][1]
            max_C = max([self.ideal_ranges[c][0].m for c in self.criteria])
            max_D = max([self.ideal_ranges[c][1].m for c in self.criteria])
            c_star[crit] = TriangularFuzzyNumber(
                C_j.l / max_C, C_j.m / max_C, C_j.r / max_C
            )
            d_star[crit] = TriangularFuzzyNumber(
                D_j.l / max_D, D_j.m / max_D, D_j.r / max_D
            )

        return {
            alt: (
                sum(
                    self.absolute_distance(
                        weighted_matrix[alt][crit], self.weights[crit]
                    )
                    for crit in self.criteria
                ),
                sum(
                    max(
                        self.absolute_distance(
                            weighted_matrix[alt][crit], c_star[crit]
                        ),
                        self.absolute_distance(
                            weighted_matrix[alt][crit], d_star[crit]
                        ),
                    )
                    for crit in self.criteria
                ),
            )
            for alt in self.alternatives
        }

    def calculate_relative_indices(
        self, distances: Dict[str, Tuple[float, float]]
    ) -> Dict[str, float]:
        return {
            alt: A_minus / (A_plus + A_minus) if (A_plus + A_minus) != 0 else 0.0
            for alt, (A_plus, A_minus) in distances.items()
        }

    def calculate_normalized_weights(self) -> Dict[str, float]:
        total = sum(w.m for w in self.weights.values())
        return {crit: self.weights[crit].m / total for crit in self.criteria}

    def run(self) -> Dict:
        normalized_matrix = self.calculate_normalized_matrix()
        weighted_matrix = self.calculate_weighted_normalized_matrix(normalized_matrix)
        distances = self.calculate_ideal_distances(weighted_matrix)
        scores = self.calculate_relative_indices(distances)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        weighted_normalized_output = {
            alt: {
                crit: round(weighted_matrix[alt][crit].m, 6) for crit in self.criteria
            }
            for alt in self.alternatives
        }
        return {
            "method": "WFRIM",
            "results": {
                "ranking": [alt for alt, score in ranked],
                "scores": {alt: round(score, 6) for alt, score in scores.items()},
                "normalized_weights": weighted_normalized_output,
            },
        }


if __name__ == "__main__":
    json_data = '''
        {
            "method": "W-FRIM",
            "parameters": {
                "criteria": ["C1", "C2", "C3", "C4", "C5", "C6"],
                "performance_matrix": [
                {
                "name": "A1",
                "values": {
                    "C1": [3.3712, 3.44, 3.5088],
                    "C2": [2.9890, 3.05, 3.1110],
                    "C3": [12.6518, 12.91, 13.1682],
                    "C4": [0.5350, 0.546, 0.5569],
                    "C5": [0.1274, 0.13, 0.1326],
                    "C6": [1.0141, 1.0348, 1.0555]
                }
                },
                {
                "name": "A2",
                "values": {
                    "C1": [3.6750, 3.75, 3.8250],
                    "C2": [3.4202, 3.49, 3.5598],
                    "C3": [12.5146, 12.77, 13.0254],
                    "C4": [0.5390, 0.550, 0.5610],
                    "C5": [0.1372, 0.14, 0.1428],
                    "C6": [1.0127, 1.0333, 1.0540]
                }
                },
                {
                "name": "A3",
                "values": {
                    "C1": [3.7436, 3.82, 3.8964],
                    "C2": [3.0674, 3.13, 3.1926],
                    "C3": [12.3970, 12.65, 12.9030],
                    "C4": [0.5233, 0.534, 0.5446],
                    "C5": [0.1372, 0.14, 0.1428],
                    "C6": [1.0123, 1.033, 1.0537]
                }
                },
                {
                "name": "A4",
                "values": {
                    "C1": [3.8808, 3.96, 4.0392],
                    "C2": [3.1752, 3.24, 3.3048],
                    "C3": [12.6420, 12.90, 13.1580],
                    "C4": [0.5350, 0.546, 0.5569],
                    "C5": [0.1470, 0.15, 0.1530],
                    "C6": [1.0117, 1.0323, 1.0530]
                }
                },
                {
                "name": "A5",
                "values": {
                    "C1": [3.6064, 3.68, 3.7536],
                    "C2": [3.3320, 3.40, 3.4680],
                    "C3": [12.0932, 12.34, 12.5868],
                    "C4": [0.5331, 0.544, 0.5548],
                    "C5": [0.1470, 0.15, 0.1530],
                    "C6": [1.0130, 1.0337, 1.0543]
                }
                },
                {
                "name": "A6",
                "values": {
                    "C1": [2.4304, 2.48, 2.5296],
                    "C2": [3.1850, 3.25, 3.3150],
                    "C3": [11.7992, 12.04, 12.2808],
                    "C4": [0.5380, 0.549, 0.5599],
                    "C5": [0.1470, 0.15, 0.1530],
                    "C6": [1.0186, 1.0394, 1.0602]
                }
                },
                {
                "name": "A7",
                "values": {
                    "C1": [3.5868, 3.66, 3.7332],
                    "C2": [3.1948, 3.26, 3.3252],
                    "C3": [12.0638, 12.31, 12.5562],
                    "C4": [0.5292, 0.540, 0.5508],
                    "C5": [0.1470, 0.15, 0.1530],
                    "C6": [1.0131, 1.0338, 1.0544]
                }
                },
                {
                "name": "A8",
                "values": {
                    "C1": [3.9396, 4.02, 4.1004],
                    "C2": [3.5770, 3.65, 3.7230],
                    "C3": [12.5440, 12.80, 13.0560],
                    "C4": [0.5360, 0.547, 0.5579],
                    "C5": [0.1470, 0.15, 0.1530],
                    "C6": [1.0068, 1.0274, 1.0479]
                }
                },
                {
                "name": "A9",
                "values": {
                    "C1": [3.1850, 3.25, 3.3150],
                    "C2": [3.1262, 3.19, 3.2538],
                    "C3": [11.9560, 12.20, 12.4440],
                    "C4": [0.5448, 0.556, 0.5671],
                    "C5": [0.1470, 0.15, 0.1530],
                    "C6": [1.0150, 1.0357, 1.0565]
                }
                },
                {
                "name": "A10",
                "values": {
                    "C1": [2.9008, 2.96, 3.0192],
                    "C2": [3.4300, 3.50, 3.5700],
                    "C3": [11.8482, 12.09, 12.3318],
                    "C4": [0.5439, 0.555, 0.5661],
                    "C5": [0.1470, 0.15, 0.1530],
                    "C6": [1.0164, 1.0371, 1.0579]
                }
                },
                {
                "name": "A11",
                "values": {
                    "C1": [2.9988, 3.06, 3.1212],
                    "C2": [2.9890, 3.05, 3.1110],
                    "C3": [11.4954, 11.73, 11.9646],
                    "C4": [0.5399, 0.551, 0.5620],
                    "C5": [0.1862, 0.19, 0.1938],
                    "C6": [1.0159, 1.0367, 1.0574]
                }
                }
                ],
                "range": {
                "C1": [[2.4304, 2.4800, 2.5296], [3.9396, 4.0200, 4.1004]],
                "C2": [[2.9890, 3.0500, 3.1110], [3.5770, 3.6500, 3.7230]],
                "C3": [[11.4954, 11.730, 11.9646], [12.6518, 12.9100, 13.1682]],
                "C4": [[0.5233, 0.5340, 0.5446], [0.5440, 0.5560, 0.5671]],
                "C5": [[0.1274, 0.1300, 0.1326], [0.1862, 0.1900, 0.1938]],
                "C6": [[1.0114, 1.0320, 1.0527], [1.0186, 1.0394, 1.0602]]
                },
                "reference_ideal": {
                "C1": [[3.4300, 3.500, 3.5700], [3.9396, 4.0200, 4.1004]],
                "C2": [[3.1360, 3.2000, 3.2640], [3.5770, 3.6500, 3.7230]],
                "C3": [[11.7600, 12.0000, 12.2400], [12.6518, 12.9100, 13.1682]],
                "C4": [[0.5194, 0.5300, 0.5406], [0.5390, 0.5500, 0.5610]],
                "C5": [[0.1470, 0.1500, 0.1530], [0.1764, 0.1800, 0.1836]],
                "C6": [[1.0074, 1.0280, 1.0486], [1.0133, 1.0340, 1.0547]]
                },
                "preferences": {
                "C1": 1,
                "C2": 1,
                "C3": 1,
                "C4": 1,
                "C5": 0,
                "C6": 1
                },
                "weights": {
                "C1": [0.1568, 0.1600, 0.1632],
                "C2": [0.1568, 0.1600, 0.1632],
                "C3": [0.1568, 0.1600, 0.1632],
                "C4": [0.1568, 0.1600, 0.1632],
                "C5": [0.1568, 0.1600, 0.1632],
                "C6": [0.1568, 0.1600, 0.1632]
                }
            } 
            }
    '''
    wfrim = WFRIM(json_data)
    result = wfrim.run()
    print(json.dumps(result, indent=2))
