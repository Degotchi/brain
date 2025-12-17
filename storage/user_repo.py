# storage/user_repo.py
from typing import Optional
from uuid import UUID
from storage.supabase import supabase
from core.user import User

def load_user(user_id: UUID) -> Optional[User]:
    try:
        # 去 users 表查找
        # Query users table
        response = supabase.table("users").select("*").eq("id", str(user_id)).single().execute()
        
        if not response.data:
            return None
            
        return User(**response.data)
    except Exception as e:
        print(f"❌ 读取用户失败 / Failed to load user: {e}")
        return None