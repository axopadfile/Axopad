from dataclasses import dataclass
from typing import Optional

from app.config import Config
from app.utils.logger import get_logger
from app.utils.helpers import safe_div

logger = get_logger(__name__)


@dataclass
class CurveState:
    virtual_sol: float
    virtual_tokens: float
    real_sol: float
    real_tokens: float

    @property
    def k(self) -> float:
        return self.virtual_sol * self.virtual_tokens

    @property
    def price(self) -> float:
        """Current price in SOL per token = virtual_sol / virtual_tokens."""
        return safe_div(self.virtual_sol, self.virtual_tokens)

    def to_dict(self) -> dict:
        return {
            "virtual_sol": self.virtual_sol,
            "virtual_tokens": self.virtual_tokens,
            "real_sol": self.real_sol,
            "real_tokens": self.real_tokens,
            "price": self.price,
            "k": self.k,
        }


@dataclass
class QuoteResult:
    input_amount: float
    output_amount: float
    price_before: float
    price_after: float
    price_impact_pct: float
    fee: float


class BondingCurve:
    """
    Constant-product (x*y=k) bonding curve, pump.fun style.
    Buying tokens adds SOL to the reserve and removes tokens, raising the price.
    Selling does the reverse.
    """

    def __init__(self, config: type = Config):
        self._fee_bps = config.TRADE_FEE_BPS

    def init_state(self, config: type = Config) -> CurveState:
        return CurveState(
            virtual_sol=config.CURVE_VIRTUAL_SOL,
            virtual_tokens=config.CURVE_VIRTUAL_TOKENS,
            real_sol=0.0,
            real_tokens=config.CURVE_VIRTUAL_TOKENS,
        )

    def quote_buy(self, state: CurveState, sol_in: float) -> QuoteResult:
        """Quote how many tokens you get for sol_in SOL."""
        fee = sol_in * self._fee_bps / 10_000
        sol_after_fee = sol_in - fee

        price_before = state.price
        # x*y=k : new_tokens = k / (virtual_sol + sol_in)
        new_virtual_sol = state.virtual_sol + sol_after_fee
        new_virtual_tokens = state.k / new_virtual_sol
        tokens_out = state.virtual_tokens - new_virtual_tokens
        price_after = safe_div(new_virtual_sol, new_virtual_tokens)

        impact = safe_div(price_after - price_before, price_before) * 100

        return QuoteResult(
            input_amount=sol_in,
            output_amount=max(0.0, tokens_out),
            price_before=price_before,
            price_after=price_after,
            price_impact_pct=impact,
            fee=fee,
        )

    def quote_sell(self, state: CurveState, tokens_in: float) -> QuoteResult:
        """Quote how much SOL you get for selling tokens_in tokens."""
        price_before = state.price
        new_virtual_tokens = state.virtual_tokens + tokens_in
        new_virtual_sol = state.k / new_virtual_tokens
        sol_out_gross = state.virtual_sol - new_virtual_sol
        fee = sol_out_gross * self._fee_bps / 10_000
        sol_out = sol_out_gross - fee
        price_after = safe_div(new_virtual_sol, new_virtual_tokens)

        impact = safe_div(price_after - price_before, price_before) * 100

        return QuoteResult(
            input_amount=tokens_in,
            output_amount=max(0.0, sol_out),
            price_before=price_before,
            price_after=price_after,
            price_impact_pct=impact,
            fee=fee,
        )

    def apply_buy(self, state: CurveState, sol_in: float) -> tuple[CurveState, QuoteResult]:
        quote = self.quote_buy(state, sol_in)
        fee = quote.fee
        sol_after_fee = sol_in - fee
        new_state = CurveState(
            virtual_sol=state.virtual_sol + sol_after_fee,
            virtual_tokens=state.virtual_tokens - quote.output_amount,
            real_sol=state.real_sol + sol_after_fee,
            real_tokens=state.real_tokens - quote.output_amount,
        )
        return new_state, quote

    def apply_sell(self, state: CurveState, tokens_in: float) -> tuple[CurveState, QuoteResult]:
        quote = self.quote_sell(state, tokens_in)
        new_state = CurveState(
            virtual_sol=state.virtual_sol - (quote.output_amount + quote.fee),
            virtual_tokens=state.virtual_tokens + tokens_in,
            real_sol=max(0.0, state.real_sol - (quote.output_amount + quote.fee)),
            real_tokens=state.real_tokens + tokens_in,
        )
        return new_state, quote

    def market_cap_sol(self, state: CurveState, total_supply: float) -> float:
        return state.price * total_supply
