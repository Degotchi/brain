# storage/supabase.py
from supabase import create_client, Client
from config.settings import settings

# 初始化客户端
# Initialize client
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# 这是一个单例，以后所有 Repo 都引用这个变量
# This is a singleton, all Repos will reference this variable