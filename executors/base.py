# executors/base.py
from abc import ABC, abstractmethod
from core.proposal import Proposal
from core.context import DecisionContext

class BaseExecutor(ABC):
    @abstractmethod
    async def execute(self, proposal: Proposal, ctx: DecisionContext) -> bool:
        """
        执行具体的业务逻辑
        Execute specific business logic
        :return: True if success, False if failed
        """
        pass