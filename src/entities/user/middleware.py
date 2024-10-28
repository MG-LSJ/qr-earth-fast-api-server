from http import HTTPStatus
from typing import override
from fastapi import HTTPException
from src.auth.middleware import TokenBearer


class UserTokenBearer(TokenBearer):
    @override
    async def verify_token_data(self, token_data: dict):
        await super().verify_token_data(token_data)
        if token_data["user"] is None:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid token",
            )


class UserAccessTokenBearer(UserTokenBearer):
    @override
    async def verify_token_data(self, token_data: dict):
        await super().verify_token_data(token_data)
        if token_data["refresh"] == True:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid token",
            )


class UserRefreshTokenBearer(UserTokenBearer):
    @override
    async def verify_token_data(self, token_data: dict):
        await super().verify_token_data(token_data)
        if token_data["refresh"] == False:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid token",
            )


user_access_token_bearer = UserAccessTokenBearer()
user_refresh_token_bearer = UserRefreshTokenBearer()
