from calendar import c
from typing import Sequence
from sqlmodel import select, desc, func, col
from sqlmodel.ext.asyncio.session import AsyncSession

from src.entities.user.models import User


class PublicService:
    @staticmethod
    async def get_leaderboard(session: AsyncSession, limit: int) -> Sequence[User]:
        """
        Get the leaderboard based on the number of redeemed codes
        """
        statement = select(User).order_by(desc(User.redeemed_code_count)).limit(limit)
        result = await session.exec(statement)
        return result.all()

    @staticmethod
    async def get_total_users(session: AsyncSession) -> int:
        """
        Get the total number of users
        """
        statement = select(func.count(col(User.id)))
        result = await session.exec(statement)
        count = result.one()
        return count
