import pytest 
from src.tools.stats import load_matches
from src.tools.names import build_name_list, resolve_player

@pytest.fixture(scope="module")
def names():
    return build_name_list(load_matches())


def test_alias(names):
    assert resolve_player("rafa", names) == ["Rafael Nadal"]


def test_exact_match_ignores_case(names):
    assert resolve_player("novak djokovic", names) == ["Novak Djokovic"]


def test_partial_match(names):
    assert "Rafael Nadal" in resolve_player("nadal", names)


def test_typo_in_full_name(names):
    assert "Novak Djokovic" in resolve_player("novak djokovik", names)





def test_nonsense_returns_empty(names):
    assert resolve_player('zzzzqqqq', names) == []


