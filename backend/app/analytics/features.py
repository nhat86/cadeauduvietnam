WEIGHT = {
"view": 1,
"click": 2,
"purchase": 5
}


def apply_weights(df):
    df["score"] = df["type"].map(WEIGHT)
    return df