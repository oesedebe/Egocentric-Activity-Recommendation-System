
import pandas as pd

PRICE_LEVELS = {
    "$": 1,
    "$$": 2,
    "$$$": 3,
    "$$$$": 4
}


def get_budget_score(price, max_budget):
    """Return +1, 0, or -1 for budget compatibility."""

    if pd.isna(price):
        return 0.0

    price_level = PRICE_LEVELS.get(price)

    if price_level is None:
        return 0.0

    return 1.0 if price_level <= max_budget else -1.0


def add_budget_scores(candidates, max_budget):
    """Add budget compatibility scores to candidates."""

    df = candidates.copy()

    df["budget_score"] = df["price"].apply(
        lambda price: get_budget_score(
            price,
            max_budget
        )
    )

    return df
