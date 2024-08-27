from typing import Sequence
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from src.entities.user.models import User


class PublicService:
    @staticmethod
    async def get_leaderboard(session: AsyncSession, limit: int) -> Sequence[User]:
        """
        Get the leaderboard
        """
        statement = select(User).order_by(desc(User.points)).limit(limit)
        result = await session.exec(statement)
        return result.all()
