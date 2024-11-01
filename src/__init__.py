from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_pagination import add_pagination
from src.db.main import startup, shutdown
from src.entities.user.router import user_router
from src.entities.code.routes import code_router
from src.entities.public.routes import public_router
from src.entities.bin.routes import bin_router
from src.entities.admin.router import admin_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def life_span(app: FastAPI):
    # print("Server is starting")
    await startup()
    yield
    await shutdown()
    # print("Server is shutting down")


app = FastAPI(
    title="QR Earth Server",
    description="Api for QR Earth",
    version="0.2.0",
    lifespan=life_span,
)

origins = [
    "http://192.168.0.21:8000",
    "http://localhost:49807",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_pagination(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(user_router, prefix="/users", tags=["user"])
app.include_router(code_router, prefix="/codes", tags=["code"])
app.include_router(public_router, prefix="/public", tags=["public"])
app.include_router(bin_router, prefix="/bins", tags=["bin"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])
