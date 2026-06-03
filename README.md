# Axopad 🚀

<div align="center">

**The fair launchpad for Solana.**
*Every token starts on the curve. No presale. No insiders.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![CI](https://github.com/Axopad/Axopad/actions/workflows/ci.yml/badge.svg)](https://github.com/Axopad/Axopad/actions)
[![Solana](https://img.shields.io/badge/Solana-mainnet-9945FF.svg)](https://solana.com/)

</div>

---

## What is Axopad?

Axopad is an **open-source token launchpad for Solana** — a fair-launch platform where anyone can deploy a token in seconds, every buy and sell runs through a transparent bonding curve, and tokens auto-graduate to a DEX once they hit market cap.

No presale. No team allocation. No insider rounds. Just a curve that everyone trades against equally, from the first buyer to the last.

> *"We built Axopad because fair launches should actually be fair. Every token starts at the same price for everyone. The curve doesn't care who you are."*

### Core Features

- **Instant Token Launch** — deploy an SPL token with name, ticker, image, and description in one transaction
- **Bonding Curve Engine** — constant-product price discovery; price rises as supply is bought, falls as it's sold
- **Auto-Graduation** — tokens that reach the market cap threshold migrate liquidity to a DEX automatically
- **Trade Engine** — buy/sell against the curve with slippage protection and real-time price quotes
- **AI Token Analyst** — LLM-generated risk and momentum commentary on every launch
- **Live Discovery Feed** — trending, new, and graduating tokens in a real-time Vue3 UI

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                       Axopad                              │
│                                                           │
│   Creator                          Trader                 │
│      │                                │                   │
│      ▼                                ▼                   │
│  ┌─────────┐                    ┌──────────┐             │
│  │  Token   │                    │  Trade    │            │
│  │ Launcher │                    │  Engine   │            │
│  └────┬─────┘                    └────┬─────┘             │
│       │                               │                   │
│       └───────────┬───────────────────┘                   │
│                   │                                       │
│          ┌────────▼────────┐                              │
│          │  Bonding Curve  │                              │
│          │  price discovery │                             │
│          └────────┬────────┘                              │
│                   │                                       │
│      ┌────────────┼────────────┐                          │
│      │            │            │                          │
│  Graduation   AI Analyst   Discovery                      │
│   Engine                     Feed                         │
│      │            │            │                          │
│      └────────────┼────────────┘                          │
│                   │                                       │
│              Solana Mainnet                               │
└──────────────────────────────────────────────────────────┘
```

---

## Narrative

Every cycle, the same thing happens.

A token launches. The team holds 30%. Insiders got in at a private round. By the time you can buy, the people who matter are already in profit and you're exit liquidity.

Solana changed the game by making launches cheap and fast. But fast and cheap isn't the same as fair.

Axopad is the fair part.

Every token on Axopad starts on a bonding curve at the same price for everyone. There's no presale to get into. No team allocation to dump on you. No insider round you weren't invited to. The first buyer and the thousandth buyer trade against the exact same curve — the only difference is timing, and timing is something everyone can see.

When a token's curve fills up to the graduation threshold, its liquidity migrates to a DEX automatically and the curve closes. No team decision, no manual migration, no rug vector. The code does it.

**Axo** — from axolotl, the creature that regenerates anything it loses. **pad** — launchpad.

The market regenerates every day. Axopad is where it starts.

---

## Quickstart

### Docker

```bash
git clone https://github.com/Axopad/Axopad.git
cd Axopad
cp .env.example .env
docker compose up
```

Frontend: http://localhost:3000
Backend: http://localhost:5001

### Manual

```bash
cd backend && pip install -e . && python run.py
cd frontend && npm install && npm run dev
```

---

## Configuration

```env
LLM_API_KEY=your_key
LLM_MODEL_NAME=claude-sonnet-4-6
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
CURVE_VIRTUAL_SOL=30.0
CURVE_VIRTUAL_TOKENS=1073000000
GRADUATION_MARKET_CAP_SOL=85.0
TRADE_FEE_BPS=100
```

---

## Bonding Curve

| Parameter | Default | Description |
|-----------|---------|-------------|
| Virtual SOL reserve | 30 SOL | Seeds the curve's starting price |
| Virtual token reserve | 1.073B | Total tokens on the curve |
| Graduation market cap | 85 SOL | When liquidity migrates to DEX |
| Trade fee | 1% | Platform fee per buy/sell |
| Curve formula | x·y=k | Constant-product price discovery |

---

## Project Structure

```
axopad/
├── backend/
│   ├── app/
│   │   ├── api/        # token, trade, curve, feed endpoints
│   │   ├── models/     # Token, Trade, CurveState
│   │   ├── services/   # launcher, bonding curve, trade engine, graduation, LLM
│   │   └── utils/      # logger, cache, rate limiter, retry, helpers
│   └── scripts/        # simulate launch + trades
├── frontend/
│   └── src/
│       ├── views/      # Discover, Launch, Token, Portfolio
│       └── components/ # TokenCard, CurveChart, TradePanel
└── tests/
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT — see [LICENSE](LICENSE).

---

<div align="center">
<sub>Built on Solana. Fair by design. Every token on the curve.</sub>
</div>
