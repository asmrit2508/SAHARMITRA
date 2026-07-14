import pandas as pd


def recommend_best_vendor(vendor_df):

    df = vendor_df.copy()

    # -------------------------
    # PRICE SCORE
    # -------------------------

    max_price = df["quoted_price_lakhs"].max()
    min_price = df["quoted_price_lakhs"].min()

    if max_price == min_price:
        df["price_score"] = 100
    else:
        df["price_score"] = (
            (max_price - df["quoted_price_lakhs"])
            / (max_price - min_price)
        ) * 100

    # -------------------------
    # QUALITY SCORE
    # -------------------------

    df["quality_component"] = df["quality_score"]

    # -------------------------
    # DELIVERY SCORE
    # -------------------------

    max_delivery = df["delivery_days"].max()
    min_delivery = df["delivery_days"].min()

    if max_delivery == min_delivery:
        df["delivery_component"] = 100
    else:
        df["delivery_component"] = (
            (max_delivery - df["delivery_days"])
            / (max_delivery - min_delivery)
        ) * 100

    # -------------------------
    # WARRANTY SCORE
    # -------------------------

    df["warranty_component"] = (
        df["warranty_years"] / 5
    ) * 100

    # -------------------------
    # VENDOR RATING SCORE
    # -------------------------

    df["rating_component"] = (
        df["vendor_rating"] / 5
    ) * 100

    # -------------------------
    # GEM BONUS
    # -------------------------

    df["gem_bonus"] = df["gem_available"].apply(
        lambda x: 100 if x == "Yes" else 0
    )

    # -------------------------
    # FINAL PROCUREMENT SCORE
    # -------------------------

    df["procurement_score"] = (

        df["price_score"] * 0.35 +

        df["quality_component"] * 0.30 +

        df["delivery_component"] * 0.15 +

        df["warranty_component"] * 0.10 +

        df["rating_component"] * 0.10 +

        df["gem_bonus"] * 0.05

    )

    df = df.sort_values(
        "procurement_score",
        ascending=False
    )

    return df.iloc[0]
