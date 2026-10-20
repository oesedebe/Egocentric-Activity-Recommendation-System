# popularity baseline model with popularity calculation for dataset 
import pandas as pd 

train_df = pd.read_csv("../data/processed/train.csv")
train_df.head()
positive_interactions = train_df[train_df["rating"] >= 4]

popularity = (
    positive_interactions
    .groupby("gmap_id")["user_id"]
    .nunique()  
    .reset_index(name="popularity_score")
    .sort_values("popularity_score", ascending=False)
)

def recommend_popularity(user_id, k=10):

    seen = set(
        train_df[
            train_df["user_id"] == user_id
        ]["gmap_id"]
    )

    recommendations = popularity[
        ~popularity["gmap_id"].isin(seen)
    ].head(k).copy()

    recommendations["user_id"] = user_id

    recommendations["rank"] = range(1, len(recommendations) + 1)

    recommendations = recommendations.rename(
        columns={"popularity_score": "score"}
    )

    return recommendations[
        ["user_id", "gmap_id", "score", "rank"]
    ]