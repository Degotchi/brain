# Degotchi Brain infos

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

# Degotchi Brain Service Architecture

This directory follows a **Domain-Driven Design (DDD)** approach, separating core logic, storage infrastructure, and agent behaviors.

## Directory Structure

```text
brain/
├── .env                        # [Config] Environment variables (API Keys, URLs) | 环境变量与密钥
├── .gitignore                  # [Config] Git ignore rules | Git 忽略文件
├── requirements.txt            # [Config] Python dependencies | 项目依赖包列表
├── main.py                     # [Entry] Service Entry Point (FastAPI + Loop) | 服务启动入口
│
├── core/                       # [Domain] Pure Data Models (Pydantic) | 核心领域模型 (无业务逻辑)
│   ├── context.py              # DecisionContext (State Snapshot) | 决策上下文 (宠物+用户+市场快照)
│   ├── enums.py                # Status & Action Enums | 状态与行为枚举
│   ├── leash.py                # [NEW] Leash Model (Relationship) | 牵引绳模型 (绑定关系与限额)
│   ├── pet.py                  # Pet State Model | 宠物状态模型 (饥饿/心情/等级)
│   ├── proposal.py             # Proposal Schema | 提案结构 (Agent 的输出结果)
│   └── user.py                 # User Model | 用户模型 (偏好设置)
│
├── storage/                    # [Infra] Database Repositories | 数据持久化层 (Supabase)
│   ├── conversation_repo.py    # Chat History CRUD | 对话记录存取
│   ├── leash_repo.py           # [NEW] Active Leash Lookup | 关系查询 (查找当前主人)
│   ├── pet_repo.py             # Pet State CRUD | 宠物状态存取
│   ├── proposal_repo.py        # Proposal Persistence | 提案保存
│   ├── user_repo.py            # User Preferences Lookup | 用户信息查询
│   └── supabase.py             # DB Client Instance | 数据库连接单例
│
├── agents/                     # [Logic] Behavioral Agents | 行为智能体 (业务逻辑)
│   ├── __init__.py             # Package init
│   ├── base.py                 # Abstract Base Class | Agent 基类 (定义接口)
│   ├── dialogue.py             # Chat Logic | 对话 Agent
│   ├── hunger.py               # Survival Logic | 饥饿与进食 Agent
│   ├── investment.py           # DeFi Logic | 投资与交易 Agent
│   └── mood.py                 # Emotional Logic | 情绪变化 Agent
│
├── orchestrator/               # [Control] Decision Engine | 调度引擎
│   ├── cooldown.py             # Rate Limiting | 冷却时间管理
│   ├── priority.py             # Conflict Resolution | 优先级仲裁
│   └── selector.py             # Agent Selector | 选择器 (决定当前激活哪个 Agent)
│
├── scheduler/                  # [Trigger] Time-based Events | 时间驱动模块
│   ├── jobs.py                 # Cron Jobs | 定时任务定义
│   └── tick.py                 # Heartbeat Logic | 心跳主逻辑 (Tick -> Context -> Select -> Save)
│
├── api/                        # [Interface] HTTP API | 外部接口
│   ├── deps.py                 # Dependencies | 依赖注入
│   ├── routes.py               # API Endpoints | 路由定义
│   └── schemas.py              # API DTOs | 数据传输对象
│
├── ai/                         # [Adapter] LLM Integration | AI 模型适配层
│   ├── base.py                 # LLM Interface | 模型抽象接口
│   ├── openai.py               # OpenAI Implementation | OpenAI 调用实现
│   ├── gemini.py               # Gemini Implementation | Gemini 调用实现
│   └── prompts/                # Prompt Templates | 提示词模板文件夹
│       ├── dialogue.txt
│       ├── investment.txt
│       └── mood.txt
│
├── signals/                    # [Input] External Data Feeds | 外部信号源
│   ├── market.py               # Crypto Prices | 市场价格抓取
│   ├── trends.py               # Social Trends | 社交热点
│   └── watchlist.py            # Token Watchlist | 监控代币列表
│
├── social/                     # [Output] Social Media Integration | 社交媒体输出
│   ├── formatter.py            # Text Formatting | 文本格式化
│   └── twitter.py              # Twitter Client | 推特发帖客户端
│
├── personality/                # [Logic] RNG & Evolution | 人格演化与随机性
│   ├── evolution.py            # Stat Changes | 属性成长计算
│   ├── randomness.py           # RNG Utilities | 随机数工具
│   └── traits.py               # Personality Traits | 性格特质定义
│
├── config/                     # [Config] Global Settings | 全局配置
│   ├── constants.py            # Game Constants | 游戏数值常量
│   └── settings.py             # Env Loader | 环境变量加载器
│
└── tests/                      # [Test] Unit & Integration Tests | 测试用例
    ├── test_agents.py
    └── test_tick.py
