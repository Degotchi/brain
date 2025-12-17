# executors/feed.py
from executors.base import BaseExecutor
from core.proposal import Proposal
from core.context import DecisionContext
from storage.pet_repo import update_pet_state 

class FeedExecutor(BaseExecutor):
    async def execute(self, proposal: Proposal, ctx: DecisionContext) -> bool:
        print(f"🍽️ 执行喂食 / Executing feed: {proposal.payload}")
        
        # 1. 解析参数
        # 1. Parse parameters
        params = proposal.payload.get("params", {})
        amount = params.get("amount", 0)
        
        # 2. 修改状态 (模拟业务逻辑)
        # 2. Update state (simulate business logic)
        # 这里应该去扣减用户的代币（如果需要付费），然后增加宠物饱食度
        # Should deduct user tokens (if payment required), then increase pet satiety
        current_hunger = ctx.pet.hunger
        new_hunger = max(0, current_hunger - amount) # 饱食度增加 = 饥饿度减少 / Satiety increase = hunger decrease
        
        ctx.pet.hunger = new_hunger
        
        # 3. 写入数据库
        # 3. Write to database
        try:
            update_pet_state(ctx.pet)
            print(f"✅ 喂食成功！饥饿度从 {current_hunger} 降至 {new_hunger} / Feed successful! Hunger decreased from {current_hunger} to {new_hunger}")
            return True
        except Exception as e:
            print(f"❌ 喂食失败 / Feed failed: {e}")
            return False