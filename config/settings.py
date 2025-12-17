# config/settings.py
import os
from dotenv import load_dotenv

# 加载 .env 文件
# Load .env file
load_dotenv()

class Settings:
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # 以后可以在这里加 OPENAI_API_KEY 等
    # Can add OPENAI_API_KEY etc. here later

    def validate(self):
        if not self.SUPABASE_URL or not self.SUPABASE_KEY:
            raise ValueError("❌ 缺少必要的环境变量：SUPABASE_URL 或 SUPABASE_KEY / Missing required env vars: SUPABASE_URL or SUPABASE_KEY")

settings = Settings()
settings.validate()