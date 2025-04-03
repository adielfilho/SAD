# -*- coding: utf-8 -*-


def get_decision_matrix_from_json(alternatives, criteria):
    decision_matrix = []
    for alt in alternatives:
        row = [tuple(alt["values"][crit]) for crit in criteria]
        decision_matrix.append(row)
    return decision_matrix


def get_lower_bound_ranges_and_reference_ideal_pairs_from_json(
    range_data, reference_data, criteria
):
    lower_bound_ranges = []
    reference_ideal_pairs = []
    for crit in criteria:
        lower_bound = tuple(range_data[crit][0])
        ref_lower = tuple(reference_data[crit][0])
        ref_upper = tuple(reference_data[crit][1])
        lower_bound_ranges.append(lower_bound)
        reference_ideal_pairs.append((ref_lower, ref_upper))
    return lower_bound_ranges, reference_ideal_pairs


def get_preference_lambdas_from_json(preferences, criteria):
    return [preferences[crit] for crit in criteria]


def get_criterion_weights_from_json(weights, criteria):
    return [tuple(weights[crit]) for crit in criteria]


def get_all_parameters(parameters,criteria):
    decision_matrix = get_decision_matrix_from_json(
        parameters["performance_matrix"], criteria
    )
    lower_bound_ranges, reference_ideal_pairs = (
        get_lower_bound_ranges_and_reference_ideal_pairs_from_json(
            parameters["range"], parameters["reference_ideal"], criteria
        )
    )
    preference_lambdas = get_preference_lambdas_from_json(
        parameters["preferences"], criteria
    )
    criterion_weights = get_criterion_weights_from_json(parameters["weights"], criteria)
    return (
        decision_matrix,
        lower_bound_ranges,
        reference_ideal_pairs,
        preference_lambdas,
        criterion_weights,
    )
