from src.tools.stats_tools import win_rate_tool, head_to_head_tool

def test_alias_resolves_and_returns_stats():
    r = win_rate_tool("rafa", surface="Clay")
    assert r["status"] == "ok"
    assert r["player"] == "Rafael Nadal"


def test_unknown_player_not_found():
    r = win_rate_tool("zzzzqqqq")
    assert r["status"] == "not_found"


def test_vague_name_is_ambiguous():
    r = win_rate_tool("john")
    assert r["status"] == "ambiguous"
    assert len(r["options"]) >= 2 

def test_h2h_tool_ok():
    r = head_to_head_tool("nadal", "federer")
    assert r["status"] == "ok"
    assert r["matches"] > 0


def test_h2h_tool_first_name_ambiguous():
    r = head_to_head_tool("murray", "federer")
    assert r["status"] == "ambiguous"


def test_h2h_tool_same_player_invalid():
    r = head_to_head_tool("nadal", "rafa")
    assert r['status'] == 'invalid'