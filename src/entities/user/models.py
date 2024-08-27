from datetime import datetime
import uuid
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg


class UserBase(SQLModel):
    __tablename__ = "users"  # type: ignore

    username: str
    email: str | None = Field(nullable=True)
    phone_number: str | None = Field(nullable=True)


class UserCreate(UserBase):
    password: str


class UserLogin(UserCreate):
    username: str | None = None


class User(UserBase, table=True):
    id: uuid.UUID = Field(
        sa_column=Column(
            type_=pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )

    hashed_password: str = Field(exclude=True)

    redeemed_code_count: int = Field(default=0)
    points: int = Field(default=0)
    deleted: bool = Field(default=False)

    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now,
        ),
    )

    def __repr__(self) -> str:
        return f"<User {self.username} id {self.id}>"
