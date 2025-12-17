# agents/base.py
from abc import ABC, abstractmethod
from typing import Optional
from core.context import DecisionContext
# from core.proposal import Proposal # (假设你有这个类，如果没有暂时返回 dict) / (assuming you have this class, if not return dict temporarily)

class BaseAgent(ABC):
    name: str = "base_agent"

    @abstractmethod
    def should_activate(self, ctx: DecisionContext) -> float:
        """
        返回激活的优先级分数 (0.0 - 1.0)
        0.0 = 不激活
        1.0 = 必须立刻执行
        Return activation priority score (0.0 - 1.0)
        0.0 = not activated
        1.0 = must execute immediately
        """
        pass

    @abstractmethod
    def propose(self, ctx: DecisionContext) -> dict:
        """
        生成 Proposal 的 payload (具体内容)
        Generate Proposal payload (specific content)
        """
        pass