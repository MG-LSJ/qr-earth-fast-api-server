import uuid
from fastapi import APIRouter, HTTPException, Depends
import schemas
import crud
from http import HTTPStatus
from database.db import get_db

router = APIRouter()
expected_fixed_id = uuid.UUID("654a2bda-05a6-41d8-bc94-6ca6f7520d58")


@router.get(
    "/codes/check",
    response_model=schemas.QRCodeCheck,
)
async def check_code(code_id: uuid.UUID, db=Depends(get_db)):
    qrcode = await crud.read.get_code_by_id(session=db, code_id=code_id)
    if not qrcode:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail={
                "message": "Code not found",
            },
        )
    return qrcode


@router.get(
    "/codes/check_fixed_id",
)
async def check_code_fixed_id(code: uuid.UUID, db=Depends(get_db)):
    if code == expected_fixed_id:
        raise HTTPException(
            status_code=HTTPStatus.OK,
            detail={
                "message": "Code is valid",
                "valid": True,
            },
        )
    else:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={
                "message": "Code is invalid",
                "valid": False,
            },
        )


@router.post(
    "/codes/redeem",
)
async def redeem_code(code_id: uuid.UUID, user_id: uuid.UUID, db=Depends(get_db)):
    res = await crud.update.redeem_code(session=db, user_id=user_id, code_id=code_id)

    match res:
        case 0:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail={
                    "message": "User not found",
                    "valid": False,
                },
            )
        case 1:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail={
                    "message": "Code not found",
                    "valid": False,
                },
            )
        case 2:
            raise HTTPException(
                status_code=HTTPStatus.OK,
                detail={
                    "message": "Code redeemed successfully",
                    "valid": True,
                },
            )
        case 3:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail={
                    "message": "Code already redeemed",
                    "valid": False,
                },
            )


@router.post(
    "/codes/create",
    response_model=schemas.QRCodeCreate,
)
async def create_code(password: str, db=Depends(get_db)):
    if password != "password":
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={
                "message": "Invalid password",
            },
        )
    return await crud.create.create_code(session=db)
