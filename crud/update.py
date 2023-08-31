import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import database.models


async def update_user_username(
    session: AsyncSession, user_id: int, username: str
) -> database.models.User | None:
    """
    Update a user's username.
    """
    stmt = select(database.models.User).filter(database.models.User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if user is None:
        return None
    user.username = username
    await session.commit()
    await session.refresh(user)
    return user


async def update_user_email(
    session: AsyncSession, user_id: int, email: str
) -> database.models.User | None:
    """
    Update a user's email.
    """
    stmt = select(database.models.User).filter(database.models.User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if user is None:
        return None
    user.email = email
    await session.commit()
    await session.refresh(user)
    return user


async def update_user_phone_number(
    session: AsyncSession, user_id: int, phone_number: str
) -> database.models.User | None:
    """
    Update a user's phone number.
    """
    stmt = select(database.models.User).filter(database.models.User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if user is None:
        return None
    user.phone_number = phone_number
    await session.commit()
    await session.refresh(user)
    return user


async def update_user_password(
    session: AsyncSession, user_id: int, hashed_password: str
) -> database.models.User | None:
    """
    Update a user's password.
    """
    stmt = select(database.models.User).filter(database.models.User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if user is None:
        return None
    user.hashed_password = hashed_password
    await session.commit()
    await session.refresh(user)
    return user


async def redeem_code(
    session: AsyncSession, user_id: uuid.UUID, code_id: uuid.UUID
) -> int:
    stmt = select(database.models.User).filter(database.models.User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if user is None:
        return 0

    stmt = select(database.models.QRCode).filter(database.models.QRCode.id == code_id)
    result = await session.execute(stmt)
    code = result.scalars().first()

    if code is None:
        return 1
    if code.redeemed:
        return 3
    user.codes_count += 1
    code.redeemed = True
    code.user_id = user_id
    code.redeemed_at = datetime.datetime.utcnow()
    await session.commit()
    return 2
