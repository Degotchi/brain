# executors/__init__.py
from core.enums import ExecutorType
from executors.feed import FeedExecutor
# from executors.invest import InvestExecutor

# 注册表
# Registry
EXECUTOR_REGISTRY = {
    ExecutorType.FEED: FeedExecutor(),
    # ExecutorType.INVEST: InvestExecutor(),
}

def get_executor(executor_type: str):
    # 根据执行器类型获取对应的执行器实例
    # Get executor instance by executor type
    return EXECUTOR_REGISTRY.get(executor_type)