from http import HTTPStatus
from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse
from src.entities.user.router import user_router
from src.auth.constants import REFRESH_TOKEN_EXPIRY
from src.db.main import get_session
from src.entities.user.models import LoginResponse, UserLogin
from src.entities.user.service import UserService
from src.auth.tokens import create_user_access_token
from src.auth.passwords import verify_password


@user_router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    user: UserLogin,
    db_session=Depends(get_session),
):
    existing_user = None

    user.username = user.username.strip().lower() if user.username else None
    user.email = user.email.strip().lower() if user.email else None
    user.phone_number = user.phone_number.strip() if user.phone_number else None

    if user.username:
        existing_user = await UserService.get_user_by_username(
            db_session, user.username
        )
        if not existing_user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Username not found",
            )

    elif user.email:
        existing_user = await UserService.get_user_by_email(db_session, user.email)
        if not existing_user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Email not found",
            )

    elif user.phone_number:
        existing_user = await UserService.get_user_by_phone_number(
            db_session, user.phone_number
        )
        if not existing_user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Phone number not found",
            )

    else:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Usernmae, email or phone_number is required",
        )

    if not verify_password(
        user.password,
        existing_user.hashed_password,
    ):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Wrong password",
        )

    access_token = create_user_access_token(
        user=existing_user,
    )
    refresh_token = create_user_access_token(
        user=existing_user,
        refresh=True,
        expiry=REFRESH_TOKEN_EXPIRY,
    )

    return JSONResponse(
        content={
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": existing_user.model_dump(mode="json"),
        },
    )
