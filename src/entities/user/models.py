from datetime import datetime, timezone
import uuid
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg


class UserBase(SQLModel):
    __tablename__ = "users"  # type: ignore
    email: str | None = Field(nullable=True)
    phone_number: str | None = Field(nullable=True)


class UserCreate(UserBase):
    username: str
    password: str
    full_name: str


class UserLogin(UserBase):
    username: str | None
    password: str


class User(UserBase, table=True):
    id: uuid.UUID = Field(
        sa_column=Column(
            type_=pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )
    username: str
    hashed_password: str = Field(exclude=True)
    full_name: str
    redeemed_code_count: int = Field(default=0)
    points: int = Field(default=0)
    deleted: bool = Field(default=False)

    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            default=lambda: datetime.now(timezone.utc),
        ),
    )

    def __repr__(self) -> str:
        return f"<User {self.username} id {self.id}>"


class LoginResponse(SQLModel):
    message: str
    access_token: str
    refresh_token: str
    user: User
