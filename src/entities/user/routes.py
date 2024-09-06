from http import HTTPStatus
import uuid
from fastapi import APIRouter, HTTPException, Depends
from src.config import Config
from src.db.main import get_session
from src.entities.transaction.models import Transaction
from src.entities.user.models import User, UserCreate, UserLogin
from src.entities.user.service import UserService
from src.utils import generate_password_hash, verify_password

user_router = APIRouter()


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
            status_code=HTTPStatus.CONFLICT, detail="Username already exists"
        )

    if user.email and await UserService.get_user_by_email(db_session, user.email):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Email already registered"
        )

    if user.phone_number and await UserService.get_user_by_phone_number(
        db_session, user.phone_number
    ):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Phone number already registered"
        )

    new_user = User(**user.model_dump())

    # double hash the password
    new_user.hashed_password = generate_password_hash(user.password)

    return await UserService.create_user(db_session, new_user)


@user_router.post(
    "/login",
    response_model=User,
    status_code=200,
)
async def login(
    user: UserLogin,
    db_session=Depends(get_session),
):
    existing_user = None

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

    return existing_user


@user_router.get("/info", response_model=User)
async def get_user_by_id(
    user_id: uuid.UUID,
    db_session=Depends(get_session),
):
    user = await UserService.get_user_by_id(db_session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@user_router.get("/transactions", response_model=list[Transaction])
async def get_user_transactions(
    user_id: uuid.UUID,
    qunatiy: int = 10,
    db_session=Depends(get_session),
):
    user = await UserService.get_user_by_id(db_session, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return await UserService.get_user_transactions(db_session, user.id, qunatiy)


@user_router.get("/redeem", response_model=User)
async def redeem_user_points(
    user_id: uuid.UUID,
    points: int,
    admin_password: str,
    db_session=Depends(get_session),
):
    if admin_password != Config.ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if points < 0:
        raise HTTPException(status_code=400, detail="Points must be positive")

    user = await UserService.get_user_by_id(db_session, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.points < points:
        raise HTTPException(status_code=400, detail="Insufficient points")

    return await UserService.redeem_user_points(db_session, user, points)
