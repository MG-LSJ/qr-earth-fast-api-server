from http import HTTPStatus
import uuid
from fastapi import APIRouter, HTTPException, Depends
from src.db.main import get_session
from src.entities.bin.service import DustBinService
from src.entities.code.models import QRCode, QRCodeRedeem
from src.entities.code.service import QRCodeService
from src.entities.user.service import UserService
from src.entities.user.middleware import user_access_token_bearer

code_router = APIRouter()


@code_router.get(
    "/info",
    response_model=QRCode,
)
async def code_info(
    code_id: uuid.UUID,
    db_session=Depends(get_session),
):
    qr_code = await QRCodeService.get_qr_code_by_id(db_session, code_id)

    if qr_code is None:
        raise HTTPException(status_code=400, detail="Invalid code")

    return qr_code


@code_router.post(
    "/redeem",
    response_model=QRCode,
)
async def redeem_code(
    data: QRCodeRedeem,
    db_session=Depends(get_session),
    token_data: dict = Depends(user_access_token_bearer),
):
    dust_bin = await DustBinService.get_dust_bin_by_id(db_session, data.bin_id)

    if dust_bin is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Invalid bin",
        )

    qr_code = await QRCodeService.get_qr_code_by_id(db_session, data.code_id)

    if qr_code is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Invalid code",
        )

    if qr_code.redeemed:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Code already redeemed",
        )

    user = await UserService.get_user_by_id(db_session, token_data["user"]["id"])

    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="User does not exist",
        )

    return await QRCodeService.redeem_qr_code(db_session, qr_code, user)
