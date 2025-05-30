from fastapi import APIRouter

from .routes import tasks

api_router = APIRouter()
api_router.include_router(tasks.router)
