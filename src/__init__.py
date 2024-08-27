from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.entities.user.routes import user_router
from src.entities.code.routes import code_router
from src.entities.public.routes import public_router


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is starting")
    await init_db()
    yield

    print("Server is shutting down")


app = FastAPI(
    title="App",
    description="App Description",
    version="0.1.0",
    lifespan=life_span,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(user_router, prefix="/users", tags=["user"])
app.include_router(code_router, prefix="/codes", tags=["code"])
app.include_router(public_router, prefix="/public", tags=["public"])
