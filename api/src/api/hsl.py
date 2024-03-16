import os
from uuid import uuid4

from fastapi import APIRouter, UploadFile
from fastapi.responses import ORJSONResponse

from ..tasks import hsl

__all__ = [
    'router'
]

router = APIRouter(
    prefix='/hsl',
    default_response_class=ORJSONResponse,
    tags=['hsl']
)


@router.post('')
async def upload_file_to_hsl(
        file: UploadFile,
):
    folder_path = f'media/hsl/{uuid4()}'
    file_path = f'{folder_path}/{file.filename}'

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    with open(file_path, 'wb') as save_file:
        save_file.write(await file.read())

    hsl.delay(file_path, folder_path)

    return {'status': 'ok'}
