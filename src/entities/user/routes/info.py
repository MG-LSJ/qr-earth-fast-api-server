from http import HTTPStatus
from fastapi import HTTPException, Depends
from src.entities.user.router import user_router
from src.entities.user.middleware import (
    user_access_token_bearer,
)
from src.db.main import get_session
from src.entities.user.models import User
from src.entities.user.service import UserService


@user_router.get(
    "/info",
    response_model=User,
)
async def get_user_by_id(
    db_session=Depends(get_session),
    token_data: dict = Depends(user_access_token_bearer),
):
    user = await UserService.get_user_by_id(db_session, token_data["user"]["id"])
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )

    return user
