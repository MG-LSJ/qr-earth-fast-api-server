from datetime import datetime, timedelta, timezone
import uuid
import jwt
from src.auth.constants import ACCESS_TOKEN_EXPIRY
from src.utils.config import Config
from src.entities.user.models import User
import logging


def create_user_access_token(
    user: User,
    expiry: timedelta = ACCESS_TOKEN_EXPIRY,
    refresh: bool = False,
) -> str:
    return create_acces_token(
        expiry=expiry,
        refresh=refresh,
        user=user.model_dump(mode="json"),
    )


def create_admin_access_token(
    expiry: timedelta = ACCESS_TOKEN_EXPIRY,
    refresh: bool = False,
) -> str:
    return create_acces_token(
        expiry=expiry,
        refresh=refresh,
        admin=True,
    )


def create_acces_token(
    expiry: timedelta = ACCESS_TOKEN_EXPIRY,
    refresh: bool = False,
    **kwargs,
) -> str:
    payload = {
        "exp": datetime.now(timezone.utc) + expiry,
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
        **kwargs,
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


def decode_expired_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM],
            options={"verify_exp": False},
        )
        return payload
    except jwt.PyJWTError as e:
        logging.error(f"Error decoding token: {e}")
        return None
