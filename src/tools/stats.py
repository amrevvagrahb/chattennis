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

def player_matches(df: pd.DataFrame, player: str)-> pd.DataFrame:
    played = df[(df["winner_name"] == player) | (df["loser_name"] == player)].copy()
    played["won"] = played["winner_name"] == player
    return played


def win_rate(df: pd.DataFrame, player: str, surface: str | None = None, year: int | None = None) -> dict:
    m = player_matches(df, player)
    if surface:
        m = m[m["surface"] == surface]
    if year:
        m = m[m["year"] == year]

    wins = int(m["won"].sum())
    total = len(m)
    return {
        "player": player,
        "surface": surface,
        "year": year,
        "wins": wins,
        "losses": total - wins,
        "matches": total,
        "win_rate": round(wins / total, 3) if total else None
    }