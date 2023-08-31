from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
import urllib.parse

# get environment variables
host_server = os.environ.get("host_server", "localhost")
db_server_port = urllib.parse.quote_plus(str(os.environ.get("db_server_port", "5432")))
database_name = os.environ.get("database_name", "fastapi")
db_username = urllib.parse.quote_plus(str(os.environ.get("db_username", "postgres")))
db_password = urllib.parse.quote_plus(str(os.environ.get("db_password", "secret")))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get("ssl_mode", "prefer")))

sqlite_url: str = "sqlite+aiosqlite:///db.sqlite3"
pg_url: str = f"postgresql+asyncpg://{db_username}:{db_password}@{host_server}:{db_server_port}/{database_name}?sslmode={ssl_mode}"

asyncEngine = create_async_engine(
    sqlite_url,
    connect_args={"check_same_thread": False},
)

AsyncSession = async_sessionmaker(
    bind=asyncEngine,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSession() as session:
        yield session


class Base(DeclarativeBase):
    pass
