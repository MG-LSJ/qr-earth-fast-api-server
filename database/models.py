from __future__ import annotations

from database.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
import uuid


class QRCode(Base):
    __tablename__ = "qrcodes"
    # QR code details
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    # Redeemetion details
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id"), nullable=True, default=None
    )
    redeemed: Mapped[bool] = mapped_column(default=False)
    redeemed_at: Mapped[datetime | None] = mapped_column(nullable=True, default=None)
    # Relationship Nullable Many to One
    user: Mapped[User | None] = relationship(back_populates="codes")

    def __repr__(self):
        return f"<QRCode {self.id}>"


class User(Base):
    __tablename__ = "users"
    # User details
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid1)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str | None] = mapped_column(unique=True, nullable=True)
    phone_number: Mapped[str | None] = mapped_column(unique=True, nullable=True)
    codes_count: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    # Relationship One to Many
    codes: Mapped[list[QRCode]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"
