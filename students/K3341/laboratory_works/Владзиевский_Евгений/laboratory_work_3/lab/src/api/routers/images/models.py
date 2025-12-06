import urllib3

from pydantic import BaseModel, Field
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated

from src import config
from src.api.sessions import get_s3_session_sync



def hash_to_url(hash: str) -> str:
    return urllib3.util.parse_url(config.S3_URL).url + '/' + config.S3_BUCKET + '/' + hash


image_url = Annotated[str, AfterValidator(hash_to_url)]


class UploadResponse(BaseModel):
    hash: str
    width: int
    height: int


class ImageResponse(BaseModel):
    url: image_url = Field(None, validation_alias='hash')
    width: int
    height: int
