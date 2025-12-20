import redis.asyncio as redis
import json
import os
from typing import Optional, Any

class RedisClient:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.client: Optional[redis.Redis] = None
    
    async def connect(self):
        """Connect to Redis"""
        self.client = redis.from_url(self.redis_url, decode_responses=True)
        
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.client:
            await self.client.close()
    
    async def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Set a key-value pair with optional expiration"""
        if not self.client:
            await self.connect()
        
        serialized_value = json.dumps(value) if not isinstance(value, str) else value
        return await self.client.set(key, serialized_value, ex=expire)
    
    async def get(self, key: str) -> Optional[Any]:
        """Get a value by key"""
        if not self.client:
            await self.connect()
        
        value = await self.client.get(key)
        if value is None:
            return None
        
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    
    async def delete(self, key: str) -> bool:
        """Delete a key"""
        if not self.client:
            await self.connect()
        
        return bool(await self.client.delete(key))
    
    async def exists(self, key: str) -> bool:
        """Check if a key exists"""
        if not self.client:
            await self.connect()
        
        return bool(await self.client.exists(key))

# Global Redis client instance
redis_client = RedisClient()