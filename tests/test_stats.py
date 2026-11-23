import pytest
from src.tools.stats import load_matches, win_rate, head_to_head, grand_slam_record, serve_stats, recent_form, top_players

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

def test_slam_wins_plus_losses(df):
    r = grand_slam_record(df, "Rafael Nadal")
    assert r["wins"] + r["losses"] > 0


def test_titles_not_more_than_finals(df):
    r = grand_slam_record(df, "Roger Federer")
    assert r["titles"] <= r["finals_played"]


def test_unknown_player_has_no_titles(df):
    r = grand_slam_record(df, "Nobody Atall")
    assert r["titles"] == 0 and r["wins"] == 0

def test_serve_percentages_in_range(df):
    r = serve_stats(df, "Rafael Nadal")
    assert 0 <= r["first_serve_pct"] <= 1
    assert 0 <= r["bp_saved_pct"] <= 1


def test_stats_matches_not_more_than_all_matches(df):
    all_m = win_rate(df, "Rafael Nadal")["matches"]
    r = serve_stats(df, "Rafael Nadal")
    assert r["matches_with_stats"] <= all_m


def test_unknown_player_serve_is_none(df):
    r = serve_stats(df, "Nobody Atall")
    assert r["matches_with_stats"] == 0
    assert r["aces_per_match"] is None

def test_recent_form_length(df):
    assert len(recent_form(df, "Rafael Nadal", n=10)) == 10


def test_recent_form_is_in_date_order(df):
    dates = [r["date"] for r in recent_form(df, "Rafael Nadal", n=10)]
    assert dates == sorted(dates)


def test_recent_form_results_valid(df):
    for r in recent_form(df, "Rafael Nadal", n=10):
        assert r["result"] in ("W", "L")
        assert r["opponent"] != "Rafael Nadal"


def test_unknown_player_empty(df):
    assert recent_form(df, "Nobody Atall") == []

def test_top_players_length(df):
    assert len(top_players(df, surface="Clay", year=2019, n=5)) == 5


def test_top_players_sorted_descending(df):
    rates = [p["win_rate"] for p in top_players(df, surface="Clay", year=2019, n=5)]
    assert rates == sorted(rates, reverse=True)


def test_min_matches_respected(df):
    for p in top_players(df, surface="Clay", year=2019, min_matches=15):
        assert p["matches"] >= 15


def test_bad_metric_raises(df):
    with pytest.raises(ValueError):
        top_players(df, metric="nonsense")


def test_no_matches_returns_empty(df):
    assert top_players(df, year= 1900) == []