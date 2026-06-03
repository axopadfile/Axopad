from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from app.config import Config
from app.services.bonding_curve import BondingCurve, QuoteResult
from app.services.token_launcher import TokenLauncher, Token, TokenStatus
from app.utils.logger import get_logger
from app.utils.helpers import new_id, utcnow_iso
from app.utils.rate_limiter import trade_limiter

logger = get_logger(__name__)

_trades: list["Trade"] = []


class TradeSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


@dataclass
class Trade:
    id: str
    token_id: str
    ticker: str
    side: TradeSide
    trader: str
    sol_amount: float
    token_amount: float
    price: float
    price_impact_pct: float
    fee: float
    created_at: str = field(default_factory=utcnow_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "token_id": self.token_id,
            "ticker": self.ticker,
            "side": self.side.value,
            "trader": self.trader,
            "sol_amount": round(self.sol_amount, 6),
            "token_amount": round(self.token_amount, 2),
            "price": self.price,
            "price_impact_pct": round(self.price_impact_pct, 4),
            "fee": round(self.fee, 6),
            "created_at": self.created_at,
        }


class TradeEngine:
    def __init__(
        self,
        launcher: Optional[TokenLauncher] = None,
        graduation_cb=None,
        config: type = Config,
    ):
        self._config = config
        self._launcher = launcher or TokenLauncher(config)
        self._curve = BondingCurve(config)
        self._graduation_cb = graduation_cb

    def buy(
        self,
        token_id: str,
        trader: str,
        sol_in: float,
        slippage_bps: int = 500,
        min_tokens_out: Optional[float] = None,
    ) -> Trade:
        trade_limiter.acquire()
        token = self._launcher.get(token_id)
        if not token:
            raise ValueError("Token not found")
        if token.status != TokenStatus.BONDING:
            raise ValueError(f"Token is {token.status.value}, not tradeable on curve")
        if sol_in <= 0:
            raise ValueError("sol_in must be positive")

        quote = self._curve.quote_buy(token.curve, sol_in)
        if min_tokens_out is not None and quote.output_amount < min_tokens_out:
            raise ValueError(f"Slippage exceeded: got {quote.output_amount:.2f} < min {min_tokens_out:.2f}")

        new_state, quote = self._curve.apply_buy(token.curve, sol_in)
        token.curve = new_state
        token.trade_count += 1
        token.volume_sol += sol_in
        token.holder_count += 1  # simplified

        trade = Trade(
            id=new_id(), token_id=token_id, ticker=token.ticker,
            side=TradeSide.BUY, trader=trader,
            sol_amount=sol_in, token_amount=quote.output_amount,
            price=new_state.price, price_impact_pct=quote.price_impact_pct, fee=quote.fee,
        )
        _trades.append(trade)
        logger.info(f"BUY {token.ticker}: {sol_in} SOL → {quote.output_amount:.2f} tokens @ {new_state.price:.10f}")

        self._check_graduation(token)
        return trade

    def sell(
        self,
        token_id: str,
        trader: str,
        tokens_in: float,
        min_sol_out: Optional[float] = None,
    ) -> Trade:
        trade_limiter.acquire()
        token = self._launcher.get(token_id)
        if not token:
            raise ValueError("Token not found")
        if token.status != TokenStatus.BONDING:
            raise ValueError(f"Token is {token.status.value}, not tradeable on curve")
        if tokens_in <= 0:
            raise ValueError("tokens_in must be positive")

        quote = self._curve.quote_sell(token.curve, tokens_in)
        if min_sol_out is not None and quote.output_amount < min_sol_out:
            raise ValueError(f"Slippage exceeded: got {quote.output_amount:.6f} < min {min_sol_out:.6f}")

        new_state, quote = self._curve.apply_sell(token.curve, tokens_in)
        token.curve = new_state
        token.trade_count += 1
        token.volume_sol += quote.output_amount

        trade = Trade(
            id=new_id(), token_id=token_id, ticker=token.ticker,
            side=TradeSide.SELL, trader=trader,
            sol_amount=quote.output_amount, token_amount=tokens_in,
            price=new_state.price, price_impact_pct=quote.price_impact_pct, fee=quote.fee,
        )
        _trades.append(trade)
        logger.info(f"SELL {token.ticker}: {tokens_in:.2f} tokens → {quote.output_amount:.6f} SOL")
        return trade

    def quote(self, token_id: str, side: str, amount: float) -> Optional[QuoteResult]:
        token = self._launcher.get(token_id)
        if not token:
            return None
        if side == "buy":
            return self._curve.quote_buy(token.curve, amount)
        return self._curve.quote_sell(token.curve, amount)

    def get_trades(self, token_id: Optional[str] = None, limit: int = 50) -> list[Trade]:
        data = list(reversed(_trades))
        if token_id:
            data = [t for t in data if t.token_id == token_id]
        return data[:limit]

    def _check_graduation(self, token: Token) -> None:
        mcap = token.market_cap_sol()
        if mcap >= self._config.GRADUATION_MARKET_CAP_SOL and token.status == TokenStatus.BONDING:
            token.status = TokenStatus.GRADUATED
            token.graduated_at = utcnow_iso()
            logger.info(f"🎓 {token.ticker} GRADUATED at {mcap:.2f} SOL market cap")
            if self._graduation_cb:
                self._graduation_cb(token)
