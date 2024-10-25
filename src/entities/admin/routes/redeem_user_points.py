from http import HTTPStatus
import uuid
from fastapi import HTTPException, Depends
from src.db.main import get_session
from src.entities.admin.middleware import admin_access_token_bearer
from src.entities.user.models import User
from src.entities.user.service import UserService
from src.entities.admin.router import admin_router


@admin_router.get(
    "/redeem_user_points",
    response_model=User,
)
async def redeem_user_points(
    user_id: uuid.UUID,
    points: int,
    db_session=Depends(get_session),
    token_data=Depends(admin_access_token_bearer),
):
    if points < 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Points must be positive",
        )

    user = await UserService.get_user_by_id(db_session, user_id)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )

    if user.points < points:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Insufficient points",
        )

    return await UserService.redeem_user_points(db_session, user, points)
