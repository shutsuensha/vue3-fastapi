from fastapi import FastAPI

from app.api.v1.api import api_router
from app.middlewares.cors import register_cors

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")


register_cors(app)
