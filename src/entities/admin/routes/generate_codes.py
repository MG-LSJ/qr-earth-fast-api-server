from src.entities.admin.router import admin_router
from fastapi import Depends
from src.db.main import get_session
from src.entities.code.models import QRCodeCreate
from src.entities.admin.middleware import admin_access_token_bearer
from src.entities.code.service import QRCodeService


@admin_router.get(
    "/generate_codes",
    response_model=list[QRCodeCreate],
)
async def generate_code(
    value: int = 10,
    quantity: int = 1,
    db_session=Depends(get_session),
    token_data=Depends(admin_access_token_bearer),
):
    return await QRCodeService.generate_qr_codes(db_session, value, quantity)
