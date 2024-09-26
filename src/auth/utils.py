from datetime import datetime, timedelta
import uuid
from passlib.context import CryptContext
import jwt
from src.config import Config
from src.entities.user.models import User
import logging

password_context = CryptContext(
    schemes=["bcrypt"],
)

ACCESS_TOKEN_EXPIRY = timedelta(minutes=15)


def generate_password_hash(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def create_access_token(
    user: User, expiry: timedelta = ACCESS_TOKEN_EXPIRY, refresh: bool = False
) -> str:
    payload = {
        "user": user.model_dump(mode="json"),
        "exp": datetime.now() + expiry,
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM,
    )

    return token


def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM],
        )
        return payload
    except jwt.PyJWTError as e:
        logging.error(f"Error decoding token: {e}")
        return None
