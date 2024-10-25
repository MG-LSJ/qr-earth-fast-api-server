from src.db.cache import JTIBlocklistCache
from src.entities.admin.router import admin_router
from fastapi import Depends
from fastapi.responses import JSONResponse
from src.auth.constants import REFRESH_TOKEN_EXPIRY
from src.entities.admin.middleware import admin_refresh_token_bearer
from src.auth.tokens import (
    create_admin_access_token,
)


@admin_router.get(
    "/refresh_token",
    response_model=dict,
)
async def refresh_token(
    refresh_token_data: dict = Depends(admin_refresh_token_bearer),
):
    await JTIBlocklistCache.add(refresh_token_data["jti"])

    access_token = create_admin_access_token(
        refresh=False,
    )
    refresh_token = create_admin_access_token(
        refresh=True,
        expiry=REFRESH_TOKEN_EXPIRY,
    )

    return JSONResponse(
        content={
            "message": "Token refreshed",
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
    )
