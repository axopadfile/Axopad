import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.services.bonding_curve import BondingCurve, CurveState
from app.config import Config


def make_curve():
    return BondingCurve(Config)


def test_init_state():
    curve = make_curve()
    state = curve.init_state(Config)
    assert state.virtual_sol == Config.CURVE_VIRTUAL_SOL
    assert state.virtual_tokens == Config.CURVE_VIRTUAL_TOKENS


def test_constant_product_preserved_on_buy():
    curve = make_curve()
    state = curve.init_state(Config)
    k_before = state.k
    new_state, _ = curve.apply_buy(state, 1.0)
    # k should be approximately preserved (fee added to reserve breaks it slightly upward)
    assert new_state.k >= k_before * 0.99


def test_buy_increases_price():
    curve = make_curve()
    state = curve.init_state(Config)
    price_before = state.price
    new_state, _ = curve.apply_buy(state, 5.0)
    assert new_state.price > price_before


def test_sell_decreases_price():
    curve = make_curve()
    state = curve.init_state(Config)
    # buy first to have something to sell
    state, buy_quote = curve.apply_buy(state, 10.0)
    price_before = state.price
    new_state, _ = curve.apply_sell(state, buy_quote.output_amount / 2)
    assert new_state.price < price_before


def test_buy_returns_tokens():
    curve = make_curve()
    state = curve.init_state(Config)
    quote = curve.quote_buy(state, 1.0)
    assert quote.output_amount > 0


def test_buy_charges_fee():
    curve = make_curve()
    state = curve.init_state(Config)
    quote = curve.quote_buy(state, 10.0)
    assert quote.fee > 0
    assert abs(quote.fee - 10.0 * Config.TRADE_FEE_BPS / 10_000) < 1e-9


def test_larger_buy_more_impact():
    curve = make_curve()
    state = curve.init_state(Config)
    small = curve.quote_buy(state, 1.0)
    large = curve.quote_buy(state, 20.0)
    assert large.price_impact_pct > small.price_impact_pct


def test_market_cap_rises_with_buys():
    curve = make_curve()
    state = curve.init_state(Config)
    mcap_before = curve.market_cap_sol(state, Config.TOKEN_TOTAL_SUPPLY)
    state, _ = curve.apply_buy(state, 20.0)
    mcap_after = curve.market_cap_sol(state, Config.TOKEN_TOTAL_SUPPLY)
    assert mcap_after > mcap_before


def test_buy_then_sell_roundtrip_loses_to_fees():
    curve = make_curve()
    state = curve.init_state(Config)
    state, buy_q = curve.apply_buy(state, 5.0)
    state, sell_q = curve.apply_sell(state, buy_q.output_amount)
    # Round-trip should return less SOL than put in due to fees + slippage
    assert sell_q.output_amount < 5.0
