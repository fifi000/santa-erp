from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.config import create_db_and_tables
from api.routers import elves, items


@asynccontextmanager
async def on_startup(_):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=on_startup)

app.include_router(elves.router)
app.include_router(items.router)


@app.get('/')
async def root():
    return {'message': 'Hi there!'}