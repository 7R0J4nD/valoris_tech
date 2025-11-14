from fastapi import APIRouter

from src.users.routes import router as users_router
from src.admin.routes import router as admin_router
from src.auth.routes import router as auth_router
from src.websocket import ws_router

router = APIRouter()

# Inclut les sous-routers
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(admin_router, prefix="/admin", tags=["Admin"])
router.include_router(ws_router)  # websocket
