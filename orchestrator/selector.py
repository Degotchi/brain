# orchestrator/selector.py
from typing import List, Optional
from agents.base import BaseAgent
from core.context import DecisionContext

# 注册所有的 Agents
# Register all Agents
from agents.hunger import HungerAgent
from agents.investment import InvestmentAgent
# from agents.mood import MoodAgent ...

# 实例化 Agent 池
# Instantiate Agent pool
AVAILABLE_AGENTS: List[BaseAgent] = [
    HungerAgent(),
    InvestmentAgent(),
    # MoodAgent(),
]

def select_agent(ctx: DecisionContext) -> Optional[BaseAgent]:
    """
    遍历所有 Agent，返回分数最高的那个（胜出者）
    Iterate through all Agents, return the one with highest score (winner)
    """
    best_agent = None
    best_score = 0.0
    
    # 阈值：如果分数太低（比如都只是 0.1），可能就不做任何事
    # Threshold: if score is too low (e.g., all 0.1), might do nothing
    MIN_THRESHOLD = 0.2 

    print(f"🕵️ 正在评估 {len(AVAILABLE_AGENTS)} 个 Agent... / Evaluating {len(AVAILABLE_AGENTS)} Agents...")

    for agent in AVAILABLE_AGENTS:
        score = agent.should_activate(ctx)
        print(f"   [{agent.name}] 得分 / Score: {score:.2f}")

        if score > best_score:
            best_score = score
            best_agent = agent
    
    if best_score < MIN_THRESHOLD:
        print("💤 所有 Agent 得分过低，继续睡觉 / All Agents scored too low, continue sleeping")
        return None

    print(f"👉 选中 Agent / Selected Agent: {best_agent.name} (得分 / Score: {best_score:.2f})")
    return best_agent