# storage/proposal_repo.py
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from typing import List
# 导入基础常量
# Import base constants
from storage.supabase import supabase
from core.proposal import Proposal
from core.enums import ProposalStatus

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
        print(f"💾 提案已保存 / Proposal Saved: {proposal.id} [{proposal.type}]")
        
    except Exception as e:
        print(f"❌ 保存提案失败 / Failed to save proposal: {e}")
        raise e

def load_proposal(proposal_id: UUID) -> Optional[Proposal]:
    """
    从数据库加载提案（通过 proposal_id）
    Load a proposal from the database with proposal_id
    """
    try:
        # .single() 确保返回单条记录而不是数据列表
        # .single() ensures returning a single record instead of a data list
        response = supabase.table("proposals") \
            .select("*")\
            .eq("id", str(proposal_id))\
            .single()\
            .execute()
        if not response.data:
            return None
        print(f"🔍 提案已加载 / Proposal Loaded: {response.data}")
        # Pydantic 魔法：将字典转换为 Proposal 对象
        # Pydantic magic: convert dict to Proposal object
        return Proposal(**response.data)
        
    except Exception as e:
        print(f"❌ 加载提案失败 / Error loading proposal {proposal_id}: {e}")
        return None

def update_proposal_status(
    proposal_id: UUID, 
    status: ProposalStatus,
    metadata: Dict[str, Any] = None
):
    """
    更新提案状态（比如 Pending -> Approved -> Executed）
    Update proposal status (e.g., Pending -> Approved -> Executed)
    :param metadata: 可选，用于存执行结果或错误信息，会合并进 payload 或单独存
    :param metadata: Optional, for storing execution results or error info, will be merged into payload or stored separately
    """
    try:
        update_data={
            "status": status.value
        }

        # 如果执行成功，保存执行时间
        # If execution succeeds, save execution time
        if status == ProposalStatus.EXECUTED:
            update_data["executed_at"] = datetime.now().isoformat()

        # TODO: proposals 表加一个 error_log 字段
        # TODO: add error_log field to proposals table
        
        supabase.table("proposals") \
            .update(update_data) \
            .eq("id", str(proposal_id)) \
            .execute()
            
        print(f"🔄 状态已更新 / Status Updated: {proposal_id} -> {status.value}")
        
    except Exception as e:
        print(f"❌ 更新状态失败 / Error updating status for {proposal_id}: {e}")
        raise e

def get_proposals_by_status(status: ProposalStatus) -> List[Proposal]:
    """
    根据状态获取所有提案（用于批量执行）
    Get all proposals by status (for batch execution)
    """
    try:
        response = supabase.table("proposals") \
            .select("*")\
            .eq("status", status.value)\
            .execute()

        return [Proposal(**item) for item in response.data]
    except Exception as e:
        print(f"❌ 按状态获取提案失败 / Error getting proposals by status {status}: {e}")
        return []