from fastapi import FastAPI
from database.db import asyncEngine, Base
from routers import public, user, codes

app = FastAPI(
    title="QR Code API",
    description="An API to redeem QR codes",
    version="0.0.1",
    docs_url="/",
)

app.include_router(public.router)
app.include_router(user.router)
app.include_router(codes.router)


@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    async with asyncEngine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
