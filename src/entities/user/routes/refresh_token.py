from http import HTTPStatus
from src.db.cache import JTIBlocklistCache
from src.entities.user.router import user_router
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from src.auth.constants import REFRESH_TOKEN_EXPIRY
from src.entities.user.middleware import (
    user_refresh_token_bearer,
)
from src.entities.user.models import User
from src.auth.tokens import (
    create_user_access_token,
    decode_access_token,
    decode_expired_access_token,
)


@user_router.get(
    "/refresh_token",
    response_model=dict,
)
async def refresh_tokens(
    access_token: str,
    refresh_token_data: dict = Depends(user_refresh_token_bearer),
):

    if access_token_data := decode_access_token(access_token):
        if access_token_data["user"]["id"] != refresh_token_data["user"]["id"]:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid token",
            )
        await JTIBlocklistCache.add(access_token_data["jti"])

    elif access_token_data := decode_expired_access_token(access_token):
        if access_token_data["user"]["id"] != refresh_token_data["user"]["id"]:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid token",
            )
    else:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid token",
        )

    await JTIBlocklistCache.add(refresh_token_data["jti"])

    access_token = create_user_access_token(
        user=User(**refresh_token_data["user"]),
    )

    refresh_token = create_user_access_token(
        user=User(**refresh_token_data["user"]),
        refresh=True,
        expiry=REFRESH_TOKEN_EXPIRY,
    )

    return JSONResponse(
        content={
            "message": "Access token",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )
