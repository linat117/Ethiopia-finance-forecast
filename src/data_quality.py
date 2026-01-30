import pandas as pd

def missing_value_summary(df):
    """Return % of missing values per column."""
    return df.isna().mean().mul(100).sort_values(ascending=False)

def record_type_distribution(df):
    """Count of records by record_type."""
    return df["record_type"].value_counts()

def indicator_coverage(df):
    """Count observations per indicator_code."""
    return df.groupby("indicator_code").size().sort_values(ascending=False)

def confidence_distribution(df):
    """Distribution of confidence levels per record type."""
    return df.groupby("record_type")["confidence"].value_counts(normalize=True).unstack().fillna(0)
