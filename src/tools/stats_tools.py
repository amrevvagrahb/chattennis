from src.tools.stats import load_matches, win_rate, head_to_head, grand_slam_record, serve_stats, recent_form, top_players
from src.tools.names import build_name_list, resolve_player

_DF = load_matches()
_NAMES = build_name_list(_DF)


def _pick(query: str):
    """Return (exact_name, None) if clear, else (None, problem_dict)."""
    matches = resolve_player(query, _NAMES)
    if len(matches) == 1:
        return matches[0], None
    if not matches:
        return None, {
            "status": "not_found",
            "message": f"No player found matching '{query}'.",
        }
    return None, {
        "status": "ambiguous",
        "message": f"'{query}' matches several players. Ask the user which one.",
        "options": matches[:5],
    }


def win_rate_tool(player: str, surface: str | None = None, year: int | None = None) -> dict:
    name, problem = _pick(player)
    if problem:
        return problem
    return {"status": "ok", **win_rate(_DF, name, surface, year)}

def head_to_head_tool(player1: str, player2: str, surface: str | None = None ) -> dict:
    name1, problem1 = _pick(player1)
    if problem1:
        return problem1
    name2, problem2 = _pick(player2)
    if problem2:
        return problem2
    if name1 == name2:
        return {
            "status": "invalid",
            "message": "Both names resolve to the same player.",
        }
    return {'status': 'ok', **head_to_head(_DF, name1, name2, surface)}


def grand_slam_record_tool(player: str) -> dict:
    name, problem = _pick(player)
    if problem:
        return problem
    return {"status": "ok", **grand_slam_record(_DF, name)}


def serve_stats_tool(player: str, surface: str | None = None) -> dict:
    name, problem = _pick(player)
    if problem:
        return problem
    return {"status": "ok", **serve_stats(_DF, name, surface)}


def recent_form_tool(player: str, n: int = 10) -> dict:
    name, problem = _pick(player)
    if problem:
        return problem
    return {
        "status": "ok",
        "player": name,
        "note": "Most recent matches in the dataset (data ends in 2024).",
        "matches": recent_form(_DF, name, n),
    }

def top_players_tool(
    surface: str | None = None,
    year: int | None = None,
    metric: str = "win_rate",
    n: int = 5,
) -> dict:
    try:
        players = top_players(_DF, surface, year, metric, n)
    except ValueError as e:
        return {"status": "invalid", "message": str(e)}
    return {'status': 'ok', 'players': players}