from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.redis import close_redis
from src.utils.config import Config
from sqlalchemy.orm import sessionmaker

DATABASE_URL = f"postgresql+asyncpg://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"

engine = AsyncEngine(
    create_engine(
        url=DATABASE_URL,
        echo=False,
    )
)

# SQL Model dosent support async natively
# Ingroing type checking

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore


async def get_session() -> AsyncSession:  # type: ignore
    async with async_session_maker() as session:  # type: ignore
        yield session  # type: ignore


# Migrations and caching

from src.db.cache import Cache
from src.db.migrartions import run_migrations


async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(run_migrations)
    await Cache.init()


async def shutdown():
    await engine.dispose()
    await close_redis()
