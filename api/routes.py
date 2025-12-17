from fastapi import APIRouter, HTTPException, BackgroundTasks
from uuid import UUID
from typing import List

from scheduler.tick import tick
from core.enums import ProposalStatus
from storage.proposal_repo import load_proposal, update_proposal_status, get_proposals_by_status
from storage.pet_repo import load_pet
from core.context import DecisionContext
from executors import get_executor

router = APIRouter()

# ==========================================
# 入口 1: Tick (系统心跳)
# Endpoint 1: Tick (system heartbeat)
# ==========================================
@router.post("/tick/{pet_id}")
async def trigger_tick(pet_id: str, background_tasks: BackgroundTasks):
    """
    触发一次tick，使用BackgroundTask避免阻塞API
    Trigger a tick, use BackgroundTask to avoid blocking API
    """
    try:
        UUID(pet_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="UUID for pet_id format")
    
    # 后台任务执行 tick
    # Background task to run tick
    background_tasks.add_task(tick, pet_id)
    
    return {
        "status": "tick accepted",
        "pet_id": pet_id
    }

# ==========================================
# 入口 2: Proposal 审批
# Endpoint 2: Proposal approval
# ==========================================
@router.post("/proposals/{proposal_id}/approve")
async def approve_proposal(proposal_id: UUID):
    # 1. 从数据库加载 Proposal
    # 1. Load Proposal from database
    proposal = load_proposal(proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    if proposal.status != ProposalStatus.PENDING_USER:
        raise HTTPException(status_code=400, detail=f"Cannot approve proposal in status: {proposal.status}")

    # 2. 标记为 Approved (先记录用户的意图)
    # 2. Mark as Approved (record user intent first)
    update_proposal_status(proposal_id, ProposalStatus.APPROVED)

    # 返回成功消息
    # Return success message
    return {"id": proposal_id, "status": ProposalStatus.APPROVED, "message": "Proposal approved by user"}

    # TODO: execute proposal
    # # 3. 寻找对应的 Executor
    # # 3. Find corresponding Executor
    # executor = get_executor(proposal.executor)
    # if not executor:    
    #     raise HTTPException(status_code=500, detail=f"No executor found for type: {proposal.executor}")

    # # 4. 构建上下文 (执行需要知道当前的最新状态)
    # # 4. Build context (execution needs current latest state)
    # pet = load_pet(str(proposal.pet_id))
    # # 这里省略了 load_user / leash 的过程，实际需要补全
    # # load_user / leash process omitted here, needs to be completed
    # ctx = DecisionContext(pet=pet) 

    # # 5. 执行逻辑
    # # 5. Execute logic
    # success = await executor.execute(proposal, ctx)

    # # 6. 更新最终状态
    # # 6. Update final status
    # final_status = ProposalStatus.EXECUTED if success else ProposalStatus.FAILED
    # update_proposal_status(proposal_id, final_status)

    # return {
    #     "proposal_id": proposal_id, 
    #     "final_status": final_status, 
    #     "message": "Execution finished"
    # }


@router.post("/proposals/{proposal_id}/reject")
async def reject_proposal(proposal_id: UUID):
    """
    用户拒绝提案
    User reject proposal
    """
    proposal = load_proposal(proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
        
    if proposal.status != ProposalStatus.PENDING_USER:
        raise HTTPException(status_code=400, detail=f"Cannot reject. Current status: {proposal.status}")

    # 更新状态为 REJECTED
    # Update status to REJECTED
    update_proposal_status(proposal_id, ProposalStatus.REJECTED)
    
    return {"id": proposal_id, "status": ProposalStatus.REJECTED, "message": "Proposal rejected by user"}


# ==========================================
# 入口 3: Executor Worker (后台执行器)
# Endpoint 3: Executor Worker (background executor)
# ==========================================
@router.post("/executor/run")
async def run_executor_worker():
    """
    批量执行所有状态为 APPROVED 的提案。
    接口由 CronJob 定时调用，或者在用户 Approve 后异步调用。
    Batch execute all proposals with APPROVED status.
    Called by CronJob periodically, or asynchronously after user Approve.
    """
    # 1. 获取所有状态为 APPROVED 的提案
    # 1. Get all proposals with APPROVED status
    tasks = get_proposals_by_status(ProposalStatus.APPROVED)

    results = []

    print(f"⚙️ 执行器工作器：找到 {len(tasks)} 个已批准的任务 / Executor Worker: Found {len(tasks)} approved tasks.")
    for proposal in tasks:
        task_result = {
            "id": proposal.id, 
            "executor": proposal.executor, 
            "success": False
        }

        try:
            # 2. 查找执行器
            # 2. Find executor
            executor = get_executor(proposal.executor)
            if not executor:
                print(f"❌ 执行器工作器：未找到执行器 / Executor Worker: No executor found for : {proposal.executor}")
                # 标记为 FAILED 防止死循环
                # Signal FAILED to prevent deadloop
                update_proposal_status(proposal.id, ProposalStatus.FAILED)
                continue

            # 3. 构建上下文
            # 3. Build context
            pet = load_pet(str(proposal.pet_id))
            if not pet:
                print(f"⚠️ 提案 {proposal.id} 未找到宠物 / Pet not found for proposal {proposal.id}")
                update_proposal_status(proposal.id, ProposalStatus.FAILED, metadata={"error": "Pet missing"})
                continue

            ctx = DecisionContext(pet=pet)
            # TODO: 添加 user/leash 上下文
            # TODO: add user/leash context

            # 4. 执行
            # 4. Execute
            success = await executor.execute(proposal, ctx)

            # 5. 更新最终结果 (EXECUTED 或 FAILED)
            # 5. Update final result (EXECUTED or FAILED)
            final_status = ProposalStatus.EXECUTED if success else ProposalStatus.FAILED
            update_proposal_status(proposal.id, final_status)
            
            task_result["success"] = success
            task_result["final_status"] = final_status

        except Exception as e:
            print(f"❌ 执行崩溃 / Execution crash: {e}")
            update_proposal_status(proposal.id, ProposalStatus.FAILED, metadata={"error": str(e)})
        
        results.append(task_result)

    return {"processed_count": len(results), "details": results}