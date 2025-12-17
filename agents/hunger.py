# agents/hunger.py
from agents.base import BaseAgent
from core.context import DecisionContext
from typing import Dict, Any

class HungerAgent(BaseAgent):
    name: str = "hunger_agent"

    def should_activate(self, ctx: DecisionContext) -> float:
        """
        激活逻辑：
        饥饿度 0-100。
        如果 > 50 开始有反应。
        如果 > 90 优先级极高 (0.9)。
        Activation logic:
        Hunger level 0-100.
        If > 50, start reacting.
        If > 90, extremely high priority (0.9).
        """
        hunger = ctx.pet.hunger
        
        if hunger < 50:
            return 0.0
        
        # 归一化：(50~100) -> (0.0~1.0)
        # Normalize: (50~100) -> (0.0~1.0)
        score = (hunger - 50) / 50.0
        return min(score, 1.0)

    def propose(self, ctx: DecisionContext) -> Dict[str, Any]:
        """
        决定具体干什么
        Decide what to do specifically
        """
        return {
            "type": "feed",
            "action": "request_food",
            "reason": f"I am starving (Hunger: {ctx.pet.hunger})",
            "params": {
                "amount": 10,
                "food_id": "default_kibble"
            }
        }