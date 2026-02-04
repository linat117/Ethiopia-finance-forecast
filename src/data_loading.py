import pandas as pd
from pathlib import Path

def load_unified_dataset(file_path: str) -> pd.DataFrame:
    """
    Load unified Ethiopia FI dataset from Excel or CSV.
    Handles multi-sheet Excel files.
    """
    path = Path(file_path)

    if path.suffix == ".xlsx":
        xls = pd.ExcelFile(path)
        sheets = xls.sheet_names

        data_frames = []
        for sheet in sheets:
            df = pd.read_excel(path, sheet_name=sheet)
            data_frames.append(df)

        return pd.concat(data_frames, ignore_index=True)

    elif path.suffix == ".csv":
        return pd.read_csv(path)

    else:
        raise ValueError("Unsupported file format")


def load_processed_enriched(file_path: str = "data/processed/ethiopia_fi_enriched.xlsx"):
    """Load enriched dataset from processed Excel (sheets: data, events, impact_links). Returns (data, events, impact_links)."""
    path = Path(file_path)
    if not path.is_absolute():
        path = Path(__file__).resolve().parent.parent / path
    if not path.exists():
        raise FileNotFoundError(f"Processed file not found: {path}")
    data = pd.read_excel(path, sheet_name="data")
    events = pd.read_excel(path, sheet_name="events")
    impact_links = pd.read_excel(path, sheet_name="impact_links")
    return data, events, impact_links


def load_reference_codes(file_path: str) -> pd.DataFrame:
    path = Path(file_path)

    if path.suffix == ".xlsx":
        return pd.read_excel(path)
    elif path.suffix == ".csv":
        return pd.read_csv(path)
    else:
        raise ValueError("Unsupported reference file format")
