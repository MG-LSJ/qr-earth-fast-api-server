from src.entities.user.router import user_router
from http import HTTPStatus
from fastapi import HTTPException, Depends
from fastapi_pagination import Page
from src.entities.user.middleware import (
    user_access_token_bearer,
)
from src.db.main import get_session
from src.entities.transaction.models import Transaction
from src.entities.user.service import UserService


@user_router.get(
    "/transactions",
    response_model=Page[Transaction],
)
async def get_user_transactions(
    db_session=Depends(get_session),
    token_data: dict = Depends(user_access_token_bearer),
):
    user = await UserService.get_user_by_id(db_session, token_data["user"]["id"])

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )

    return await UserService.get_user_transactions_page(db_session, user.id)
