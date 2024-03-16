from aiobotocore.session import get_session
from fastapi import APIRouter, UploadFile
from fastapi.responses import ORJSONResponse

from ..config import settings

__all__ = [
    'router'
]

router = APIRouter(
    prefix='/s3',
    default_response_class=ORJSONResponse,
    tags=['s3']
)

READ_CHUNK_SIZE = 10 * 1024 * 1024  # 10 Mb


async def upload_file_to_s3(
        filename_key: str,
        file_stream: UploadFile,
        basket: str = "kokyangwuti-storage",
):
    parts_info = []
    session = get_session()
    async with session.create_client(
            service_name='s3',
            region_name=settings.AWS_S3_REGION_NAME,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    ) as client:
        create_multipart_upload_resp = await client.create_multipart_upload(
            Key=filename_key,
            Bucket=basket,
        )
        upload_id = create_multipart_upload_resp['UploadId']

        part_number = 0
        while True:
            contents = await file_stream.read(READ_CHUNK_SIZE)
            if not contents:
                break

            part_number += 1
            part_upload_resp = await client.upload_part(
                Body=contents,
                UploadId=upload_id,
                PartNumber=part_number,
                Key=filename_key,
                Bucket=basket,
            )
            parts_info.append(
                {
                    'PartNumber': part_number,
                    'ETag': part_upload_resp['ETag']
                }
            )

        await client.complete_multipart_upload(
            UploadId=upload_id,
            Key=filename_key,
            Bucket=basket,
            MultipartUpload={"Parts": parts_info},
        )


@router.post("/upload_file")
async def upload_file(
        file: UploadFile,
):
    parts_info = await upload_file_to_s3(filename_key=f'debug/original/{file.filename}', file_stream=file)
    return {
        "file": file.filename,
        "parts_info": parts_info,
    }

# @app.get("/download_file")
# async def dowload_from_s3():
#     resp = yield from s3.get_object(Bucket='mybucket', Key='k')
#     stream = resp['Body']
#     try:
#         chunk = yield from stream.read(10)
#         while len(chunk) > 0:
#             ...
#             chunk = yield from stream.read(10)
#     finally:
#         stream.close()


# @app.get("/files/")
# def read_stream():
#     return StreamingResponse(some_generator, media_type='application/json')
