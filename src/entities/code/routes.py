import uuid
from fastapi import APIRouter, HTTPException, Depends
from src.config import Config
from src.db.main import get_session
from src.entities.code.models import QRCode, RedeemCodeRequest
from src.entities.code.service import QRCOdeService
from src.entities.user.service import UserService


code_router = APIRouter()


@code_router.get("/check_fixed")
async def check(fixed_code_id: str):
    if fixed_code_id == Config.FIXED_CODE:
        return {"valid": True}
    raise HTTPException(status_code=400, detail="Invalid code")


@code_router.get("/generate", response_model=QRCode)
async def generate_code(
    admin_password: str,
    value: int = 10,
    session=Depends(get_session),
):
    if admin_password != Config.ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return await QRCOdeService.generate_qr_code(session, value)


@code_router.get("/validate", response_model=QRCode)
async def validate_code(code_id: uuid.UUID, session=Depends(get_session)):
    qr_code = await QRCOdeService.get_qr_code_by_code(session, code_id)

    if qr_code is None:
        raise HTTPException(status_code=400, detail="Invalid code")

    return qr_code


@code_router.post("/redeem", response_model=QRCode)
async def redeem_code(
    redeem_request: RedeemCodeRequest,
    session=Depends(get_session),
):
    qr_code = await QRCOdeService.get_qr_code_by_code(session, redeem_request.code_id)

    if qr_code is None:
        raise HTTPException(status_code=400, detail="Invalid code")

    if qr_code.redeemed:
        raise HTTPException(status_code=400, detail="Code already redeemed")

    user = await UserService.get_user_by_id(session, redeem_request.user_id)

    if user is None:
        raise HTTPException(status_code=400, detail="User does not exist")

    return await QRCOdeService.redeem_qr_code(session, qr_code, user)
