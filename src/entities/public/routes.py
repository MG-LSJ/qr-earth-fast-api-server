from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from src.db.cache import Cache
from src.db.main import get_session
from src.entities.public.models import UserLeaderboard
from src.entities.public.service import PublicService

public_router = APIRouter()


@public_router.get(
    "/leaderboards",
    response_model=Page[UserLeaderboard],
)
async def get_leaderboard(session=Depends(get_session)):
    return await PublicService.get_leaderboards_page(session)


@public_router.get(
    "/total_users",
    response_model=int,
)
async def get_total_users(session=Depends(get_session)):
    return await Cache.get_total_users()
