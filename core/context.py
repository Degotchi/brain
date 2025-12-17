# core/context.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, Optional
from core.pet import Pet

class DecisionContext(BaseModel):
    pet: Pet
    
    # 用户偏好 (如果 Leash 不存在，则是空字典)
    # User preferences (empty dict if Leash doesn't exist)
    user_prefs: Dict[str, Any] = Field(default_factory=dict)
    
    # 当前的资金限额 (来自 Leash)
    # Current allowance limit (from Leash)
    allowance: float = 0.0
    
    # 市场数据
    # Market data
    market_data: Dict[str, Any] = Field(default_factory=dict)
    
    current_time: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True