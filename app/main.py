from fastapi import FastAPI

from app import routes

bubblemaps = FastAPI()

bubblemaps.include_router(routes.router)
