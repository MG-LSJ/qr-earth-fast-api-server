from src.entities.public.service import PublicService
from src.db.main import async_session_maker
from src.db.redis import redis_cache, token_blocklist_cache


class Cache:
    @staticmethod
    async def init():
        print("Caching")
        async with async_session_maker() as session:  # type: ignore
            await Cache.__cache_total_users(session)

    @staticmethod
    async def __cache_total_users(session):
        total_users = await PublicService.get_total_users(session)
        await redis_cache.set("total_users", total_users)

    @staticmethod
    async def get_total_users():
        return await redis_cache.get("total_users")

    @staticmethod
    async def increment_total_users():
        await redis_cache.incr("total_users")


JTI_EXPIREY = 60 * 60 * 24  # 1 day


class JTIBlocklistCache:

    @staticmethod
    async def add(jti: str) -> None:
        await token_blocklist_cache.set(
            name=jti,
            value="",
            ex=JTI_EXPIREY,
        )

    @staticmethod
    async def exists(jti: str) -> bool:
        return await token_blocklist_cache.exists(jti) > 0
