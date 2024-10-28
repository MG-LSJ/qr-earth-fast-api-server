from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import select, desc, func, col
from sqlmodel.ext.asyncio.session import AsyncSession
from src.entities.user.models import User


class PublicService:
    @staticmethod
    async def get_leaderboards_page(session: AsyncSession) -> Page[User]:
        """
        Get the leaderboard based on the number of redeemed codes
        """
        statement = select(User).order_by(desc(User.redeemed_code_count))
        return await paginate(session, statement)

    @staticmethod
    async def get_total_users(session: AsyncSession) -> int:
        """
        Get the total number of users
        """
        statement = select(func.count(col(User.id)))
        result = await session.exec(statement)
        count = result.one()
        return count
