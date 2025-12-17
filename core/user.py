# core/user.py
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Dict, Any, Optional

class User(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: UUID
    wallet_address: Optional[str] = None
    preferences: Dict[str, Any] = {} # 例如 {"risk_tolerance": "high"} / e.g. {"risk_tolerance": "high"}