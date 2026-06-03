from typing import Optional

from app.services.token_launcher import TokenLauncher, Token, TokenStatus
from app.config import Config
from app.utils.logger import get_logger

logger = get_logger(__name__)


class DiscoveryFeed:
    def __init__(self, launcher: Optional[TokenLauncher] = None, config: type = Config):
        self._launcher = launcher or TokenLauncher(config)
        self._graduation_threshold = config.GRADUATION_MARKET_CAP_SOL

    def trending(self, limit: int = 20) -> list[Token]:
        """Rank bonding tokens by recent volume."""
        tokens = self._launcher.list_all(status="bonding")
        return sorted(tokens, key=lambda t: t.volume_sol, reverse=True)[:limit]

    def newest(self, limit: int = 20) -> list[Token]:
        tokens = self._launcher.list_all(status="bonding")
        return sorted(tokens, key=lambda t: t.created_at, reverse=True)[:limit]

    def about_to_graduate(self, limit: int = 20) -> list[Token]:
        """Tokens close to the graduation threshold, sorted by progress."""
        tokens = self._launcher.list_all(status="bonding")
        scored = [
            (t, t.market_cap_sol() / self._graduation_threshold)
            for t in tokens
        ]
        scored = [s for s in scored if s[1] >= 0.5]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [t for t, _ in scored][:limit]

    def graduated(self, limit: int = 20) -> list[Token]:
        tokens = self._launcher.list_all(status="graduated")
        return sorted(tokens, key=lambda t: t.graduated_at or "", reverse=True)[:limit]

    def graduation_progress(self, token: Token) -> float:
        return min(1.0, token.market_cap_sol() / self._graduation_threshold)
