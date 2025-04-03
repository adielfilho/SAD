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
