# scheduler/tick.py
import asyncio
from uuid import UUID

from storage.pet_repo import load_pet
from storage.leash_repo import get_active_leash
from storage.user_repo import load_user
from storage.proposal_repo import save_proposal

from core.context import DecisionContext
from core.proposal import Proposal
from orchestrator.selector import select_agent

async def tick(pet_id: str):
    # 1. 转换 ID 格式
    # 1. Convert ID format
    try:
        pet_uuid = UUID(pet_id)
    except ValueError:
        print(f"❌ 无效的 UUID / Invalid UUID: {pet_id}")
        return

    print(f"\n⏰ Tick 开始 / Tick started: {pet_uuid}")

    # 2. 加载数据 (Pet)
    # 2. Load data (Pet)
    pet = load_pet(pet_id)
    if not pet:
        print("❌ 找不到宠物数据 / Pet data not found")
        return

    # 3. 加载关系链 (Pet -> Leash -> User)
    # 3. Load relationship chain (Pet -> Leash -> User)
    leash = get_active_leash(pet_id)

    user = None
    allowance = 0.0
    user_prefs = {}
    if leash:
        print(f"🔗 发现 Leash关系 / Leash relationship found: Owner={leash.user_id}, Limit={leash.allowance_limit}")
        allowance = leash.allowance_limit
        
        # 只有存在 Leash 时，才去加载 User
        # Only load User when Leash exists
        user = load_user(leash.user_id)
        if user:
            user_prefs = user.preferences
            print(f"👤 加载用户偏好 / User preferences loaded: {user_prefs.keys()}")
    else:
        print("🍃 这是一只流浪宠物 (无 Leash 绑定) / This is a stray pet (no Leash binding)")
        # 流浪宠物的逻辑：没有 user_prefs，allowance = 0
        # Stray pet logic: no user_prefs, allowance = 0

    # 4. 构建上下文 (Context)
    # 4. Build context (Context)
    ctx = DecisionContext(
        pet=pet,
        user_prefs=user_prefs,
        allowance=allowance,  # ✅ 传入限额 / Pass allowance limit
        market_data={}        # MVP 先留空 / MVP: leave empty for now
    )


    # 5. 调度 (选 Agent)
    # 5. Schedule (select Agent)
    agent = select_agent(ctx)
    if not agent:
        return # 无事发生 / Nothing to do

    # 6. 执行 (生成 Payload)
    # 6. Execute (generate Payload)
    proposal_payload = agent.propose(ctx)

    # 7. 封装为 Proposal 对象
    # 7. Wrap as Proposal object
    proposal = Proposal(
        pet_id=pet.id,
        type=proposal_payload.get("type", "unknown"),
        payload=proposal_payload,
        reason=proposal_payload.get("reason", "Agent triggered"),
        confidence=0.9 # 这里可以是 Agent 返回的，也可以写死 / Can be returned by Agent or hardcoded
    )

    # 8. 保存到数据库
    # 8. Save to database
    save_proposal(proposal)
    
    print("🏁 Tick 结束: 提案已生成 / Tick ended: proposal generated")