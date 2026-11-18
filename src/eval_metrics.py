# evaluation functions for recall, ndcg, hitrate
import math

def recall_at_k(recommended, relevant, k):
    recommended_k = recommended[:k]

    if len(relevant) == 0:
        return None

    hits = len(set(recommended_k) & set(relevant))

    return hits / len(relevant)


def ndcg_at_k(recommended, relevant, k):
    recommended_k = recommended[:k]

    if len(relevant) == 0:
        return None

    # Actual DCG
    dcg = 0
    for i, item in enumerate(recommended_k):
        if item in relevant:
            dcg += 1 / math.log2(i + 2)

    # Best possible DCG
    ideal_hits = min(len(relevant), k)

    idcg = sum(
        1 / math.log2(i + 2)
        for i in range(ideal_hits)
    )

    return dcg / idcg


def hit_rate_at_k(recommended, relevant, k):
    recommended_k = recommended[:k]

    if len(relevant) == 0:
        return None

    hits = set(recommended_k) & set(relevant)

    if len(hits) > 0:
        return 1
    else:
        return 0


def calculate_metrics(recommended, relevant, k=10):

    recall = recall_at_k(recommended, relevant, k)
    hit_rate = hit_rate_at_k(recommended, relevant, k)
    ndcg = ndcg_at_k(recommended, relevant, k)

    return {
        f"Recall@{k}": recall,
        f"HitRate@{k}": hit_rate,
        f"NDCG@{k}": ndcg
    }
