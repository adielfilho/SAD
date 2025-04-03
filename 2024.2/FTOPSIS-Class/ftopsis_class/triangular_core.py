import pandas as pd
import numpy as np
from enum import Enum


class CriteriaType(Enum):
    Cost = 0
    Benefit = 1


class FTOPSISClass:
    @staticmethod
    def normalize_matrix(
        matrix: pd.DataFrame, criteria_type: dict[str, CriteriaType]
    ) -> pd.DataFrame:
        criteria = list(matrix.columns)

        min_value = []
        max_value = []

        fuzzy_decision_matrix = {}
        division_dictionary = {}

        for x in criteria:
            Type = criteria_type[x]
            if Type == CriteriaType.Cost:
                for i in matrix[x]:
                    min_value.append(min(i))
                division_dictionary[x] = min(min_value)

            elif Type == CriteriaType.Benefit:
                for i in matrix[x]:
                    max_value.append(max(i))
                division_dictionary[x] = max(max_value)

        for y in matrix:
            Type = criteria_type[y]

            if Type == CriteriaType.Cost:
                normalized_fuzzy_number = division_dictionary[y] / matrix[y]
                normalized_list = list(
                    map(
                        lambda row: np.nan_to_num(row, nan=0.0).tolist(),
                        normalized_fuzzy_number,
                    )
                )
                fuzzy_decision_matrix[y] = normalized_list
            elif Type == CriteriaType.Benefit:
                normalized_fuzzy_number = np.nan_to_num(
                    matrix[y] / division_dictionary[y]
                )
                normalized_list = list(
                    map(
                        lambda row: np.nan_to_num(row, nan=0.0).tolist(),
                        normalized_fuzzy_number,
                    )
                )
                fuzzy_decision_matrix[y] = normalized_list

        normalized_decision_matrix = pd.DataFrame(fuzzy_decision_matrix)
        return normalized_decision_matrix

    @staticmethod
    def weigh_matrix(
        df_normalized_matrix: pd.DataFrame, df_vector_weights: pd.DataFrame
    ) -> pd.DataFrame:
        matrix_weight_data = {}

        for col in range(len(df_normalized_matrix.columns)):
            for lin in range(len(df_normalized_matrix)):

                name_column = df_normalized_matrix.columns[col]
                name_column_weights = df_vector_weights.columns[col]

                fuzzy_number = df_normalized_matrix.loc[lin, name_column]
                weight = df_vector_weights.loc[0, name_column_weights]

                weighted_number = fuzzy_number * weight
                key = name_column

                if key not in matrix_weight_data:
                    matrix_weight_data[key] = []
                matrix_weight_data[key].append(weighted_number)

        w_n_matrix = pd.DataFrame(matrix_weight_data)
        weighted_normalized_matrix = FTOPSISClass.round_weighted_normalized_matrix(
            w_n_matrix
        )
        return weighted_normalized_matrix

    @staticmethod
    def round_weighted_normalized_matrix(
        df_weighted_normalized_matrix: pd.DataFrame,
    ) -> pd.DataFrame:
        matrix_data = {}

        for i in df_weighted_normalized_matrix:
            array = []
            for j in df_weighted_normalized_matrix[i]:
                number = np.round(j, 4)
                array.append(number)
            matrix_data[i] = array

        normalized_weighted_rounded_matrix = pd.DataFrame(matrix_data)
        return normalized_weighted_rounded_matrix

    @staticmethod
    def ideal_solution(
        df_profile_matrix: pd.DataFrame, profile_mapping: dict[int, str]
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        positive_ideal_solution_data = {}
        negative_ideal_solution_data = {}

        for index, _ in df_profile_matrix.iterrows():
            positive_ideal_solution_data[f"{profile_mapping[index]}"] = (
                df_profile_matrix.iloc[index]
            )

            if index == 0:
                negative_ideal_solution_data[f"{profile_mapping[index]}"] = (
                    df_profile_matrix.iloc[-1]
                )

            elif index != 0 and index != len(df_profile_matrix) - 1:
                negative_ideal_solution_data[f"{profile_mapping[index]}"] = (
                    df_profile_matrix.iloc[-1]
                )

            else:
                negative_ideal_solution_data[f"{profile_mapping[index]}"] = (
                    df_profile_matrix.iloc[0]
                )

        positive_ideal_solution = pd.DataFrame(positive_ideal_solution_data)
        negative_ideal_solution = pd.DataFrame(negative_ideal_solution_data)

        return positive_ideal_solution, negative_ideal_solution

    def distance_calculation(
        matrix: pd.DataFrame,
        df_positive_solution: pd.DataFrame,
        df_negative_solution: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        positive_distance_data = {}
        negative_distance_data = {}

        for i in range(len(matrix)):
            alt = list(matrix.iloc[i])

            for j in df_positive_solution:
                positive_solution = list(df_positive_solution[j])
                distance = FTOPSISClass.euclidean_distance(alt, positive_solution)

                if j not in positive_distance_data:
                    positive_distance_data[j] = []
                positive_distance_data[j].append(sum(distance))

            for j in df_negative_solution:
                negative_solution = list(df_negative_solution[j])
                distance = FTOPSISClass.euclidean_distance(alt, negative_solution)

                if j not in negative_distance_data:
                    negative_distance_data[j] = []
                negative_distance_data[j].append(sum(distance))

        positive_distance = pd.DataFrame(positive_distance_data)
        negative_distance = pd.DataFrame(negative_distance_data)

        return positive_distance, negative_distance

    def euclidean_distance(v1: list[float], v2: list[float]) -> list[float]:
        distance = []

        for v1, v2 in zip(v1, v2):
            d = np.sqrt(1 / len(v1) * sum((x - y) ** 2 for x, y in zip(v1, v2)))
            distance.append(d)

        return distance

    def proximity_coefficient(
        positive_distances: pd.DataFrame, negative_distances: pd.DataFrame
    ) -> pd.DataFrame:
        result = {}

        for col in range(len(positive_distances.columns)):
            for lin in range(len(positive_distances)):
                column_name_p = positive_distances.columns[col]
                column_name_n = negative_distances.columns[col]

                a = positive_distances.loc[lin, column_name_p]
                b = negative_distances.loc[lin, column_name_n]

                calculation = np.divide(b, (a + b))

                key = column_name_p

                if key not in result:
                    result[key] = []
                result[key].append(calculation)

        f_result = pd.DataFrame(result)
        return f_result
