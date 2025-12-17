# main.py
import asyncio
from scheduler.tick import tick

if __name__ == "__main__":
    # 换成你真实的 pet_id
    # Replace with your real pet_id
    TEST_PET_ID = "a6da0115-5976-4f81-8f4a-fa458206cb9e"
    
    # 因为 tick 是 async 的，需要用 asyncio 运行
    # Since tick is async, need to run with asyncio
    asyncio.run(tick(TEST_PET_ID))