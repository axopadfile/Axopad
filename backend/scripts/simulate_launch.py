#!/usr/bin/env python3
"""Simulate a token launch and a buy frenzy until graduation."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.token_launcher import TokenLauncher
from app.services.trade_engine import TradeEngine
from app.services.discovery_feed import DiscoveryFeed
from app.config import Config
from app.utils.logger import get_logger

logger = get_logger("simulate")


def main():
    print("\n🚀 Axopad Launch Simulation\n" + "="*50)

    launcher = TokenLauncher()
    engine = TradeEngine(launcher=launcher)
    feed = DiscoveryFeed(launcher=launcher)

    # Launch a token
    token = launcher.launch(
        name="Axolotl Coin", ticker="AXO",
        description="The regenerating meme on Solana",
        creator="CreatorWallet1111111111111111111111111111",
    )
    print(f"\nLaunched: {token.ticker} ({token.name})")
    print(f"  Mint: {token.mint[:16]}...")
    print(f"  Start price: {token.curve.price:.12f} SOL")
    print(f"  Start mcap: {token.market_cap_sol():.4f} SOL")
    print(f"  Graduation target: {Config.GRADUATION_MARKET_CAP_SOL} SOL\n")

    # Buy frenzy
    buyers = [f"Buyer{i}Wallet" + "x"*30 for i in range(1, 16)]
    print("Buy frenzy:")
    for i, buyer in enumerate(buyers, 1):
        try:
            trade = engine.buy(token.id, buyer, sol_in=3.0)
            progress = feed.graduation_progress(token) * 100
            bar = "█" * int(progress / 5) + "░" * (20 - int(progress / 5))
            print(f"  #{i:>2} {buyer[:10]} +3 SOL → {trade.token_amount:>14,.0f} {token.ticker}  "
                  f"mcap={token.market_cap_sol():>7.2f} SOL  [{bar}] {progress:.0f}%")
            if token.status.value == "graduated":
                print(f"\n  🎓 {token.ticker} GRADUATED! Liquidity migrates to DEX.")
                break
        except ValueError as e:
            print(f"  #{i}: {e}")
            break

    print(f"\n{'='*50}")
    print(f"Final price: {token.curve.price:.12f} SOL")
    print(f"Final mcap: {token.market_cap_sol():.2f} SOL")
    print(f"Total trades: {token.trade_count}")
    print(f"Volume: {token.volume_sol:.2f} SOL")
    print(f"Status: {token.status.value}")
    print("\n✓ Done\n")


if __name__ == "__main__":
    main()
