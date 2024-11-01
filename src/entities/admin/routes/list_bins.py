from src.entities.admin.router import admin_router
from fastapi import Depends
from src.db.main import get_session
from src.entities.bin.models import DustBin
from src.entities.bin.service import DustBinService
from src.entities.admin.middleware import admin_access_token_bearer
from fastapi_pagination import Page


@admin_router.get(
    "/list_bins",
    response_model=Page[DustBin],
)
async def list_bins(
    db_session=Depends(get_session),
    token_data=Depends(admin_access_token_bearer),
):
    return await DustBinService.get_all_dust_bins_page(
        db_session,
    )
