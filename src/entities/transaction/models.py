from datetime import datetime, timezone
import sqlalchemy.dialects.postgresql as pg
import uuid
from sqlmodel import Field, SQLModel, Column
from src.entities.user.models import User


class Transaction(SQLModel, table=True):
    """
    Point transaction table
    """

    __tablename__ = "transactions"  # type: ignore

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            default=uuid.uuid4,
        ),
    )
    user_id: uuid.UUID = Field(
        foreign_key="users.id",
    )
    amount: int
    timestamp: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            default=lambda: datetime.now(timezone.utc),
        ),
    )
