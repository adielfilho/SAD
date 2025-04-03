from __future__ import annotations
import json
from typing import Dict, Tuple, Union


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
    def __init__(self, input_file: Union[dict, str] = None):
        self.alternatives = []
        self.criteria = []
        self.decision_matrix = {}
        self.weights = {}
        self.ranges = {}
        self.ideal_ranges = {}
        self.lambdas = {}

        if input_file:
            if type(input_file) == dict: input_file = json.dumps(input_file)
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
