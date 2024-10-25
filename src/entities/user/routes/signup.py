from http import HTTPStatus
from fastapi import HTTPException, Depends
from src.db.main import get_session
from src.entities.user.router import user_router
from src.entities.user.models import User, UserCreate
from src.entities.user.service import UserService
from src.auth.passwords import generate_password_hash


@user_router.post(
    "/signup",
    response_model=User,
    status_code=HTTPStatus.CREATED,
)
async def signup(
    user: UserCreate,
    db_session=Depends(get_session),
):

    # Check if user already exists
    if await UserService.get_user_by_username(db_session, user.username):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Username already exists",
        )

    if user.email and await UserService.get_user_by_email(db_session, user.email):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Email already registered",
        )

    if user.phone_number and await UserService.get_user_by_phone_number(
        db_session, user.phone_number
    ):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Phone number already registered",
        )

    user.full_name = user.full_name.strip().upper()
    user.username = user.username.strip().lower()
    user.email = user.email.strip().lower() if user.email else None
    user.phone_number = user.phone_number.strip() if user.phone_number else None

    new_user = User(**user.model_dump())

    # double hash the password
    new_user.hashed_password = generate_password_hash(user.password)

    return await UserService.create_user(db_session, new_user)
