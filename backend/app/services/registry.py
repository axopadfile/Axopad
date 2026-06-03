"""Shared singleton service instances so all API blueprints operate on the same state."""
from app.services.token_launcher import TokenLauncher
from app.services.trade_engine import TradeEngine
from app.services.discovery_feed import DiscoveryFeed
from app.services.llm_analyst import LLMAnalyst

launcher = TokenLauncher()
trade_engine = TradeEngine(launcher=launcher)
discovery = DiscoveryFeed(launcher=launcher)
analyst = LLMAnalyst()
