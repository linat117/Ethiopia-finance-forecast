"""
Execute data enrichment: add observations, events, and impact_links
following the schema. Saves enriched dataset to data/processed/.
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
from src.data_loading import load_unified_dataset
from src.schema_checks import validate_schema


def _base_row(columns: list) -> dict:
    """Return a row dict with NaN for all columns."""
    return {c: None for c in columns}


def _add_observation(
    rows: list,
    record_id: int,
    indicator_code: str,
    value_numeric: float,
    observation_date: str,
    source_name: str,
    source_url: str,
    confidence: str,
    collected_by: str,
    collection_date: str,
    notes: str,
    columns: list,
    **kwargs,
) -> None:
    """Append an observation row following schema."""
    row = _base_row(columns)
    row.update({
        "record_id": record_id,
        "record_type": "observation",
        "indicator_code": indicator_code,
        "value_numeric": value_numeric,
        "observation_date": pd.to_datetime(observation_date),
        "source_name": source_name,
        "source_url": source_url,
        "confidence": confidence,
        "collected_by": collected_by,
        "collection_date": collection_date,
        "notes": notes,
        **kwargs,
    })
    rows.append(row)


def _add_event(
    rows: list,
    record_id: int,
    category: str,
    period_start: str,
    source_name: str,
    source_url: str,
    confidence: str,
    collected_by: str,
    collection_date: str,
    notes: str,
    columns: list,
) -> None:
    """Append an event row following schema."""
    row = _base_row(columns)
    row.update({
        "record_id": record_id,
        "record_type": "event",
        "category": category,
        "period_start": pd.to_datetime(period_start),
        "source_name": source_name,
        "source_url": source_url,
        "confidence": confidence,
        "collected_by": collected_by,
        "collection_date": collection_date,
        "notes": notes,
    })
    rows.append(row)


def _add_impact_link(
    rows: list,
    record_id: int,
    parent_id: int,
    related_indicator: str,
    impact_direction: str,
    columns: list,
) -> None:
    """Append an impact_link row following schema."""
    row = _base_row(columns)
    row.update({
        "record_id": record_id,
        "record_type": "impact_link",
        "parent_id": parent_id,
        "related_indicator": related_indicator,
        "impact_direction": impact_direction,
    })
    rows.append(row)


def execute_enrichment(
    raw_path: str = "data/raw/ethiopia_fi_unified_data.xlsx",
    output_path: str = "data/processed/ethiopia_fi_enriched.csv",
) -> pd.DataFrame:
    """
    Load raw data, add new observations/events/impact_links from external sources,
    validate schema, and save enriched dataset.
    """
    base_path = Path(__file__).resolve().parent.parent
    raw_full = base_path / raw_path
    output_full = base_path / output_path

    df = load_unified_dataset(str(raw_full))
    columns = df.columns.tolist()
    max_id = int(df["record_id"].max()) if df["record_id"].notna().any() else 0
    new_rows = []

    # --- New observations from NBE Annual Report 2023-2024 & GSMA ---
    # Source: NBE Annual Report 2023-2024, GSMA Mobile Money Ethiopia
    # Mobile money accounts: 12.2M (2020) -> 139.5M (2025); Bank: 9.1M -> 54M
    today = datetime.now().strftime("%Y-%m-%d")

    _add_observation(
        new_rows,
        record_id=max_id + 1,
        indicator_code="MOBILE_MONEY_ACCTS_MN",
        value_numeric=12.2,
        observation_date="2020-12-31",
        source_name="National Bank of Ethiopia / GSMA",
        source_url="https://nbe.gov.et/wp-content/uploads/2025/06/Annual-Report-2023-2024.pdf",
        confidence="high",
        collected_by="enrichment_script",
        collection_date=today,
        notes="Mobile money accounts in millions. Useful for growth rate and digital payments modeling.",
        columns=columns,
        indicator="Mobile money accounts (millions)",
        unit="millions",
    )
    _add_observation(
        new_rows,
        record_id=max_id + 2,
        indicator_code="MOBILE_MONEY_ACCTS_MN",
        value_numeric=139.5,
        observation_date="2025-12-31",
        source_name="National Bank of Ethiopia",
        source_url="https://nbe.gov.et/wp-content/uploads/2025/06/Annual-Report-2023-2024.pdf",
        confidence="high",
        collected_by="enrichment_script",
        collection_date=today,
        notes="Mobile money accounts in millions. Supports trend and forecast validation.",
        columns=columns,
        indicator="Mobile money accounts (millions)",
        unit="millions",
    )
    _add_observation(
        new_rows,
        record_id=max_id + 3,
        indicator_code="BANK_ACCTS_MN",
        value_numeric=9.1,
        observation_date="2020-12-31",
        source_name="National Bank of Ethiopia",
        source_url="https://nbe.gov.et/wp-content/uploads/2025/06/Annual-Report-2023-2024.pdf",
        confidence="high",
        collected_by="enrichment_script",
        collection_date=today,
        notes="Bank accounts in millions. Complements account ownership analysis.",
        columns=columns,
        indicator="Bank accounts (millions)",
        unit="millions",
    )
    _add_observation(
        new_rows,
        record_id=max_id + 4,
        indicator_code="BANK_ACCTS_MN",
        value_numeric=54.0,
        observation_date="2025-12-31",
        source_name="National Bank of Ethiopia",
        source_url="https://nbe.gov.et/wp-content/uploads/2025/06/Annual-Report-2023-2024.pdf",
        confidence="high",
        collected_by="enrichment_script",
        collection_date=today,
        notes="Bank accounts in millions. Critical for access vs usage gap analysis.",
        columns=columns,
        indicator="Bank accounts (millions)",
        unit="millions",
    )
    _add_observation(
        new_rows,
        record_id=max_id + 5,
        indicator_code="MOBILE_MONEY_ACTIVATION_PCT",
        value_numeric=15.0,
        observation_date="2024-12-31",
        source_name="GSMA / NBE",
        source_url="https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-for-development/wp-content/uploads/2023/06/GSMA_Mobile-money-in-Ethiopia-Advancing-financial-inclusion-and-driving-growth-report.pdf",
        confidence="medium",
        collected_by="enrichment_script",
        collection_date=today,
        notes="Share of mobile money accounts that are active. Highlights usage gap.",
        columns=columns,
        indicator="Active mobile money accounts (%)",
        unit="percent",
    )

    # --- Events ---
    event_id_1 = max_id + 6
    _add_event(
        new_rows,
        record_id=event_id_1,
        category="policy_launch",
        period_start="2021-01-01",
        source_name="National Bank of Ethiopia",
        source_url="https://nbe.gov.et/ndps/",
        confidence="high",
        collected_by="enrichment_script",
        collection_date=today,
        notes="National Digital Payments Strategy 2021-2024 launch. Enables event-indicator modeling.",
        columns=columns,
    )
    event_id_2 = max_id + 7
    _add_event(
        new_rows,
        record_id=event_id_2,
        category="policy_launch",
        period_start="2020-06-01",
        source_name="National Bank of Ethiopia",
        source_url="https://nbe.gov.et/",
        confidence="high",
        collected_by="enrichment_script",
        collection_date=today,
        notes="Mobile money licensing (M-Pesa, Telebirr). Key driver of account growth.",
        columns=columns,
    )
    event_id_3 = max_id + 8
    _add_event(
        new_rows,
        record_id=event_id_3,
        category="policy_launch",
        period_start="2026-01-01",
        source_name="National Bank of Ethiopia",
        source_url="https://nbe.gov.et/ndps/",
        confidence="high",
        collected_by="enrichment_script",
        collection_date=today,
        notes="BRIDGE 2030 digital payments strategy. Supports scenario modeling.",
        columns=columns,
    )

    # --- Impact links: connect events to indicators ---
    _add_impact_link(
        new_rows,
        record_id=max_id + 9,
        parent_id=event_id_2,
        related_indicator="MOBILE_MONEY_ACCTS_MN",
        impact_direction="positive",
        columns=columns,
    )
    _add_impact_link(
        new_rows,
        record_id=max_id + 10,
        parent_id=event_id_1,
        related_indicator="MOBILE_MONEY_ACCTS_MN",
        impact_direction="positive",
        columns=columns,
    )
    _add_impact_link(
        new_rows,
        record_id=max_id + 11,
        parent_id=event_id_1,
        related_indicator="BANK_ACCTS_MN",
        impact_direction="positive",
        columns=columns,
    )

    # --- Append and validate ---
    df_new = pd.DataFrame(new_rows)
    df_enriched = pd.concat([df, df_new], ignore_index=True)
    validate_schema(df_enriched)

    output_full.parent.mkdir(parents=True, exist_ok=True)
    df_enriched.to_csv(output_full, index=False)
    return df_enriched


if __name__ == "__main__":
    df = execute_enrichment()
    print(f"Enriched dataset saved. Total records: {len(df)}")
