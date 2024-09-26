from datetime import datetime
import uuid
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg

from src.entities.user.models import User


class QRCodeBase(SQLModel):
    __tablename__ = "codes"  # type: ignore

    id: uuid.UUID = Field(
        sa_column=Column(
            type_=pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )

    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now,
        ),
    )

    value: int = Field(default=10)


class QRCode(QRCodeBase, table=True):
    user_id: uuid.UUID | None = Field(
        exclude=True,
        default=None,
        foreign_key="users.id",
    )
    redeemed: bool = False
    redeemed_at: datetime | None = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=None,
            nullable=True,
        ),
    )


class RedeemCodeRequest(SQLModel):
    code_id: uuid.UUID
    user_id: uuid.UUID
