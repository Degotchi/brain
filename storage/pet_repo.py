# storage/pet_repo.py
from typing import Optional
from uuid import UUID
from storage.supabase import supabase
from core.pet import Pet

def load_pet(pet_id: str) -> Optional[Pet]:
    try:
        # 1. 查询
        # 1. Query
        response = supabase.table("pets").select("*").eq("id", pet_id).single().execute()
        
        # 2. 这里的 response.data 是一个字典
        # 2. response.data is a dictionary
        if not response.data:
            return None
            
        # 3. 这里的魔法：用 **dict 直接转成 Pet 对象
        # 3. Magic: convert dict to Pet object using **dict
        return Pet(**response.data)
        
    except Exception as e:
        print(f"❌ 读取宠物数据失败 / Failed to load pet data: {e}")
        return None

def save_pet_state(pet: Pet):
    # 将对象转回字典存入库
    # Convert object back to dictionary for storage
    # exclude={'id'} 防止更新时修改主键（虽然 Supabase 会忽略，但好习惯）
    # exclude={'id'} prevents updating primary key (Supabase will ignore, but good practice)
    data = pet.model_dump(exclude={'id'}) 
    
    supabase.table("pets").update(data).eq("id", str(pet.id)).execute()