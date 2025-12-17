# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router
from scheduler.tick import tick
import asyncio
from contextlib import asynccontextmanager

# 生命周期管理：启动时做什么，关闭时做什么
# Lifecycle management: what to do on startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Brain Service Starting... / Brain Service Starting...")
    # 这里可以启动后台 Scheduler 任务
    # Can start background Scheduler tasks here
    yield
    print("🛑 Brain Service Stopping... / Brain Service Stopping...")

app = FastAPI(title="Degotchi Brain API", lifespan=lifespan)

# 配置 CORS 中间件
# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有源，生产环境应指定具体域名 / Dev: allow all origins, prod should specify domains
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法 / Allow all HTTP methods
    allow_headers=["*"],  # 允许所有请求头 / Allow all request headers
)

# 注册路由
# Register routes
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    # 启动命令：python main.py
    # Startup command: python main.py
    # 访问文档：http://127.0.0.1:8000/docs
    # Access docs: http://127.0.0.1:8000/docs
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)