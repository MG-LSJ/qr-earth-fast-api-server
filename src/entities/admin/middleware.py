from http import HTTPStatus
from typing import override
from fastapi import HTTPException
from src.auth.middleware import TokenBearer


class AdminTokenBearer(TokenBearer):

    @override
    def verify_token_data(self, token_data: dict):
        super().verify_token_data(token_data)
        if token_data["admin"] is None:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid token",
            )


class AdminAccessTokenBearer(AdminTokenBearer):
    @override
    def verify_token_data(self, token_data: dict):
        super().verify_token_data(token_data)
        if token_data["refresh"] == True:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid token",
            )


class AdminRefreshTokenBearer(AdminTokenBearer):
    @override
    def verify_token_data(self, token_data: dict):
        super().verify_token_data(token_data)
        if token_data["refresh"] == False:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid token",
            )


admin_access_token_bearer = AdminAccessTokenBearer()
admin_refresh_token_bearer = AdminRefreshTokenBearer()
