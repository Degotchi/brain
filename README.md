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

brain/
├── main.py                 # 服务入口（FastAPI / Scheduler）
│
├── core/                   # 核心领域模型（不依赖 AI）
│   ├── pet.py              # Pet 状态模型
│   ├── user.py             # User 偏好
│   ├── proposal.py         # Proposal 统一结构
│   ├── enums.py            # 状态 / 行为枚举
│   └── context.py          # 决策上下文（DecisionContext）
│
├── agents/                 # 行为 Agent（AI or Rule）
│   ├── investment.py
│   ├── dialogue.py
│   ├── hunger.py
│   ├── mood.py
│   └── __init__.py
│
├── orchestrator/           # 决策调度（不使用 AI）
│   ├── selector.py         # 选哪个 Agent
│   ├── priority.py         # 优先级 & 冲突解决
│   └── cooldown.py         # 冷却时间
│
├── signals/                # 外部“原料”
│   ├── market.py
│   ├── trends.py
│   ├── watchlist.py
│   └── __init__.py
│
├── personality/            # 人格 & 随机性
│   ├── traits.py
│   ├── randomness.py
│   └── evolution.py
│
├── ai/                     # AI 适配层（可替换）
│   ├── base.py             # 抽象接口
│   ├── openai.py
│   ├── gemini.py
│   └── prompts/
│       ├── investment.txt
│       ├── dialogue.txt
│       └── mood.txt
│
├── scheduler/              # 时间驱动
│   ├── tick.py
│   └── jobs.py
│
├── api/                    # HTTP / RPC 接口
│   ├── routes.py
│   ├── schemas.py
│   └── deps.py
│
├── storage/                # 数据持久化
│   ├── supabase.py
│   ├── pet_repo.py
│   ├── proposal_repo.py
│   └── conversation_repo.py
│
├── social/                 # 对外表达（Twitter 等）
│   ├── twitter.py
│   └── formatter.py
│
├── config/
│   ├── settings.py
│   └── constants.py
│
├── tests/                  # 单元测试（占位即可）
│
└── README.md               # Brain 子项目说明
