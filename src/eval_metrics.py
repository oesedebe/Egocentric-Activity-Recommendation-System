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

""""
* to calculate avg recall hit rate and ndcg, replace MODEL_NAME with model
* eligible users are users that are present in both test and train set 

import random
test_pos = test_df[test_df["rating"] >= 4]

eligible_users = list(
    set(train_df["user_id"]) &
    set(test_pos["user_id"])
)

random.seed(42)

sample_size = min(1000, len(eligible_users))
evaluation_users = random.sample(eligible_users, sample_size)

relevant_by_user = (
    test_pos
    .groupby("user_id")["gmap_id"]
    .apply(set)
    .to_dict()
)
hit_scores, recall_scores, ndcg_scores = [], [], []

for user_id in evaluation_users:

    recs = MODEL_NAME(user_id, k=10)
    recommended = recs["gmap_id"].tolist()

    relevant = set(
        test_pos[
            test_pos["user_id"] == user_id
        ]["gmap_id"]
    )

    recall_scores.append(
        recall_at_k(recommended, relevant, 10)
    )

    hit_scores.append(
        hit_rate_at_k(recommended, relevant, 10)
    )

    ndcg_scores.append(
        ndcg_at_k(recommended, relevant, 10)
    )

avg_recall = sum(recall_scores) / len(recall_scores)
avg_hit = sum(hit_scores) / len(hit_scores)
avg_ndcg = sum(ndcg_scores) / len(ndcg_scores)

print("Recall@10:", avg_recall)
print("Hit Rate@10:", avg_hit)
print("NDCG@10:", avg_ndcg)

"""