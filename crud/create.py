from sqlalchemy.ext.asyncio import AsyncSession
import database.models as models, schemas


async def create_user(session: AsyncSession, user: schemas.UserCreate) -> models.User:
    """
    Create a new user in the database and return the created user.
    """
    db_user = models.User(
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        hashed_password=user.hashed_password,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def create_code(session: AsyncSession) -> models.QRCode:
    """
    Create a new code in the database and return the created code.
    """
    db_code = models.QRCode()
    session.add(db_code)
    await session.commit()
    await session.refresh(db_code)
    return db_code
