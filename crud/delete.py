from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import database.models as models


async def delete_user(session: AsyncSession, user_id: int) -> models.User | None:
    """
    Delete a user and all their codes.
    """
    stmt = select(models.User).filter(models.User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if user is None:
        return None

    # for code in user.codes:
    #     await session.delete(code)

    await session.delete(user)
    await session.commit()
    return user
