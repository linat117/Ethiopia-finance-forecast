import pandas as pd
#loader logic
def load_events_and_impacts(df):
    events = df[df["record_type"] == "event"].copy()
    impacts = df[df["record_type"] == "impact_link"].copy()
    return events, impacts

#join events - impact links
def merge_event_impacts(events, impacts):
    merged = impacts.merge(
        events[
            ["record_id", "category", "period_start", "source_name"]
        ],
        left_on="parent_id",
        right_on="record_id",
        how="left",
        suffixes=("_impact", "_event")
    )
    return merged
IMPACT_MAP = {
    "low": 0.5,
    "medium": 1.5,
    "high": 3.0
}

def compute_numeric_impact(df):
    df = df.copy()
    mag = df["impact_magnitude"]
    df["impact_pp"] = mag.map(IMPACT_MAP) if mag.dtype == object else mag
    df["impact_pp"] = pd.to_numeric(df["impact_pp"], errors="coerce").fillna(0.1)
    neg = df["impact_direction"].isin(["negative", "decrease"])
    df.loc[neg, "impact_pp"] *= -1
    return df


def apply_event_impacts_over_time(indicator_df, impact_links, duration_months=36):
    """
    Applies lagged and cumulative event impacts to indicator time series.
    Assumption: effect begins after lag_months; accumulates linearly over time; no decay.

    Parameters
    ----------
    indicator_df : pd.DataFrame
        Must have columns: observation_date, value_numeric, indicator_code (optional if single indicator).
    impact_links : pd.DataFrame
        Merged impact_links with events; must have period_start, lag_months, indicator_code,
        and impact magnitude (numeric or categorical). impact_direction for sign.
    duration_months : int
        Months over which total impact is spread (linear accumulation).

    Returns
    -------
    pd.DataFrame
        indicator_df with added column impact_addition (cumulative effect) and value_impacted (baseline + impact).
    """
    ind = indicator_df.copy()
    ind["observation_date"] = pd.to_datetime(ind["observation_date"])
    ind = ind.sort_values("observation_date").reset_index(drop=True)

    links = impact_links.copy()
    if "period_start" not in links.columns and "period_start_event" in links.columns:
        links["period_start"] = links["period_start_event"]
    if "impact_pp" not in links.columns:
        links = compute_numeric_impact(links)
    links["period_start"] = pd.to_datetime(links["period_start"], errors="coerce")
    links["lag_months"] = pd.to_numeric(links["lag_months"], errors="coerce").fillna(0)
    # Filter to this indicator if we have indicator_code
    if "indicator_code" in ind.columns and ind["indicator_code"].nunique() == 1:
        code = ind["indicator_code"].iloc[0]
        links = links[links["indicator_code"] == code]
    elif "indicator_code" in links.columns:
        links = links.dropna(subset=["indicator_code"])

    impact_col = "impact_pp" if "impact_pp" in links.columns else "signed_impact"
    if impact_col not in links.columns:
        links["impact_pp"] = pd.to_numeric(links.get("impact_magnitude", 0), errors="coerce").fillna(0.1)
        impact_col = "impact_pp"

    monthly_effect = links.groupby(["period_start", "lag_months"])[impact_col].sum().reset_index()
    monthly_effect["effect_start"] = monthly_effect["period_start"] + pd.to_timedelta(monthly_effect["lag_months"].astype(int), unit="M")

    def cumulative_impact(obs_date):
        total = 0.0
        for _, row in monthly_effect.iterrows():
            start = row["effect_start"]
            if pd.isna(start) or obs_date < start:
                continue
            months_elapsed = (obs_date - start).days / 30.44
            if months_elapsed <= 0:
                continue
            # Linear accumulation: each month add (total_impact / duration_months)
            add = row[impact_col] * min(months_elapsed / duration_months, 1.0)
            total += add
        return total

    ind["impact_addition"] = ind["observation_date"].map(cumulative_impact)
    ind["value_impacted"] = ind["value_numeric"] + ind["impact_addition"]
    return ind

def spread_impact_over_time(
    event_date,
    impact_pp,
    lag_months,
    duration_months=36
):
    start = pd.to_datetime(event_date) + pd.DateOffset(months=lag_months)
    monthly_effect = impact_pp / duration_months

    timeline = pd.date_range(
        start=start,
        periods=duration_months,
        freq="MS"
    )

    return pd.DataFrame({
        "date": timeline,
        "monthly_effect": monthly_effect
    })

def build_event_indicator_matrix(merged_df):
    """
    Build an Event × Indicator impact matrix.

    Parameters
    ----------
    merged_df : pd.DataFrame
        DataFrame that includes:
        - parent_id (event id)
        - event_name or event_type
        - indicator_code
        - impact_direction
        - impact_magnitude

    Returns
    -------
    pd.DataFrame
        Pivot table: rows = events, columns = indicators,
        values = signed impact magnitude
    """

    df = merged_df.copy()

    # Use indicator_code or related_indicator for matrix columns
    if "indicator_code" not in df.columns or df["indicator_code"].isna().all():
        df = df.rename(columns={"related_indicator": "indicator_code"})
    df["indicator_code"] = df["indicator_code"].fillna(df.get("related_indicator"))

    # Convert direction to numeric sign (include increase/decrease)
    direction_map = {
        "positive": 1, "increase": 1,
        "negative": -1, "decrease": -1,
        "neutral": 0
    }
    df["direction_sign"] = df["impact_direction"].map(direction_map).fillna(0)

    # Magnitude: map categorical to numeric, then signed
    mag = df["impact_magnitude"].copy()
    if mag.dtype == object or mag.dtype.name == "string":
        mag = mag.map(IMPACT_MAP).fillna(pd.to_numeric(mag, errors="coerce")).fillna(0.1)
    else:
        mag = pd.to_numeric(mag, errors="coerce").fillna(0.1)
    df["signed_impact"] = df["direction_sign"] * mag
    df = df.dropna(subset=["indicator_code"])

    # Build matrix
    matrix = df.pivot_table(
        index="parent_id",
        columns="indicator_code",
        values="signed_impact",
        aggfunc="sum",
        fill_value=0
    )

    return matrix

