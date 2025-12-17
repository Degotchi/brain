# storage/proposal_repo.py
from storage.supabase import supabase
from core.proposal import Proposal

def save_proposal(proposal: Proposal):
    try:
        # 1. 转成字典
        # 1. Convert to dictionary
        data = proposal.model_dump(mode='json')
        
        # 2. 插入数据库
        # 2. Insert into database
        # 注意：Supabase 的 uuid 字段需要字符串，pydantic 的 json mode 会自动处理 datetime
        # Note: Supabase uuid fields need strings, pydantic json mode automatically handles datetime
        supabase.table("proposals").insert(data).execute()
        
        print(f"✅ 提案已保存至 DB / Proposal saved to DB: ID={proposal.id}")
        
    except Exception as e:
        print(f"❌ 保存提案失败 / Failed to save proposal: {e}")