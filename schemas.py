from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict


class QRCodeBase(BaseModel):
    id: uuid.UUID
    created_at: datetime


class QRCodeCreate(QRCodeBase):
    pass

    model_config = ConfigDict(from_attributes=True)


class QRCode(QRCodeBase):
    user_id: uuid.UUID | None
    redeemed: bool = False
    redeemed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class QRCodeCheck(QRCodeBase):
    created_at: datetime
    redeemed: bool = False
    redeemed_at: datetime | None


class UserBase(BaseModel):
    username: str
    email: str | None = None
    phone_number: str | None = None


class UserCreate(UserBase):
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    id: uuid.UUID
    codes_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLeaderboard(BaseModel):
    username: str
    codes_count: int

    model_config = ConfigDict(from_attributes=True)
