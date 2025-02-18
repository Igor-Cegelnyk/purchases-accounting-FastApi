__all__ = ["router"]

from fastapi import APIRouter

from .auth import router as auth


router = APIRouter()

router.include_router(auth)
