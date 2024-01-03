from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.config import create_db_and_tables


@asynccontextmanager
async def on_startup(_):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=on_startup)