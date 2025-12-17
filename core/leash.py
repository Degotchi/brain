# core/leash.py
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class Leash(BaseModel):
    model_config = ConfigDict(extra='ignore')

    pet_id: UUID
    user_id: UUID
    allowance_limit: float = 0.0
    # created_at 等字段如果是只读的，可以不写，或者写成 Optional
    # If fields like created_at are read-only, can omit or write as Optional