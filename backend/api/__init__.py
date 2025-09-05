from fastapi import APIRouter
from .users import router as users_router
from .repos import router as repos_router

api_router = APIRouter()
api_router.include_router(users_router)
api_router.include_router(repos_router)
