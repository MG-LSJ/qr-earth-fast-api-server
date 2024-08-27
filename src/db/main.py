from sqlmodel import create_engine, SQLModel
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


async def init_db():
    async with engine.begin() as conn:
        from src.entities.user.models import User
        from src.entities.code.models import QRCode
        from src.entities.transaction.models import Transaction

        await conn.run_sync(SQLModel.metadata.create_all)


# SQL Model dosent support async natively
# Ingroing type checking


async def get_session() -> AsyncSession:  # type: ignore
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore
    async with async_session() as session:  # type: ignore
        yield session  # type: ignore
