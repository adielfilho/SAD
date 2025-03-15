import pandas as pd
import numpy as np
import math

def get_decision_matrix(df_table1):
    decision_matrix = []
    num_criteria = len([col for col in df_table1.columns if col.endswith("_l")])

    for _, row in df_table1.iterrows():
        alt_fuzzy_numbers = []
        for crit in range(1, num_criteria + 1):
            col_l = f"C{crit}_l"
            col_m = f"C{crit}_m"
            col_u = f"C{crit}_u"
            fuzzy_num = (row[col_l], row[col_m], row[col_u])
            alt_fuzzy_numbers.append(fuzzy_num)
        decision_matrix.append(alt_fuzzy_numbers)
    return decision_matrix


def get_lower_bound_ranges_and_reference_ideal_pairs(df_table2):
    """
    For each criterion, we extract:
    lower_bound_range = (Range_A_l, Range_A_m, Range_A_u)
    reference_ideal_pair = ((RefIdeal_C_l, RefIdeal_C_m, RefIdeal_C_u), (RefIdeal_D_l, RefIdeal_D_m, RefIdeal_D_u))
    """
    lower_bound_ranges = []
    reference_ideal_pairs = []

    for _, row in df_table2.iterrows():
        lower_bound = (row["Range_A_l"], row["Range_A_m"], row["Range_A_u"])
        ref_lower = (row["RefIdeal_C_l"], row["RefIdeal_C_m"], row["RefIdeal_C_u"])
        ref_upper = (row["RefIdeal_D_l"], row["RefIdeal_D_m"], row["RefIdeal_D_u"])
        lower_bound_ranges.append(lower_bound)
        reference_ideal_pairs.append((ref_lower, ref_upper))

    return lower_bound_ranges, reference_ideal_pairs


def get_preference_lambdas(df_table3):
    df_table3_sorted = df_table3.sort_values(by="Criterion")
    preference_lambdas = df_table3_sorted["Lambda"].tolist()
    return preference_lambdas


def get_criterion_weights(df_table4):
    df_weights = df_table4.sort_values("Criterion")
    criterion_weights = []
    for _, row in df_weights.iterrows():
        weight = (row["Weight_l"], row["Weight_m"], row["Weight_u"])
        criterion_weights.append(weight)
    return criterion_weights


class WeightedFuzzyReferenceIdealMethod:
    def __init__(
        self,
        decision_matrix,
        criterion_weights,
        lower_bound_ranges,
        reference_ideal_pairs,
        preference_lambdas,
    ):
        self.decision_matrix = decision_matrix
        self.criterion_weights = criterion_weights
        self.lower_bound_ranges = lower_bound_ranges
        self.reference_ideal_pairs = reference_ideal_pairs
        self.preference_lambdas = preference_lambdas

        self.num_alternatives = len(decision_matrix)
        self.num_criteria = len(decision_matrix[0])

        self.weighted_reference_ideals = self._calculate_weighted_reference_ideal_list()
        self.normalized_decision_matrix = None
        self.weighted_normalized_matrix = None
        self.relative_indices = None
        self.alternative_ranking = None

    @staticmethod
    def calculate_fuzzy_distance(fuzzy_number1, fuzzy_number2):
        return (
            abs(fuzzy_number1[0] - fuzzy_number2[0])
            + abs(fuzzy_number1[1] - fuzzy_number2[1])
            + abs(fuzzy_number1[2] - fuzzy_number2[2])
        ) / 3.0

    @staticmethod
    def calculate_adjusted_distance(
        fuzzy_value, weighted_reference, reference_lower, reference_upper
    ):
        denominator = 1 + abs(reference_lower[0] - reference_upper[2])
        distance_lower = abs(fuzzy_value[0] - weighted_reference[0]) / denominator
        distance_middle = abs(fuzzy_value[1] - weighted_reference[1])
        distance_upper = abs(fuzzy_value[2] - weighted_reference[2]) / denominator
        return distance_lower + distance_middle + distance_upper

    @staticmethod
    def is_value_in_reference_interval(fuzzy_value, reference_lower, reference_upper):
        return reference_lower[1] <= fuzzy_value[1] <= reference_upper[1]

    @staticmethod
    def are_floats_nearly_equal(value1, value2, tolerance=1e-6):
        return abs(value1 - value2) < tolerance

    def _calculate_weighted_reference_ideal_list(self):
        weighted_reference_list = []
        for j in range(self.num_criteria):
            ref_lower, ref_upper = self.reference_ideal_pairs[j]
            lam = self.preference_lambdas[j]
            delta_lower = ref_lower[0]
            delta_middle = (1 - lam) * ref_lower[1] + lam * ref_upper[1]
            delta_upper = ref_upper[2]
            weighted_reference_list.append((delta_lower, delta_middle, delta_upper))
        return weighted_reference_list

    def _calculate_normalized_value(
        self,
        fuzzy_performance,
        lower_bound_range,
        weighted_reference,
        ref_lower,
        ref_upper,
    ):
        tolerance = 1e-6
        if self.are_floats_nearly_equal(
            fuzzy_performance[1], weighted_reference[1], tolerance
        ):
            return 1.0

        base_distance = self.calculate_fuzzy_distance(
            lower_bound_range, weighted_reference
        )
        if self.are_floats_nearly_equal(base_distance, 0, tolerance):
            return 1.0

        if self.is_value_in_reference_interval(fuzzy_performance, ref_lower, ref_upper):
            normalized_value = 1 - (
                self.calculate_adjusted_distance(
                    fuzzy_performance, weighted_reference, ref_lower, ref_upper
                )
                / (2 * base_distance)
            )
        else:
            normalized_value = 1 - (
                self.calculate_fuzzy_distance(fuzzy_performance, weighted_reference)
                / base_distance
            )
        return max(0, min(normalized_value, 1))

    def compute_normalized_decision_matrix(self):
        N = np.zeros((self.num_alternatives, self.num_criteria))
        for alt in range(self.num_alternatives):
            for crit in range(self.num_criteria):
                perf = self.decision_matrix[alt][crit]
                lower_bound = self.lower_bound_ranges[crit]
                weighted_ref = self.weighted_reference_ideals[crit]
                ref_lower, ref_upper = self.reference_ideal_pairs[crit]
                N[alt, crit] = self._calculate_normalized_value(
                    perf, lower_bound, weighted_ref, ref_lower, ref_upper
                )
        self.normalized_decision_matrix = N
        return N

    def compute_weighted_normalized_matrix(self):
        if self.normalized_decision_matrix is None:
            self.compute_normalized_decision_matrix()
        weight_middles = np.array([w[1] for w in self.criterion_weights])
        P = self.normalized_decision_matrix * weight_middles
        self.weighted_normalized_matrix = P
        return P

    def compute_relative_indices(self):
        if self.weighted_normalized_matrix is None:
            self.compute_weighted_normalized_matrix()
        weight_middles = np.array([w[1] for w in self.criterion_weights])
        A_plus = np.zeros(self.num_alternatives)
        A_minus = np.zeros(self.num_alternatives)
        for i in range(self.num_alternatives):
            sum_plus = 0
            sum_minus = 0
            for j in range(self.num_criteria):
                sum_plus += (
                    self.weighted_normalized_matrix[i, j] - weight_middles[j]
                ) ** 2
                sum_minus += (self.weighted_normalized_matrix[i, j]) ** 2
            A_plus[i] = math.sqrt(sum_plus)
            A_minus[i] = math.sqrt(sum_minus)
        self.relative_indices = []
        for i in range(self.num_alternatives):
            denom = A_plus[i] + A_minus[i]
            rel_index = 0 if denom == 0 else A_minus[i] / denom
            self.relative_indices.append(rel_index)
        return self.relative_indices

    def rank_alternatives(self):
        if self.relative_indices is None:
            self.compute_relative_indices()
        self.alternative_ranking = sorted(
            list(enumerate(self.relative_indices)),
            key=lambda item: item[1],
            reverse=True,
        )
        return self.alternative_ranking

    def run_w_frim(self):
        self.compute_normalized_decision_matrix()
        self.compute_weighted_normalized_matrix()
        self.compute_relative_indices()
        self.rank_alternatives()
        return (
            self.alternative_ranking,
            self.relative_indices,
            self.normalized_decision_matrix,
            self.weighted_normalized_matrix,
        )


if __name__ == "__main__":
    df_table1 = pd.read_csv("data/table1_fuzzy_decision_matrix.csv")
    df_table2 = pd.read_csv("data/table2_range_reference_ideal.csv")
    df_table3 = pd.read_csv("data/table3_preference_structure.csv")
    df_table4 = pd.read_csv("data/table4_criterion_weights.csv")
    
    decision_matrix = get_decision_matrix(df_table1)
    lower_bound_ranges, reference_ideal_pairs = (
        get_lower_bound_ranges_and_reference_ideal_pairs(df_table2)
    )
    preference_lambdas = get_preference_lambdas(df_table3)
    criterion_weights = get_criterion_weights(df_table4)

    model = WeightedFuzzyReferenceIdealMethod(
        decision_matrix,
        criterion_weights,
        lower_bound_ranges,
        reference_ideal_pairs,
        preference_lambdas,
    )

    ranking, relative_indices, normalized_matrix, weighted_matrix = model.run_w_frim()

    # np.set_printoptions(precision=4, suppress=True)
    print("Normalized Decision Matrix (N):")
    print(normalized_matrix)
    print("\nWeighted Normalized Decision Matrix (P):")
    print(weighted_matrix)
    print("\nRelative Indices for Alternatives:")
    for idx, rel in enumerate(relative_indices):
        print(f"Alternative A{idx+1}: {rel:.6f}")
    print("\nRanking of Alternatives (Best First):")
    for rank, (idx, rel) in enumerate(ranking, start=1):
        print(f"Rank {rank}: Alternative A{idx+1} (Relative Index = {rel:.6f})")
