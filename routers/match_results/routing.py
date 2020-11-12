from fastapi import APIRouter
from .feyenoord import router as feyenoord_router

match_router = APIRouter()
match_router.include_router(feyenoord_router)