def summary_by_column(df, column):
    return df[column].value_counts(dropna=False)


def temporal_range(df):
    dates = df["observation_date"].dropna()
    return dates.min(), dates.max()


def confidence_distribution(df):
    return df["confidence"].value_counts()
