"""
Simple forecasting utilities for Task 4: baseline trend, event-augmented, and scenario analysis.
No ML models; linear regression only (appropriate for sparse, low-frequency data).
"""
import pandas as pd
import numpy as np
from typing import Tuple, Optional


def _extract_series(obs: pd.DataFrame, indicator_code: str) -> Tuple[np.ndarray, np.ndarray]:
    """Extract year and value_numeric for an indicator. Returns (years, values)."""
    df = obs[obs["indicator_code"] == indicator_code].copy()
    df["observation_date"] = pd.to_datetime(df["observation_date"])
    df["year"] = df["observation_date"].dt.year
    df = df.dropna(subset=["value_numeric", "year"]).sort_values("year")
    years = df["year"].values.astype(float)
    values = df["value_numeric"].values.astype(float)
    return years, values


def baseline_trend_forecast(
    obs: pd.DataFrame,
    indicator_code: str,
    forecast_years: list,
    confidence: float = 0.95,
) -> pd.DataFrame:
    """
    Linear regression of value_numeric on year. Returns point forecast and lower/upper bounds.
    """
    years, values = _extract_series(obs, indicator_code)
    if len(years) < 2:
        # Not enough data: flat line at last value or mean
        point = float(values[-1]) if len(values) else np.nan
        out = []
        for y in forecast_years:
            out.append({"year": y, "forecast": point, "lower": point, "upper": point})
        return pd.DataFrame(out)
    # OLS: value = a + b * year
    x = np.column_stack([np.ones_like(years), years])
    beta, res, rank, s = np.linalg.lstsq(x, values, rcond=None)
    a, b = beta[0], beta[1]
    n = len(years)
    y_mean = years.mean()
    mse = ((values - (a + b * years)) ** 2).sum() / max(n - 2, 1)
    t_val = 1.96 if n <= 3 else min(2.0, 1.96 + 0.5 / (n - 2))  # approximate t for small n
    out = []
    for y in forecast_years:
        y_f = float(a + b * y)
        se_sq = mse * (1 + 1 / n + (y - y_mean) ** 2 / max(((years - y_mean) ** 2).sum(), 1e-6))
        se = np.sqrt(max(se_sq, 0))
        half = t_val * se
        out.append({"year": y, "forecast": y_f, "lower": y_f - half, "upper": y_f + half})
    return pd.DataFrame(out)


def event_impact_additions(
    forecast_years: list,
    events: pd.DataFrame,
    impact_links: pd.DataFrame,
    scale: float = 1.0,
    indicator_code: Optional[str] = None,
) -> np.ndarray:
    """
    For each forecast year, compute cumulative event impact (sum of scaled effects).
    If indicator_code is given, filter impact_links to that indicator.
    """
    events = events.copy()
    events["period_start"] = pd.to_datetime(events["period_start"], errors="coerce")
    impact_links = impact_links.copy()
    if indicator_code:
        if "indicator_code" in impact_links.columns:
            mask = impact_links["indicator_code"] == indicator_code
        else:
            mask = pd.Series(False, index=impact_links.index)
        if "related_indicator" in impact_links.columns:
            mask = mask | (impact_links["related_indicator"] == indicator_code)
        if mask.any():
            impact_links = impact_links[mask]
    if events.empty or impact_links.empty:
        return np.zeros(len(forecast_years))
    if "record_id" not in events.columns or "period_start" not in events.columns:
        return np.zeros(len(forecast_years))
    merged = impact_links.merge(
        events[["record_id", "period_start"]],
        left_on="parent_id",
        right_on="record_id",
        how="left",
    )
    # Magnitude: numeric or map low/medium/high
    mag_map = {"low": 0.5, "medium": 1.5, "high": 3.0}
    def num_mag(m):
        if pd.isna(m): return 0.5
        if isinstance(m, (int, float)): return float(m)
        return mag_map.get(str(m).lower(), 0.5)
    merged["mag"] = merged.get("impact_magnitude", pd.Series(dtype=float)).map(num_mag)
    dir_sign = merged.get("impact_direction", pd.Series(dtype=object)).replace(
        {"positive": 1, "increase": 1, "negative": -1, "decrease": -1}
    ).fillna(1)
    merged["sign"] = np.where(dir_sign.astype(str).str.lower().str.contains("neg|dec"), -1, 1)
    merged["effect"] = merged["sign"] * merged["mag"] * scale
    merged["lag_months"] = pd.to_numeric(merged.get("lag_months", 0), errors="coerce").fillna(0)
    additions = np.zeros(len(forecast_years))
    for _, row in merged.iterrows():
        start = row["period_start"]
        if pd.isna(start):
            continue
        start_year = start.year + int(row["lag_months"] // 12)
        effect_per_year = row["effect"] / 3.0  # spread over ~3 years
        for i, y in enumerate(forecast_years):
            if y >= start_year:
                years_since = min(y - start_year + 1, 3)
                additions[i] += effect_per_year * years_since
    return additions


def event_augmented_forecast(
    obs: pd.DataFrame,
    indicator_code: str,
    forecast_years: list,
    events: pd.DataFrame,
    impact_links: pd.DataFrame,
    event_scale: float = 1.0,
    confidence: float = 0.95,
) -> pd.DataFrame:
    """Baseline trend plus cumulative event impacts. Returns forecast table with lower/upper."""
    base = baseline_trend_forecast(obs, indicator_code, forecast_years, confidence)
    additions = event_impact_additions(forecast_years, events, impact_links, scale=event_scale, indicator_code=indicator_code)
    base["forecast"] = base["forecast"] + additions
    base["lower"] = base["lower"] + additions * 0.8  # wider band
    base["upper"] = base["upper"] + additions * 1.2
    return base


def scenario_forecasts(
    obs: pd.DataFrame,
    indicator_code: str,
    forecast_years: list,
    events: pd.DataFrame,
    impact_links: pd.DataFrame,
) -> pd.DataFrame:
    """
    Three scenarios: pessimistic (low trend, low event effectiveness), base, optimistic.
    Returns long-format table: year, scenario, forecast, lower, upper.
    """
    base_trend = baseline_trend_forecast(obs, indicator_code, forecast_years, confidence=0.68)
    rows = []
    for i, y in enumerate(forecast_years):
        pt = base_trend.loc[base_trend["year"] == y, "forecast"].iloc[0]
        lo = base_trend.loc[base_trend["year"] == y, "lower"].iloc[0]
        hi = base_trend.loc[base_trend["year"] == y, "upper"].iloc[0]
        add_pess = event_impact_additions([y], events, impact_links, scale=0.5, indicator_code=indicator_code)[0]
        add_base = event_impact_additions([y], events, impact_links, scale=1.0, indicator_code=indicator_code)[0]
        add_opt = event_impact_additions([y], events, impact_links, scale=1.5, indicator_code=indicator_code)[0]
        # Pessimistic: lower trend, low event effect
        rows.append({"indicator": indicator_code, "year": y, "scenario": "pessimistic", "forecast": pt * 0.95 + add_pess, "lower": lo * 0.9 + add_pess * 0.8, "upper": pt * 0.95 + add_pess * 1.2})
        rows.append({"indicator": indicator_code, "year": y, "scenario": "base", "forecast": pt + add_base, "lower": lo + add_base * 0.9, "upper": hi + add_base * 1.1})
        rows.append({"indicator": indicator_code, "year": y, "scenario": "optimistic", "forecast": pt * 1.05 + add_opt, "lower": pt * 1.02 + add_opt * 0.9, "upper": hi * 1.1 + add_opt * 1.2})
    return pd.DataFrame(rows)
