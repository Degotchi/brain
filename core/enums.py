# core/enums.py
from enum import Enum

class ProposalStatus(str, Enum):
    CREATED = "created"             # 刚生成，还没发给用户 / Just created, not sent to user yet
    PENDING_USER = "pending_user"   # 已推送，等用户审批 / Pushed, waiting for user approval
    APPROVED = "approved"           # 用户点了同意 / User approved
    REJECTED = "rejected"           # 用户点了拒绝 / User rejected
    EXECUTED = "executed"           # 链上或逻辑已执行完毕 / On-chain or logic execution completed
    EXPIRED = "expired"             # 超时未处理 / Expired without processing
    FAILED = "failed"               # 执行过程中出错了 / Error occurred during execution

class ExecutorType(str, Enum):
    FEED = "feed_executor"          # 喂食执行器 / Feed executor
    INVEST = "invest_executor"      # 投资执行器 / Investment executor
    SOCIAL = "social_executor"      # 社交执行器 / Social executor