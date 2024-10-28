from http import HTTPStatus
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.auth.constants import REFRESH_TOKEN_EXPIRY
from src.auth.models import AdminLogin
from src.auth.tokens import create_admin_access_token
from src.auth.passwords import verify_password
from src.utils.config import Config
from src.entities.admin.router import admin_router


@admin_router.post(
    "/login",
    response_model=dict,
)
async def admin_login(
    credentails: AdminLogin,
):
    if not verify_password(credentails.password, Config.HASHED_ADMIN_PASSWORD):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Unauthorized",
        )

    access_token = create_admin_access_token(
        refresh=False,
    )

    refresh_token = create_admin_access_token(
        refresh=True,
        expiry=REFRESH_TOKEN_EXPIRY,
    )

    return JSONResponse(
        content={
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
    )
