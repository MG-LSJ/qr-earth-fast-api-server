from src.entities.admin.router import admin_router
from fastapi import Depends
from src.db.main import get_session
from src.entities.bin.models import DustBin
from src.entities.bin.service import DustBinService
from src.entities.admin.middleware import admin_access_token_bearer


@admin_router.post(
    "/create_bin",
    response_model=DustBin,
)
async def create_bin(
    location: str,
    db_session=Depends(get_session),
    token_data=Depends(admin_access_token_bearer),
):
    return await DustBinService.create_dust_bin(
        db_session,
        location,
    )
