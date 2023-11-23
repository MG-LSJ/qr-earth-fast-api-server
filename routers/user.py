import uuid
from fastapi import APIRouter, HTTPException, Depends
import schemas
import crud
from http import HTTPStatus
from database.db import get_db

router = APIRouter()


@router.post(
    "/create_user",
    response_model=schemas.User,
    status_code=HTTPStatus.CREATED,
)
async def create_user(user: schemas.UserCreate, db=Depends(get_db)):
    """
    Create a new user.
    """
    # check if user already exists
    if await crud.read.get_user_by_username(session=db, username=user.username):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Username already registered",
        )
    if user.email:
        if await crud.read.get_user_by_email(session=db, email=user.email):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Email already registered",
            )

    if user.phone_number:
        if await crud.read.get_user_by_phone_number(
            session=db, phone_number=user.phone_number
        ):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Phone number already registered",
            )

    return await crud.create.create_user(session=db, user=user)


@router.get("/get/user/by/user_id/", response_model=schemas.User)
async def get_user_by_id(user_id: uuid.UUID, db=Depends(get_db)):
    """
    Get a user by id.
    """
    usr = await crud.read.get_user_by_id(session=db, user_id=user_id)
    if not usr:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )
    return usr


@router.get("/get/user/by/username/", response_model=schemas.User)
async def get_user_by_username(username: str, hashed_password: str, db=Depends(get_db)):
    """
    Get a user by username and password.
    """
    usr = await crud.read.get_user_by_username(session=db, username=username)
    if not usr:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )
    if usr.hashed_password != hashed_password:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect password",
        )
    return usr


@router.get("/get/user/by/email/", response_model=schemas.User)
async def get_user_by_email(email: str, hashed_password: str, db=Depends(get_db)):
    """
    Get a user by email and password.
    """
    usr = await crud.read.get_user_by_email(session=db, email=email)
    if not usr:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )
    if usr.hashed_password != hashed_password:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect password",
        )
    return usr


@router.get("/get/user/by/phone_number/", response_model=schemas.User)
async def get_user_by_phone_number(
    phone_number: str, hashed_password: str, db=Depends(get_db)
):
    """
    Get a user by phone number and password.
    """
    usr = await crud.read.get_user_by_phone_number(
        session=db, phone_number=phone_number
    )
    if not usr:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )
    if usr.hashed_password != hashed_password:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect password",
        )
    return usr


@router.get(
    "/get/user/history/",
    response_model=list[schemas.QRCode],
)
async def get_user_history(user_id: uuid.UUID, limit: int = 20, db=Depends(get_db)):
    """
    Get a user's history by user id.
    """
    res = await crud.read.get_user_codes(session=db, user_id=user_id, limit=limit)

    if res is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )
    return res
