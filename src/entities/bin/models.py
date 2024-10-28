from datetime import datetime, timezone
import uuid
from sqlmodel import SQLModel, Column, Field
import sqlalchemy.dialects.postgresql as pg


class DustBinBase(SQLModel):
    __tablename__ = "bins"  # type: ignore

    location: str = Field(
        nullable=False,
    )


class DustBin(DustBinBase, table=True):
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
            pg.TIMESTAMP(timezone=True),
            default=lambda: datetime.now(timezone.utc),
        ),
    )
