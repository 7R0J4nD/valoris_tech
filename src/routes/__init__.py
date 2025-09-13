from fastapi import APIRouter
from src.routes import user_route


router = APIRouter()

router.include_router(user_route.router, prefix="/users", tags=["Users"])
