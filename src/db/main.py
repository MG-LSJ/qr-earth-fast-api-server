from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import Config
from sqlalchemy.orm import sessionmaker


DATABASE_URL = f"postgresql+asyncpg://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"

engine = AsyncEngine(
    create_engine(
        url=DATABASE_URL,
        echo=True,
    )
)

# Use run_migration to create tables

from alembic import command, config


def __run_migrations(connection):
    alembic_config = config.Config("alembic.ini")
    alembic_config.attributes["connection"] = connection
    command.upgrade(alembic_config, "head")


async def migrate_db():
    async with engine.begin() as conn:
        await conn.run_sync(__run_migrations)


# SQL Model dosent support async natively
# Ingroing type checking


async def get_session() -> AsyncSession:  # type: ignore
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore
    async with async_session() as session:  # type: ignore
        yield session  # type: ignore
