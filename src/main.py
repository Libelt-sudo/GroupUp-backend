from contextlib import asynccontextmanager

from fastapi import FastAPI
from .auth.router import router as auth_router
from .groups.router import router as groups_router

from .database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(groups_router)