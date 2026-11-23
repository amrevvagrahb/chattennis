import pytest
from src.tools.stats import load_matches, win_rate

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