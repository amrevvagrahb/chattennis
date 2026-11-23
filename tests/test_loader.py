import pytest 
from src.tools.stats import load_matches

@pytest.fixture(scope="module")
def df():
    return load_matches()


def test_loads_many_rows(df):
    assert len(df) > 50_000


def test_has_required_columns(df):
    for col in ["winner_name", "loser_name", "surface", "tourney_date", "year"]:
        assert col in df.columns


def test_year_range(df):
    assert df["year"].min() == 2000
    assert df["year"].max() == 2024


def test_main_surfaces_present(df):
    assert {"Hard", "Clay", "Grass"} <= set(df["surface"].dropna().unique())
