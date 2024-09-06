from urllib import response
from fastapi import APIRouter, Depends

from src.db.main import get_session
from src.entities.public.models import UserLeaderboard
from src.entities.public.service import PublicService

public_router = APIRouter()


@public_router.get(
    "/leaderboard",
    response_model=list[UserLeaderboard],
)
async def get_leaderboard(limit: int = 10, session=Depends(get_session)):
    return await PublicService.get_leaderboard(session, limit)


@public_router.get(
    "/total_users",
    response_model=int,
)
async def get_total_users(session=Depends(get_session)):
    return await PublicService.get_total_users(session)
