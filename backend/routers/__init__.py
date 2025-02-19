__all__ = ["router"]

from fastapi import APIRouter

from .auth import router as auth
from .receipt import router as receipt


router = APIRouter()

router.include_router(auth)
router.include_router(receipt)
