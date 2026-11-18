
from geopy.distance import geodesic
import pandas as pd


def calculate_distance(user_location, activity_location):
    """Return straight-line geographic distance in miles."""
    return geodesic(user_location, activity_location).miles


def distance_score(distance_miles, radius_miles):
    """Score distance compatibility between -1 and 1."""
    if radius_miles <= 0:
        raise ValueError("Radius must be positive")

    if pd.isna(distance_miles):
        return 0.0

    return max(-1.0, 1.0 - distance_miles / radius_miles)


def add_distance_scores(candidates, user_location, radius_miles):
    """Add distance information to BPR candidates."""
    df = candidates.copy()

    def get_distance(row):
        if pd.isna(row["latitude"]) or pd.isna(row["longitude"]):
            return float("nan")

        return calculate_distance(
            user_location,
            (row["latitude"], row["longitude"])
        )

    df["distance_miles"] = df.apply(get_distance, axis=1)

    df["distance_score"] = df["distance_miles"].apply(
        lambda d: distance_score(d, radius_miles)
    )

    return df

def hybrid_distance_rerank(
    candidates,
    user_location,
    radius_miles,
    k=10
):
    df = add_distance_scores(
        candidates,
        user_location,
        radius_miles
    )

    nearby = df[
        df["distance_miles"] <= radius_miles
    ].sort_values("bpr_normalized", ascending=False)

    fallback = df[
        ~(df["distance_miles"] <= radius_miles)
    ].sort_values("bpr_normalized", ascending=False)

    selected = nearby.head(k)

    remaining = k - len(selected)

    if remaining > 0:
        selected = pd.concat(
            [selected, fallback.head(remaining)]
        )

    return selected.reset_index(drop=True)