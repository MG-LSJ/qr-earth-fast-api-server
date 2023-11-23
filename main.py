from fastapi import FastAPI
from database.db import asyncEngine, Base
from routers import public, user, codes
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    async with asyncEngine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    print("Shutting down...")


app = FastAPI(
    title="QR Code API",
    description="An API to redeem QR codes",
    version="0.0.1",
    docs_url="/",
    lifespan=lifespan,
)

app.include_router(public.router)
app.include_router(user.router)
app.include_router(codes.router)
