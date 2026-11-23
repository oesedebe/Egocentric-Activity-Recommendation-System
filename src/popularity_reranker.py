import numpy as np

POPULARITY_GROUPS = ['Long-tail', 'Mid-tail', 'Popular']

def popularity_rerank_integrated(
    user_candidates,
    lambda_weight=0.7,
    k=10,
    relevance_column='bpr_normalized'
):
    if not 0 <= lambda_weight <= 1:
        raise ValueError("lambda_weight must be between 0 and 1")

    if relevance_column not in user_candidates.columns:
        raise ValueError(
            f"Missing relevance column: {relevance_column}"
        )

    candidates = user_candidates.copy()

    if len(candidates) < k:
        raise ValueError("Not enough candidates for requested k")

    target = candidates[
        ['long_tail_preference',
         'mid_tail_preference',
         'popular_preference']
    ].iloc[0].to_numpy(dtype=float)

    selected_indices = []
    selected_counts = np.zeros(3, dtype=int)

    for position in range(k):

        best_index = None
        best_score = -np.inf

        for idx, candidate in candidates.iterrows():

            if idx in selected_indices:
                continue

            group_index = POPULARITY_GROUPS.index(
                candidate['popularity_group']
            )

            new_counts = selected_counts.copy()
            new_counts[group_index] += 1

            new_distribution = new_counts / (position + 1)

            calibration_error = (
                0.5 * np.abs(target - new_distribution).sum()
            )

            relevance = float(candidate[relevance_column])

            combined_score = (
                (1 - lambda_weight) * relevance
                - lambda_weight * calibration_error
            )

            if combined_score > best_score:
                best_score = combined_score
                best_index = idx

        selected_indices.append(best_index)

        chosen_group = candidates.loc[
            best_index, 'popularity_group'
        ]

        selected_counts[
            POPULARITY_GROUPS.index(chosen_group)
        ] += 1

    reranked = candidates.loc[selected_indices].copy()
    reranked['reranked_rank'] = range(1, k + 1)

    return reranked
