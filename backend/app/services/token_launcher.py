from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from app.config import Config
from app.services.bonding_curve import BondingCurve, CurveState
from app.utils.logger import get_logger
from app.utils.helpers import (
    new_id, utcnow_iso, fake_mint_address, slugify, validate_ticker,
)

logger = get_logger(__name__)

_tokens: dict[str, "Token"] = {}


class TokenStatus(str, Enum):
    BONDING = "bonding"        # trading on the curve
    GRADUATED = "graduated"    # migrated to DEX
    FROZEN = "frozen"


@dataclass
class Token:
    id: str
    mint: str
    name: str
    ticker: str
    description: str
    image_url: str
    creator: str
    curve: CurveState
    status: TokenStatus = TokenStatus.BONDING
    total_supply: float = 1_000_000_000
    created_at: str = field(default_factory=utcnow_iso)
    graduated_at: Optional[str] = None
    holder_count: int = 0
    trade_count: int = 0
    volume_sol: float = 0.0
    twitter: str = ""
    telegram: str = ""
    website: str = ""

    def market_cap_sol(self) -> float:
        return self.curve.price * self.total_supply

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "mint": self.mint,
            "name": self.name,
            "ticker": self.ticker,
            "description": self.description,
            "image_url": self.image_url,
            "creator": self.creator,
            "status": self.status.value,
            "price": self.curve.price,
            "market_cap_sol": round(self.market_cap_sol(), 4),
            "total_supply": self.total_supply,
            "real_sol": round(self.curve.real_sol, 4),
            "holder_count": self.holder_count,
            "trade_count": self.trade_count,
            "volume_sol": round(self.volume_sol, 4),
            "created_at": self.created_at,
            "graduated_at": self.graduated_at,
            "twitter": self.twitter,
            "telegram": self.telegram,
            "website": self.website,
        }


class TokenLauncher:
    def __init__(self, config: type = Config):
        self._config = config
        self._curve = BondingCurve(config)

    def launch(
        self,
        name: str,
        ticker: str,
        description: str,
        creator: str,
        image_url: str = "",
        twitter: str = "",
        telegram: str = "",
        website: str = "",
    ) -> Token:
        name = name.strip()
        ticker = ticker.strip().upper()

        if not name or len(name) > self._config.MAX_NAME_LENGTH:
            raise ValueError(f"Name must be 1-{self._config.MAX_NAME_LENGTH} chars")
        if not validate_ticker(ticker, self._config.MAX_TICKER_LENGTH):
            raise ValueError(f"Ticker must be 1-{self._config.MAX_TICKER_LENGTH} uppercase alphanumeric")

        token = Token(
            id=new_id(),
            mint=fake_mint_address(),
            name=name,
            ticker=ticker,
            description=description,
            image_url=image_url,
            creator=creator,
            curve=self._curve.init_state(self._config),
            total_supply=self._config.TOKEN_TOTAL_SUPPLY,
            twitter=twitter,
            telegram=telegram,
            website=website,
        )
        _tokens[token.id] = token
        logger.info(f"Token launched: {ticker} ({name}) mint={token.mint[:8]}... by {creator[:8]}")
        return token

    def get(self, token_id: str) -> Optional[Token]:
        return _tokens.get(token_id)

    def get_by_mint(self, mint: str) -> Optional[Token]:
        return next((t for t in _tokens.values() if t.mint == mint), None)

    def list_all(self, status: Optional[str] = None) -> list[Token]:
        tokens = list(_tokens.values())
        if status:
            tokens = [t for t in tokens if t.status.value == status]
        return tokens
