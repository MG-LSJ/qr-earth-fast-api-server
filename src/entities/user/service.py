from datetime import datetime
import uuid
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from src.entities.transaction.models import Transaction
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from src.entities.user.models import User
from src.db.cache import Cache


class UserService:
    @staticmethod
    async def get_user_by_id(
        session: AsyncSession,
        user_id: uuid.UUID,
    ):
        """
        Get a user by their ID
        """
        statement = select(User).where(User.id == user_id)
        result = await session.exec(statement)
        return result.first()

    @staticmethod
    async def get_user_by_username(
        session: AsyncSession,
        username: str,
    ):
        """
        Get a user by their username
        """
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        return result.first()

    @staticmethod
    async def get_user_by_email(
        session: AsyncSession,
        email: str,
    ):
        """
        Get a user by their email
        """
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    @staticmethod
    async def get_user_by_phone_number(
        session: AsyncSession,
        phone_number: str,
    ):
        """
        Get a user by their phone number
        """
        statement = select(User).where(User.phone_number == phone_number)
        result = await session.exec(statement)
        return result.first()

    @staticmethod
    async def create_user(
        session: AsyncSession,
        user: User,
    ):
        """
        Create a new user
        """
        global TOTAL_USERS

        session.add(user)
        await session.commit()
        await session.refresh(user)
        await Cache.increment_total_users()
        return user

    @staticmethod
    async def update_user(
        session: AsyncSession,
        user: User,
    ):
        existing_user = await UserService.get_user_by_id(session, user.id)
        if existing_user is None:
            return None

        for field, value in user.model_dump().items():
            setattr(existing_user, field, value)

        await session.commit()
        await session.refresh(existing_user)
        return existing_user

    @staticmethod
    async def get_user_transactions_page(
        session: AsyncSession,
        user_id: uuid.UUID,
    ) -> Page[Transaction]:
        statement = (
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .order_by(desc(Transaction.timestamp))
        )
        return await paginate(session, statement)

    @staticmethod
    async def redeem_user_points(
        session: AsyncSession,
        user: User,
        points: int,
    ):
        user.points -= points
        transaction = Transaction(
            id=uuid.uuid4(),
            user_id=user.id,
            amount=-points,
            timestamp=datetime.now(),
        )

        session.add(transaction)
        await session.commit()
        await session.refresh(user)
        return user
