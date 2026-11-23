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

def head_to_head(df: pd.DataFrame, player1: str, player2: str,  surface: str | None = None) -> dict:
    m= df[
        ((df["winner_name"] == player1) & (df["loser_name"] == player2))
        | ((df["winner_name"] == player2) & (df["loser_name"] == player1))
    ]
    if surface:
        m = m[m["surface"] == surface]

    p1_wins = int((m["winner_name"] == player1).sum())
    p2_wins = int((m["winner_name"] == player2).sum())
    return {
        "player1": player1,
        "player2": player2,
        "surface": surface,
        "player1_wins": p1_wins,
        "player2_wins": p2_wins,
        "matches": len(m),
    }
