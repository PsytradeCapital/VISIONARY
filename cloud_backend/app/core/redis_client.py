"""
Redis cache configuration for cloud deployment
"""

import redis.asyncio as redis
from typing import Optional, Any
import json
import logging
from .config import settings

logger = logging.getLogger(__name__)

redis_client: Optional[redis.Redis] = None

async def init_redis():
    """Initialize Redis connection"""
    global redis_client
    try:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True,
            health_check_interval=30
        )
        
        # Test connection
        await redis_client.ping()
        logger.info("Redis connection established")
        
    except Exception as e:
        logger.error(f"Redis initialization failed: {e}")
        raise

async def get_redis_client() -> redis.Redis:
    """Get Redis client"""
    if not redis_client:
        await init_redis()
    return redis_client

class CacheService:
    """Redis cache service for cloud operations"""
    
    def __init__(self):
        self.client = None
    
    async def get_client(self):
        if not self.client:
            self.client = await get_redis_client()
        return self.client
    
    async def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Set cache value with expiration"""
        try:
            client = await self.get_client()
            serialized_value = json.dumps(value) if not isinstance(value, str) else value
            return await client.setex(key, expire, serialized_value)
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    async def get(self, key: str) -> Optional[Any]:
        """Get cache value"""
        try:
            client = await self.get_client()
            value = await client.get(key)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    async def delete(self, key: str) -> bool:
        """Delete cache key"""
        try:
            client = await self.get_client()
            return await client.delete(key) > 0
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        try:
            client = await self.get_client()
            return await client.exists(key) > 0
        except Exception as e:
            logger.error(f"Cache exists error: {e}")
            return False

cache_service = CacheService()