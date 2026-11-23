from difflib import get_close_matches
import pandas as pd

ALIASES = {
    "rafa": "Rafael Nadal",
    "nole": "Novak Djokovic",
    "carlitos": "Carlos Alcaraz",
}

def build_name_list(df: pd.DataFrame) -> list[str]:
    names = pd.concat([df["winner_name"], df["loser_name"]]).dropna().unique()
    return sorted(names)

def resolve_player(query: str, names: list[str]) -> list[str]:
    q = query.strip().lower()

    if q in ALIASES:
        return [ALIASES[q]]

    exact = [n for n in names if n.lower() == q]
    if exact:
        return exact

    partial = [n for n in names if q in n.lower()]
    if partial:
        return partial

    lookup = {n.lower(): n for n in names}
    close = get_close_matches(q, lookup.keys(), n=3, cutoff=0.8)
    return [lookup[c] for c in close]