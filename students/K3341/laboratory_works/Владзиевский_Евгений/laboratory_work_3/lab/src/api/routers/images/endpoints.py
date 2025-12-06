import random

from PIL import Image, ImageOps
from fastapi import APIRouter, UploadFile, Depends, HTTPException
from fastapi.responses import RedirectResponse

from src import config
from src.api.routers.images.models import UploadResponse
from src.api.security import access_policy
from src.api.sessions import get_s3_session_async, get_db_session
from src.db.crud import add_image

router = APIRouter(
    prefix="/image",
    tags=["images"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(access_policy)]
)


@router.post("/upload", response_model=UploadResponse)
async def upload_frames(file: UploadFile,
                        s3=Depends(get_s3_session_async), session=Depends(get_db_session),
                        credentials=Depends(access_policy)):
    if file.filename.split(".")[-1] not in config.ALLOWED_IMAGE_EXTENSIONS:
        HTTPException(status_code=400, detail="Wrong file extension!")
    hash_name = f'{random.randbytes(15).hex()}.{file.filename.split(".")[-1]}'
    async with s3 as s3_session:
        await s3_session.upload_fileobj(file.file, config.S3_BUCKET, hash_name)
    pil = Image.open(file.file)
    pil = ImageOps.exif_transpose(pil)
    width, height = pil.size
    await add_image(session, credentials.subject['id'], hash_name, width, height)
    return {'hash': hash_name, 'width': width, 'height': height}


@router.get('/{hash:str}')
async def get_image(hash: str, s3=Depends(get_s3_session_async)):
    async with s3 as s3_session:
        url = await s3_session.generate_presigned_url('get_object', Params={'Bucket': config.S3_BUCKET, 'Key': hash},
                                                      ExpiresIn=3600)
        return RedirectResponse(url=url)
