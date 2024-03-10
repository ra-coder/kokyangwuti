from fastapi import APIRouter

from .upload_file import files_router

router = APIRouter()
router.include_router(files_router)

__all__ = ['router']