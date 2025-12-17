# agents/investment.py
from agents.base import BaseAgent
from core.context import DecisionContext

class InvestmentAgent(BaseAgent):
    name = "investment_agent"

    def should_activate(self, ctx: DecisionContext) -> float:
        # 逻辑：如果风险偏好 > 0.5，我就想投资。风险偏好越高分数越高。
        # Logic: if risk profile > 0.5, want to invest. Higher risk profile = higher score.
        if ctx.pet.risk_profile > 0.5:
            return (ctx.pet.risk_profile - 0.5) / 0.5  # 0.0 ~ 1.0
        return 0.0

    def propose(self, ctx: DecisionContext) -> dict:
        return { "type": "investment_request", "reason": f"My risk profile is at {ctx.pet.risk_profile}, I want to invest!", "action": "ask_user_for_investment" }