import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.services.token_launcher import TokenLauncher, TokenStatus, _tokens
from app.services.trade_engine import TradeEngine, TradeSide, _trades
from app.config import Config


def setup_function():
    _tokens.clear()
    _trades.clear()


def make_stack():
    launcher = TokenLauncher()
    engine = TradeEngine(launcher=launcher)
    return launcher, engine


def test_buy_returns_tokens():
    launcher, engine = make_stack()
    token = launcher.launch("Test", "TST", "", "creator")
    trade = engine.buy(token.id, "buyer1", sol_in=2.0)
    assert trade.side == TradeSide.BUY
    assert trade.token_amount > 0


def test_buy_raises_price():
    launcher, engine = make_stack()
    token = launcher.launch("Test", "TST", "", "creator")
    p0 = token.curve.price
    engine.buy(token.id, "buyer1", sol_in=5.0)
    assert token.curve.price > p0


def test_sell_after_buy():
    launcher, engine = make_stack()
    token = launcher.launch("Test", "TST", "", "creator")
    buy = engine.buy(token.id, "trader1", sol_in=5.0)
    sell = engine.sell(token.id, "trader1", tokens_in=buy.token_amount / 2)
    assert sell.side == TradeSide.SELL
    assert sell.sol_amount > 0


def test_buy_rejects_zero():
    launcher, engine = make_stack()
    token = launcher.launch("Test", "TST", "", "creator")
    try:
        engine.buy(token.id, "buyer1", sol_in=0)
        assert False
    except ValueError:
        pass


def test_slippage_protection():
    launcher, engine = make_stack()
    token = launcher.launch("Test", "TST", "", "creator")
    try:
        engine.buy(token.id, "buyer1", sol_in=1.0, min_tokens_out=1e18)
        assert False
    except ValueError:
        pass


def test_graduation_triggers():
    launcher, engine = make_stack()
    token = launcher.launch("Test", "TST", "", "creator")
    # Buy enough to cross graduation threshold
    for i in range(40):
        if token.status != TokenStatus.BONDING:
            break
        try:
            engine.buy(token.id, f"buyer{i}", sol_in=5.0)
        except ValueError:
            break
    assert token.status == TokenStatus.GRADUATED
    assert token.graduated_at is not None


def test_trade_history_recorded():
    launcher, engine = make_stack()
    token = launcher.launch("Test", "TST", "", "creator")
    engine.buy(token.id, "b1", sol_in=1.0)
    engine.buy(token.id, "b2", sol_in=1.0)
    trades = engine.get_trades(token_id=token.id)
    assert len(trades) == 2


def test_quote_does_not_mutate():
    launcher, engine = make_stack()
    token = launcher.launch("Test", "TST", "", "creator")
    p0 = token.curve.price
    engine.quote(token.id, "buy", 5.0)
    assert token.curve.price == p0
