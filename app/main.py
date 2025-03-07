from fastapi import FastAPI

from app.api.routes import router
from app.core.db import init_db

app = FastAPI()


@app.on_event("startup")
async def startup():
    await init_db()


app.include_router(router, prefix="/api")
