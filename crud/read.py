import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import database.models
from typing import Sequence
from sqlalchemy.orm import joinedload


async def get_user_by_username(
    session: AsyncSession, username: str
) -> database.models.User | None:
    """
    Get a user by their username.
    """
    stmt = select(database.models.User).filter(
        database.models.User.username == username
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_email(
    session: AsyncSession, email: str
) -> database.models.User | None:
    """
    Get a user by their email.
    """
    stmt = select(database.models.User).filter(database.models.User.email == email)
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_phone_number(
    session: AsyncSession, phone_number: str
) -> database.models.User | None:
    """
    Get a user by their phone number.
    """
    stmt = select(database.models.User).filter(
        database.models.User.phone_number == phone_number
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_id(
    session: AsyncSession, user_id: uuid.UUID
) -> database.models.User | None:
    """
    Get a user by their id.
    """
    stmt = select(database.models.User).filter(database.models.User.id == user_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_leaderboard(
    session: AsyncSession, limit: int = 10
) -> Sequence[database.models.User]:
    """
    Get the top users by number of codes.
    """
    stmt = (
        select(database.models.User)
        .order_by(database.models.User.codes_count.desc())
        .limit(limit)
    )
    result = await session.execute(stmt)

    return result.scalars().all()


async def get_user_codes(
    session: AsyncSession, user_id: uuid.UUID, limit: int = 20
) -> list[database.models.QRCode] | None:
    """
    Get all codes for a user.
    """
    stmt = (
        select(database.models.User)
        .options(joinedload(database.models.User.codes))
        .filter(database.models.User.id == user_id)
        .limit(limit)
    )
    result = await session.execute(stmt)

    db_user = result.scalars().first()
    if db_user is None:
        return None

    codes = db_user.codes
    return codes


async def get_code_by_id(
    session: AsyncSession, code_id: uuid.UUID
) -> database.models.QRCode | None:
    """
    Get a code by its id.
    """
    stmt = select(database.models.QRCode).filter(database.models.QRCode.id == code_id)
    result = await session.execute(stmt)
    return result.scalars().first()
