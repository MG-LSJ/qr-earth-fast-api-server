import redis.asyncio as aioredis
from src.utils.config import Config


redis_cache = aioredis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    password=Config.REDIS_PASSWORD,
    db=0,
    decode_responses=True,
)

token_blocklist_cache = aioredis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    password=Config.REDIS_PASSWORD,
    db=1,
    decode_responses=True,
)


async def close_redis():
    print("Closing redis")
    await redis_cache.close()
    await token_blocklist_cache.close()
