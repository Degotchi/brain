# Degotchi Brain

This folder contains the **Degotchi Brain** domain + decision stack.

- **core/**: domain models (no AI dependency)
- **agents/**: behavior agents (AI or rule-based)
- **orchestrator/**: agent selection, prioritization, cooldowns (no AI dependency)
- **signals/**: external inputs (market, trends, watchlist)
- **personality/**: traits, randomness, evolution
- **ai/**: AI adapter layer (swappable providers) + prompts
- **scheduler/**: time-driven ticks/jobs
- **api/**: HTTP/RPC routes + schemas + deps
- **storage/**: persistence adapters + repos
- **social/**: outbound expression (Twitter etc.)
- **config/**: settings/constants
- **tests/**: unit tests (placeholder)
