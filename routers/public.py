from fastapi import APIRouter, HTTPException, Depends
import schemas
import crud
from http import HTTPStatus
from database.db import get_db

router = APIRouter()


@router.get("/public/leaderboard/", response_model=list[schemas.UserLeaderboard])
async def get_leaderboard(limit: int = 10, db=Depends(get_db)):
    """
    Get a list of all users sorted by number of codes redeemed.
    """
    return await crud.read.get_leaderboard(db, limit=limit)
