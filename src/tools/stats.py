from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

def load_matches() -> pd.DataFrame:
    files = sorted(DATA_DIR.glob("atp_matches_*.csv"))
    if not files:
        raise FileNotFoundError(f"No match CSVs found in {DATA_DIR}")
    df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
    df["tourney_date"] = pd.to_datetime(df["tourney_date"], format="%Y%m%d")
    df["year"] = df["tourney_date"].dt.year
    return df