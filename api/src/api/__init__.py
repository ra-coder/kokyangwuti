from fastapi import APIRouter

from .upload_file import router as upload_router
from .hsl import router as hsl_router

__all__ = [
    'router'
]

router = APIRouter(prefix='')
router.include_router(router=upload_router)
router.include_router(router=hsl_router)
