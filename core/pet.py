# core/pet.py
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal

class Pet(BaseModel):
    id: UUID  # Pydantic 会自动把字符串 UUID 转成对象 / Pydantic automatically converts string UUID to object
    created_at: datetime
    updated_at: datetime
    nft_address: str
    level: int = 1
    exp: int = 0
    mood: str = "happy"  # 数据库默认值是 'happy' / Database default is 'happy'
    hunger: int = 0
    risk_profile: float = 0.5  # double precision
    allowance: Decimal = Decimal("0")  # numeric 类型，使用 Decimal 更精确 / numeric type, use Decimal for precision
    