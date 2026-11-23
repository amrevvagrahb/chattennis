import pytest
from src.tools.stats import load_matches, win_rate, head_to_head

@pytest.fixture(scope="module")
def df():
    return load_matches()


def test_wins_plus_losses_equals_matches(df):
    r = win_rate(df, "Rafael Nadal")
    assert r["wins"] + r["losses"] == r["matches"]


def test_rate_between_0_and_1(df):
    r = win_rate(df, "Rafael Nadal", surface="Clay")
    assert 0 <= r["win_rate"] <= 1


def test_surface_filter_reduces_matches(df):
    overall = win_rate(df, "Rafael Nadal")
    clay = win_rate(df, "Rafael Nadal", surface="Clay")
    assert clay["matches"] < overall["matches"]


def test_unknown_player_returns_none_rate(df):
    r = win_rate(df, "Nobody Atall")
    assert r["matches"] == 0
    assert r["win_rate"]== None

def test_h2h_wins_add_up(df):
    r = head_to_head(df, "Rafael Nadal", "Roger Federer")
    assert r["player1_wins"] + r["player2_wins"] == r["matches"]


def test_h2h_is_symmetric(df):
    a = head_to_head(df, "Rafael Nadal", "Roger Federer")
    b = head_to_head(df, "Roger Federer", "Rafael Nadal")
    assert a["player1_wins"] == b["player2_wins"]
    assert a["matches"] == b["matches"]


def test_h2h_surface_filter(df):
    overall = head_to_head(df, "Rafael Nadal", "Roger Federer")
    clay = head_to_head(df, "Rafael Nadal", "Roger Federer", surface="Clay")
    assert clay["matches"] <= overall["matches"]    