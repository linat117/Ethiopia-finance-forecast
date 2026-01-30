REQUIRED_BY_RECORD_TYPE = {
    "observation": {
        "record_type",
        "indicator_code",
        "value_numeric",
        "observation_date",
        "source_name",
        "confidence",
    },
    "event": {
        "record_type",
        "category",
        "period_start",
        "source_name",
        "confidence",
    },
    "impact_link": {
        "record_type",
        "parent_id",
        "related_indicator",
        "impact_direction",
    },
    "target": {
        "record_type",
        "indicator_code",
        "value_numeric",
        "fiscal_year",
    },
}


def validate_schema(df):
    errors = []

    for record_type, required_cols in REQUIRED_BY_RECORD_TYPE.items():
        subset = df[df["record_type"] == record_type]

        if subset.empty:
            continue

        missing = required_cols - set(subset.columns)
        if missing:
            errors.append(
                f"{record_type}: missing columns {missing}"
            )

    if errors:
        raise ValueError("Schema validation failed:\n" + "\n".join(errors))

    return True
