from datetime import datetime, timezone
import uuid
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg


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
    value: int = Field(default=10)


class QRCodeCreate(QRCodeBase):
    pass


class QRCode(QRCodeBase, table=True):
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            default=lambda: datetime.now(timezone.utc),
        ),
    )

    user_id: uuid.UUID | None = Field(
        exclude=True,
        default=None,
        foreign_key="users.id",
    )
    redeemed: bool = False
    redeemed_at: datetime | None = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            default=None,
            nullable=True,
        ),
    )


class QRCodeRedeem(SQLModel):
    code_id: uuid.UUID
    bin_id: uuid.UUID
