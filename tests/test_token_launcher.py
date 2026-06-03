import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.services.token_launcher import TokenLauncher, TokenStatus, _tokens


def setup_function():
    _tokens.clear()


def test_launch_creates_token():
    l = TokenLauncher()
    t = l.launch("Axolotl Coin", "AXO", "regen meme", "Creator1111")
    assert t.ticker == "AXO"
    assert t.status == TokenStatus.BONDING
    assert len(t.mint) == 44


def test_launch_lowercase_ticker_uppercased():
    l = TokenLauncher()
    t = l.launch("Test", "abc", "", "Creator1111")
    assert t.ticker == "ABC"


def test_launch_rejects_empty_name():
    l = TokenLauncher()
    try:
        l.launch("", "AXO", "", "Creator1111")
        assert False
    except ValueError:
        pass


def test_launch_rejects_bad_ticker():
    l = TokenLauncher()
    try:
        l.launch("Test", "this-is-invalid!", "", "Creator1111")
        assert False
    except ValueError:
        pass


def test_get_by_mint():
    l = TokenLauncher()
    t = l.launch("Test", "TST", "", "Creator1111")
    found = l.get_by_mint(t.mint)
    assert found is not None and found.id == t.id


def test_starting_market_cap_positive():
    l = TokenLauncher()
    t = l.launch("Test", "TST", "", "Creator1111")
    assert t.market_cap_sol() > 0


def test_list_filters_by_status():
    l = TokenLauncher()
    l.launch("A", "AAA", "", "c1")
    l.launch("B", "BBB", "", "c2")
    bonding = l.list_all(status="bonding")
    assert len(bonding) == 2
