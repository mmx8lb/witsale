import aioredis
from app.core.config import settings


class RedisClient:
    """Redis客户端管理"""
    
    def __init__(self):
        self.redis = None
    
    async def init_redis(self):
        """初始化Redis连接"""
        self.redis = await aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
    
    async def close(self):
        """关闭Redis连接"""
        if self.redis:
            await self.redis.close()
    
    async def get(self, key: str) -> str:
        """获取缓存"""
        return await self.redis.get(key)
    
    async def set(self, key: str, value: str, expire: int = None) -> bool:
        """设置缓存"""
        if expire:
            return await self.redis.setex(key, expire, value)
        return await self.redis.set(key, value)
    
    async def delete(self, key: str) -> int:
        """删除缓存"""
        return await self.redis.delete(key)
    
    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        return await self.redis.exists(key) > 0


# 创建全局Redis客户端实例
redis_client = RedisClient()
