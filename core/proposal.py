# core/proposal.py
from pydantic import BaseModel, Field, ConfigDict
from core.enums import ProposalStatus, ExecutorType
from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime

class Proposal(BaseModel):
    model_config = ConfigDict(extra='ignore')

    # 生成一个新 UUID，如果是从数据库读出来的，会覆盖这个值
    # Generate a new UUID, will be overwritten if read from database
    id: UUID = Field(default_factory=uuid4)
    pet_id: UUID
    
    # 核心内容
    # Core content
    type: str             # 例如: "feed", "trade", "tweet" / e.g.: "feed", "trade", "tweet"
    status: ProposalStatus = ProposalStatus.PENDING_USER
    payload: Dict[str, Any] = {}  # 具体的动作参数，比如 {"food_type": "steak"} / Specific action params, e.g. {"food_type": "steak"}
    
    # AI 的自我评估
    # AI's self-assessment
    confidence: float = 1.0
    reason: str = ""
    
    # 时间戳
    # Timestamp
    created_at: datetime = Field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None

    # 执行器
    # executor
    executor: ExecutorType = ExecutorType.FEED