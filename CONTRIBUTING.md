# Contributing to Axopad

PRs welcome.

## Setup
```bash
git clone https://github.com/Axopad/Axopad.git
cd Axopad && cp .env.example .env
npm run setup
```

## Tests
```bash
pytest tests/ -v
```
All mocked — no API keys needed. The bonding curve math is fully unit-tested.

## Branches
`feature/`, `hotfix/`, `chore/`

## Commits
Conventional: `feat:`, `fix:`, `chore:`, `docs:`

## Roadmap
- Real SPL token deployment (Metaplex / Token-2022)
- On-chain bonding curve program (Anchor)
- Real DEX graduation (Raydium / Meteora migration)
- WebSocket live price + trade feeds
- Holder distribution tracking
- Anti-bot / anti-snipe launch protection
- Creator fee revenue share
