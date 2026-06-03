# Axopad

## Overview
Fair-launch token launchpad for Solana (pump.fun style).
Bonding curve price discovery, instant token launch, auto-graduation to DEX, LLM token analyst.

## Stack
- **Backend**: Python 3.11, Flask 3.0, httpx
- **Frontend**: Vue 3 + Vite, Pinia, Axios
- **AI**: Anthropic Claude (primary), DeepInfra (fallback)

## Structure
```
backend/app/
  config.py              — curve params, graduation threshold, fees
  __init__.py            — Flask factory (3 blueprints)
  api/
    token.py             — launch, get, list, LLM analyze
    trade.py             — buy, sell, quote, history
    feed.py              — trending/new/graduating/graduated
  services/
    bonding_curve.py     — constant-product (x*y=k) price engine [core]
    token_launcher.py    — token deploy + registry
    trade_engine.py      — buy/sell against curve + auto-graduation
    discovery_feed.py    — trending/new/graduating ranking
    llm_analyst.py       — LLM token momentum/risk commentary
    registry.py          — shared singletons (one state across blueprints)
  utils/
    logger, cache (TTL), rate_limiter, retry,
    helpers (mint addr, slugify, validate_ticker, format_sol)

frontend/src/
  views/Discover.vue     — trending/new/graduating/graduated feed
  views/Launch.vue       — token launch form
  views/TokenView.vue    — trade panel + bonding curve + AI analyst + trades
  components/TokenCard.vue

tests/
  test_bonding_curve.py  — curve math (price up/down, fees, impact, k)
  test_token_launcher.py — launch validation
  test_trade_engine.py   — buy/sell/slippage/graduation
```

## Bonding curve (the core)
Constant product `x*y=k`:
- virtual_sol starts at 30, virtual_tokens at 1.073B
- buy: add SOL, remove tokens → price up
- sell: add tokens, remove SOL → price down
- 1% fee per trade
- graduates to DEX at 85 SOL market cap

## API
- `POST /api/token/launch`        — `{name, ticker, creator, description?, image_url?}`
- `GET  /api/token/<id>`          — token + curve + graduation progress
- `POST /api/token/<id>/analyze`  — LLM momentum/risk
- `POST /api/trade/buy`           — `{token_id, trader, sol_in, min_tokens_out?}`
- `POST /api/trade/sell`          — `{token_id, trader, tokens_in, min_sol_out?}`
- `GET  /api/trade/quote`         — `?token_id=&side=&amount=`
- `GET  /api/feed/trending|new|graduating|graduated`

## Dev
```bash
npm run dev      # both servers
pytest tests/ -v # no API keys needed
python backend/scripts/simulate_launch.py  # watch a token graduate
```
