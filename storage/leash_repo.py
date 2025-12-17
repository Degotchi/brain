# storage/leash_repo.py
from typing import Optional
from uuid import UUID
from storage.supabase import supabase
from core.leash import Leash

def get_active_leash(pet_id: str) -> Optional[Leash]:
    """
    查询当前宠物被谁牵着（查找 Leash 表）
    Query which user is currently leashing this pet (query Leash table)
    """
    try:
        # 你的 Leash 表设计是 pet_id 为 PK，所以直接查 pet_id 即可
        # Your Leash table design uses pet_id as PK, so query by pet_id directly
        response = supabase.table("leash").select("*").eq("pet_id", pet_id).single().execute()
        
        if not response.data:
            return None # 这只宠物可能是流浪状态（没绳子） / This pet might be stray (no leash)
            
        return Leash(**response.data)
        
    except Exception as e:
        # 如果是查不到数据（API error），通常也当作 None 处理
        # If no data found (API error), usually treat as None
        # print(f"⚠️ 查找 Leash 失败或无数据 / Failed to find Leash or no data: {e}")
        return None