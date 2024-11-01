from fastapi.responses import JSONResponse
from src.entities.admin.router import admin_router
from fastapi import Depends
from src.entities.admin.middleware import admin_access_token_bearer


@admin_router.get(
    "/session_valid",
)
async def session_valid(
    token_data=Depends(admin_access_token_bearer),
):
    return JSONResponse(content={"message": "Session is valid"})
