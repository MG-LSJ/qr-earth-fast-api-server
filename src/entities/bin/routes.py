from http import HTTPStatus
import uuid
from fastapi import APIRouter, HTTPException, Depends
from src.db.main import get_session
from src.entities.bin.models import DustBin
from src.entities.bin.service import DustBinService

bin_router = APIRouter()


@bin_router.get(
    "/info",
    response_model=DustBin,
)
async def bin_info(
    bin_id: uuid.UUID,
    db_session=Depends(get_session),
):
    dust_bin = await DustBinService.get_dust_bin_by_id(db_session, bin_id)

    if dust_bin is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Invalid bin",
        )

    return dust_bin
