REQUIRED_COLUMNS = {
    "record_type",
    "pillar",
    "indicator",
    "indicator_code",
    "value_numeric",
    "observation_date",
    "event_date",
    "category",
    "confidence",
}

def validate_schema(df):
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return True


def record_type_counts(df):
    return df["record_type"].value_counts()


def unique_indicators(df):
    return df.loc[df["record_type"] == "observation", "indicator_code"].unique()
